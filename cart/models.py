from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    @property
    def total(self):
        return sum(
            item.subtotal
            for item in self.items.select_related("product")
        )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT
    )

    size = models.ForeignKey(
        "catalog.Size",
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product", "size"],
                name="unique_cart_product_size"
            )
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class PromoCode(models.Model):
    code = models.CharField(
        "Промокод",
        max_length=50,
        unique=True
    )

    discount_percent = models.PositiveIntegerField(
        "Скидка (%)"
    )

    is_active = models.BooleanField(
        "Активен",
        default=True
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.code} — {self.discount_percent}%"

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"