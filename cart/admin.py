from django.contrib import admin

from .models import Cart, CartItem, PromoCode


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "size",
        "quantity",
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_percent",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "code",
    )