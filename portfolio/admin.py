from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import PortfolioImage, PortfolioCategory, PortfolioSliderImage, AboutMe


class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(PortfolioCategory, PortfolioCategoryAdmin)


class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated')
    list_filter = ['updated']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = 'created',
    fieldsets = [
                (_('Item'),             {'fields': [('name', 'slug'), 'category']}),
                (_('Medias'),           {'fields': ['image']}),
                (_('Date information'), {'fields': ['created'], 'classes': ['collapse']}),
                (_('Description'),      {'fields': ['description']}),
                (_('Metas'),            {'fields': ['draft']}),
            ]
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(PortfolioImage, PortfolioImageAdmin)


admin.site.register(PortfolioSliderImage)

admin.site.register(AboutMe)
