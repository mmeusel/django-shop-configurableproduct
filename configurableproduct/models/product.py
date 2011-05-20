#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from django.db import models
from shop.models import Product
from django.utils.translation import ugettext_lazy as _

from fields.image_field import ProductImage


class CProduct(Product):
    '''
        A configurable product class, has m2m relations to text, float and boolean fields
    '''
    class Meta(object):
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        app_label = 'configurableproduct'

    type = models.ForeignKey('ProductType', verbose_name=_('Type'), null=False, blank=False)
    char_fields = models.ManyToManyField('ProductCharField', through='ProductChar')
    float_fields = models.ManyToManyField('ProductFloatField', through='ProductFloat')
    boolean_fields = models.ManyToManyField('ProductBooleanField', through='ProductBoolean')
    image_fields = models.ManyToManyField('ProductImageField', through=ProductImage)

    product_fields = [
            'char_fields',
            'float_fields',
            'boolean_fields',
            'image_fields'
    ]

    def save(self, *args, **kwargs):
        super(CProduct, self).save(*args, **kwargs)
        # Create relation for each field in product type
        for field_type in self.product_fields:
            self_field = getattr(self, field_type)
            type_field = getattr(self.type, field_type)
            for tf in type_field.all():
                if not self_field.through.objects.filter(field=tf, product=self).count():
                    pt = self_field.through(product=self, field=tf)
                    pt.save()
