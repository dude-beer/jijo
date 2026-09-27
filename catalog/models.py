from django.db import models

class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True, blank=True)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField('Размер', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    hex_code = models.CharField('HEX', max_length=7, default='#000000')
    
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    slug = models.SlugField('Slug', max_length=100, unique=True)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='products', verbose_name='Цвет')
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sizes = models.ManyToManyField(Size, through='ProductSize', related_name='products', verbose_name='Размеры')
    is_active = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Дата добавления',auto_now_add=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    @property
    def main_image(self):
        return (self.images.filter(is_main=True).first()
                or self.images.first())
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField('Фото', upload_to='products/%Y/%m')
    is_main = models.BooleanField('Главное фото', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
        ordering = ["is_main", "created_at"]
        
    def __str__(self):
        return f"Фото {self.product.name}"
    
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_items', verbose_name='Товар')
    size = models.ForeignKey(Size, on_delete=models.PROTECT, related_name='stock_items', verbose_name='Размер')
    quantity = models.PositiveIntegerField('Количество на складе', default=0)
    class Meta:
        verbose_name = "Размер товара"
        verbose_name_plural = "Размеры товаров"
        
        constraints = [models.UniqueConstraint(
            fields=['product', 'size'],
            name = 'unique_product_size'
        )]
        
    def __str__(self):
        return f"{self.product.name} - {self.size.name}: {self.quantity} шт."