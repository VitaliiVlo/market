from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Products Categories'


class Product(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    category = models.ForeignKey(ProductCategory, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.name, self.price)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='img/')
    is_main = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Products Images'


def product_image_post_save(sender, instance, created, **kwargs):
    product = instance.product
    if not product.productimage_set.filter(is_main=True).exists():
        instance.is_main = True
        instance.save()


post_save.connect(product_image_post_save, sender=ProductImage)


class Rating(models.Model):
    name = models.CharField(max_length=64)
    stars = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.name, self.stars)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Comment(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    rating = models.ForeignKey(Rating)
    text = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Product Comment'
        verbose_name_plural = 'Product Comments'


def comment_post_save(sender, instance, created, **kwargs):
    product = instance.product
    average = Comment.objects.filter(product=product).aggregate(Avg('rating__stars'))
    product.average_rating = average['rating__stars__avg']
    product.save()


post_save.connect(comment_post_save, sender=Comment)
