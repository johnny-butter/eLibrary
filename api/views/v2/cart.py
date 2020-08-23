from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from api.serializers import cartSerializer


class shopCarManage(mixins.ListModelMixin, GenericViewSet):

    serializer_class = cartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()

        action = self.request.query_params.get('action', 'add')
        if action == 'add':
            cart.quantity += 1
        elif action == 'cut':
            cart.quantity = cart.quantity - 1 if cart.quantity > 0 else 0

        cart.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        self.queryset = self.request.user.shopcar_set.exclude(quantity=0)
        return super(shopCarManage, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        action = self.request.query_params.get('del', 'one')
        if action == 'one':
            instance = self.request.user.shopcar_set.filter(
                book=request.data.get('book'))
        elif action == 'all':
            instance = self.request.user.shopcar_set.all()

        result = instance.delete()

        resp = {
            'data': {'delete_count': result[0]}
        }

        return Response(resp, status=status.HTTP_200_OK)
