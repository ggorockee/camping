from django.db import models
from django.conf import settings
from common.models import BaseModel


class Review(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    campsite = models.ForeignKey(
        "campsites.Campsite", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()  # 1~5점
    content = models.TextField()

    def __str__(self):
        # 예: "꼬록키 캠핑장 - ggorockee님의 리뷰 (5점)" 형식으로 표시
        return f"{self.campsite.name} - {self.user}'s Review ({self.rating} stars)"
