from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey(verbose_name=_('parent'), to='self', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    title = models.CharField(verbose_name=_('title'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, null=True, upload_to='categories/')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('-created_time',)
        indexes = [
            models.Index(fields=['title', '-created_time'])
        ]

    def __str__(self):
        return self.title


class Product(models.Model):
    categories = models.ManyToManyField(verbose_name=_('categories'), to='Category',
                                        blank=True, related_name='products')
    title = models.CharField(verbose_name=_('title'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, null=True, upload_to="products/")
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('product')
        verbose_name_plural = _("'products'")
        ordering = ('-created_time',)
        indexes = [models.Index(fields=['title', '-created_time'])]

    def __str__(self):
        return self.title


class File(models.Model):
    products = models.ForeignKey(verbose_name=_('products'), to='Product',
                                 on_delete=models.CASCADE, related_name="files")
    title = models.CharField(verbose_name=_('title'), max_length=50)
    file = models.FileField(verbose_name=_('file'), upload_to='file/%Y/%m/%d/')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _("'files'")
        ordering = ('-created_time',)
        indexes = [models.Index(fields=['title', '-created_time'])]

    def __str__(self):
        return self.title