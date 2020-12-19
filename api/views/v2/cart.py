from rest_framework import status, mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import CartSerializer
from api.models import Book


class ShopCarManager(mixins.ListModelMixin, GenericViewSet):

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @Book.stock_opt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()

        action = self.request.query_params.get('action', 'add')
        amount = int(self.request.query_params.get('amount', '1'))
        if action == 'add':
            cart.add_quantity(amount=amount)
            cart.book.cut_stock(amount=amount)
        elif action == 'cut':
            if cart.quantity < amount:
                cart.book.add_stock(amount=cart.quantity)
                cart.quantity = 0
            else:
                cart.book.add_stock(amount=amount)
                cart.cut_quantity(amount=amount)

        cart.save()
        cart.book.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        self.queryset = self.request.user.shopcar_set.exclude(quantity=0)
        return super(ShopCarManager, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cart_items = self.request.user.shopcar_set.all()

        result = cart_items.delete()

        resp = {
            'data': {'delete_count': result[0]}
        }

        return Response(resp, status=status.HTTP_200_OK)
