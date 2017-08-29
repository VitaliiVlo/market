from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class ProductInBasket(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    nmb = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Product In Basket'
        verbose_name_plural = 'Products In Basket'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.total_price = int(self.nmb) * price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)
