from django.db import models


class favoriteQuerySet(models.QuerySet):
    def favorited(self):
        return self.filter(isFavorite=True)

    def not_favorited(self):
        return self.filter(isFavorite=False)


class favoriteManager(models.Manager):
    def get_queryset(self):
        return favoriteQuerySet(self.model, using=self._db)

    def favorited(self):
        return self.get_queryset().favorited()

    def not_favorited(self):
        return self.get_queryset().not_favorited()


class favoriteBook(models.Model):
    book = models.ForeignKey('Book', models.PROTECT)
    user = models.ForeignKey('User', models.PROTECT)
    isFavorite = models.BooleanField()

    # objects = favoriteManager()
    objects = favoriteQuerySet.as_manager()

    class Meta:
        db_table = 'favorite_book'
        unique_together = (("book", "user"),)
