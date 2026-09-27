from django.contrib import admin
from .models import (Product,ProductImage,ProductSize,Size,Color,Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','hex_code',)
    search_fields = ('name',)
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 4
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'color',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'color', 'is_active',)
    search_fields = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSizeInline]
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main', 'created_at')
    list_filter = ('is_main',)

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity',)
    list_filter = ('size',)
    search_fields = ('product__name',)