from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

# Create your models here.
User = get_user_model()

RATING_CHOICES = (
        (1, 'π'),
        (2, 'ππ'),
        (3, 'πππ'),
        (4, 'ππππ'),
        (5, 'πππππ'),
    )


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, primary_key=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'ΠΠ°ΡΠ΅Π³ΠΎΡΠΈΡ'
        verbose_name_plural = 'ΠΠ°ΡΠ΅Π³ΠΎΡΠΈΠΈ'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    image = models.ImageField(upload_to='products')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'ΠΡΠΎΠ΄ΡΠΊΡ'
        verbose_name_plural = 'ΠΡΠΎΠ΄ΡΠΊΡΡ'


class CommentAndRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.rating and self.text:
            return f'Comment and rating from {self.author.name} to {self.product}'
        elif self.rating:
            return f'Rating from {self.author.name} to {self.product}'
        elif self.text:
            return f'Comment from {self.author.name} to {self.product}'

    class Meta:
        verbose_name = 'ΠΠΎΠΌΠΌΠ΅Π½ΡΠ°ΡΠΈΠΉ'
        verbose_name_plural = 'ΠΠΎΠΌΠΌΠ΅Π½ΡΠ°ΡΠΈΠΈ'
        ordering = ['-create_date']


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: favorites {self.product}'

    class Meta:
        verbose_name = 'ΠΠ·Π±ΡΠ°Π½Π½ΠΎΠ΅'
        verbose_name_plural = 'ΠΠ·Π±ΡΠ°Π½Π½ΡΠ΅'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: liked {self.product}'

    class Meta:
        verbose_name = 'ΠΠ°ΠΉΠΊ'
        verbose_name_plural = 'ΠΠ°ΠΉΠΊΠΈ'

