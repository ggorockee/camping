from django.db import models
from django.conf import settings

from common.models import BaseModel


# Create your models here.
class Campsite(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campsites"
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True)
    blog_url = models.URLField(blank=True)
    layout_image_url = models.URLField(blank=True)  # 사이트 배치도 이미지


class CampsiteImage(BaseModel):
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="images"
    )
    cloudflare_id = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)


class Site(BaseModel):
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="sites"
    )
    name = models.CharField(max_length=50)  # 예: A1, B5
    camp_type = models.CharField(max_length=50)  # 예: 오토캠핑, 글램핑
    base_price = models.DecimalField(max_digits=10, decimal_places=2)


class Amenity(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    icon_url = models.URLField(blank=True)


class CampsiteAmenity(BaseModel):
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)


class Policy(BaseModel):  # OneToOneField로 변경
    campsite = models.OneToOneField(
        Campsite, on_delete=models.CASCADE, related_name="policy"
    )
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    manner_time_start = models.TimeField()
    manner_time_end = models.TimeField()


class PricingRule(BaseModel):  # 요금 정책
    campsite = models.ForeignKey(
        Campsite, on_delete=models.CASCADE, related_name="pricing_rules"
    )
    name = models.CharField(max_length=100)  # 예: 주말/성수기 요금
    start_date = models.DateField()
    end_date = models.DateField()
    # 0=월요일, 1=화요일... 6=일요일
    day_of_week = models.CharField(
        max_length=15, blank=True, help_text="쉼표로 구분된 요일(0-6)"
    )
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2)  # 추가 요금
