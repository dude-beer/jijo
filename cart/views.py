from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product, ProductSize, Size

from .models import Cart, CartItem, PromoCode


DELIVERY_PRICE = Decimal("1500.00")


@login_required
def cart_detail(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related(
        "product",
        "size",
    ).prefetch_related(
        "product__images"
    )

    subtotal = Decimal("0.00")

    for item in items:
        subtotal += item.subtotal

    # Получаем промокод из сессии
    promo_code_text = request.session.get(
        "promo_code"
    )

    promo = None
    discount = Decimal("0.00")

    if promo_code_text:

        promo = PromoCode.objects.filter(
            code__iexact=promo_code_text,
            is_active=True
        ).first()

        if promo:

            discount = (
                subtotal *
                Decimal(promo.discount_percent) /
                Decimal("100")
            )

    total = subtotal - discount + DELIVERY_PRICE

    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
            "items": items,
            "subtotal": subtotal,
            "promo": promo,
            "discount": discount,
            "delivery_price": DELIVERY_PRICE,
            "total": total,
        }
    )


@login_required
def add_to_cart(request, product_id):

    if request.method != "POST":
        return redirect("catalog:product_detail", slug=get_object_or_404(
            Product,
            id=product_id
        ).slug)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    size_id = request.POST.get("size")
    quantity = int(
        request.POST.get("quantity", 1)
    )

    if not size_id:
        messages.error(
            request,
            "Пожалуйста, выберите размер."
        )

        return redirect(
            "catalog:product_detail",
            slug=product.slug
        )

    stock = get_object_or_404(
        ProductSize,
        product=product,
        size_id=size_id
    )

    if stock.quantity <= 0:
        messages.error(
            request,
            "Этот размер закончился."
        )

        return redirect(
            "catalog:product_detail",
            slug=product.slug
        )

    if quantity < 1:
        quantity = 1

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size_id=size_id,
        defaults={
            "quantity": quantity
        }
    )

    if not created:

        new_quantity = cart_item.quantity + quantity

        if new_quantity > stock.quantity:
            messages.error(
                request,
                f"На складе только {stock.quantity} шт."
            )

            return redirect(
                "catalog:product_detail",
                slug=product.slug
            )

        cart_item.quantity = new_quantity
        cart_item.save()

    messages.success(
        request,
        "Товар добавлен в корзину."
    )

    return redirect("cart:detail")


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Товар удалён из корзины."
    )

    return redirect("cart:detail")


@login_required
def update_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        quantity = int(
            request.POST.get(
                "quantity",
                item.quantity
            )
        )

        if quantity < 1:
            item.delete()

            return redirect("cart:detail")

        stock = ProductSize.objects.filter(
            product=item.product,
            size=item.size
        ).first()

        if stock and quantity > stock.quantity:

            messages.error(
                request,
                f"На складе только {stock.quantity} шт."
            )

            return redirect("cart:detail")

        item.quantity = quantity
        item.save()

    return redirect("cart:detail")


@login_required
def apply_promo(request):

    if request.method == "POST":

        code = request.POST.get(
            "code",
            ""
        ).strip()

        if not code:

            request.session.pop(
                "promo_code",
                None
            )

            messages.info(
                request,
                "Промокод удалён."
            )

            return redirect("cart:detail")

        promo = PromoCode.objects.filter(
            code__iexact=code,
            is_active=True
        ).first()

        if promo:

            request.session["promo_code"] = promo.code

            messages.success(
                request,
                f"Промокод применён. Скидка {promo.discount_percent}%."
            )

        else:

            request.session.pop(
                "promo_code",
                None
            )

            messages.error(
                request,
                "Промокод не найден или больше не действует."
            )

    return redirect("cart:detail")