from django.contrib import admin


from . import models


@admin.register(models.Campsite)
class CampsiteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CampsiteImage)
class CampsiteImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CampsiteAmenity)
class CampsiteAmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Policy)
class PolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    pass
