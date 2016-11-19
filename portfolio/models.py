# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class PortfolioCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('user'))
    name = models.CharField(_('category'), max_length=50, default='Uncategorized')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(max_length=4096, default='', blank=True, null=True)
    created = models.DateTimeField(_('created'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, auto_now_add=False,
                                   help_text="Please use the following format: <em>YYYY-MM-DD</em>."
                                   )

    def get_absolute_url(self):
        return reverse('portfolio:portfolio_home_by_category', args=[self.slug])

    class Meta:
        ordering = 'name',
        verbose_name = _('portfolio category')
        verbose_name_plural = _('portfolio categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PortfolioCategory, self).save(*args, **kwargs)


def slider_upload_location(slider_images, filename):
    return 'images/%s/%s' % (slider_images.name, filename)


@python_2_unicode_compatible
class PortfolioSliderImage(models.Model):
    name = models.CharField(_('name'), max_length=120, help_text=_('any text you want'))
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to=slider_upload_location,
                              verbose_name=_('image')
                              )
    image_text = models.CharField(_('image text'), max_length=30, blank=True, null=True,
                                  help_text=_('comment 30 characters long'))

    def __str__(self):
        return self.name


def upload_location(instance, filename):
    return 'images/%s/%s' % (instance.category, filename)


@python_2_unicode_compatible
class PortfolioImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('user'))
    category = models.ForeignKey(PortfolioCategory, related_name='image', verbose_name=_('category'),
                                 default='Uncategorized', on_delete=models.PROTECT)
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    width_field = models.IntegerField(_('width field'), default=0)
    height_field = models.IntegerField(_('height field'), default=0)
    image = models.ImageField(null=True,
                              blank=True,
                              width_field='width_field',
                              height_field='height_field',
                              upload_to=upload_location,
                              verbose_name=_('image')
                              )
    description = models.TextField(_('description'), blank=True)
    draft = models.BooleanField(_('draft'), default=False)
    created = models.DateTimeField(_('created'), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, auto_now_add=False,
                                   help_text="Please use the following format: <em>YYYY-MM-DD</em>."
                                   )
    views = models.IntegerField(default=0)

    class Meta:
        ordering = 'name',
        index_together = (('id', 'slug'),)
        verbose_name = _('portfolio image')
        verbose_name_plural = _('portfolio images')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PortfolioImage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:portfolio_image_detail', args=[self.id, self.slug])


@python_2_unicode_compatible
class Feedback(models.Model):
    subject = models.CharField(_('subject'), max_length=250)
    sender = models.EmailField(_('sender'))
    message = models.TextField(_('message'))
    copy = models.BooleanField(_('copy'), default=False)

    def __str__(self):
        return self.sender


def about_me_upload_location(about_me, filename):
    return 'images/%s/%s' % (about_me.title, filename)


@python_2_unicode_compatible
class AboutMe(models.Model):
    title = models.CharField(_('title'), max_length=120, help_text=_('any text you want'))
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to=about_me_upload_location,
                              verbose_name=_('my image')
                              )
    about_me = models.TextField(_('about me'))

    def __str__(self):
        return self.title
