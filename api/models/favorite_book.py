from django.db import models


class FavoriteQuerySet(models.QuerySet):
    def favorited(self):
        return self.filter(isFavorite=True)

    def not_favorited(self):
        return self.filter(isFavorite=False)


class FavoriteManager(models.Manager):
    def get_queryset(self):
        return FavoriteQuerySet(self.model, using=self._db)

    def favorited(self):
        return self.get_queryset().favorited()

    def not_favorited(self):
        return self.get_queryset().not_favorited()


class FavoriteBook(models.Model):
    book = models.ForeignKey('Book', models.PROTECT)
    user = models.ForeignKey('User', models.PROTECT)
    isFavorite = models.BooleanField()

    # objects = FavoriteManager()
    objects = FavoriteQuerySet.as_manager()

    class Meta:
        db_table = 'favorite_book'
        unique_together = (("book", "user"),)
