from tkinter.constants import CASCADE

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=50)
    sku = models.CharField(verbose_name=_("stock keeping unit"),
                           max_length=20, validators=[validate_sku], db_index=True)
    description = models.TextField(verbose_name=_("description"), blank=True)
    avatar = models.ImageField(verbose_name=_("avatar"), blank=True, upload_to="packages/")
    is_enable = models.BooleanField(verbose_name=_("is enable"), default=True)
    price = models.PositiveIntegerField(verbose_name=_("price"))
    duration = models.DurationField(verbose_name=_("duration"), blank=True, null=True)
    # gateway = models.ManyToManyField(verbose_name=_("gateway"), to="payments.Gateway")
    created_time = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_("updated time"), auto_now=True)

    class Meta:
        db_table = "packages"
        verbose_name = _("package")
        verbose_name_plural = _("packages")

class Subscription(models.Model):
    user = models.ForeignKey(verbose_name=_("user"), to=User, related_name='subscriptions', on_delete=models.CASCADE)
    package = models.ForeignKey(verbose_name=_("package"),
                                to=Package, related_name='subscriptions', on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name=_("created time"), auto_now_add=True)
    expire_time = models.DateTimeField(verbose_name=_("expire time"), blank=True, null=True)

    class Meta:
        db_table = "subscriptions"
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")