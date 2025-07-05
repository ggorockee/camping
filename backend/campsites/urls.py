from django.urls import re_path, path
from . import views

# /api/v1/campsites/

urlpatterns = [
    # path("", views.캠핑장목록조회/등록),
    # path("<int:pk>/", views.캠핑장 상세정보관리),
    # path("<int:pk>/images/", views. API를 통해 백엔드에 전달하여 CampsiteImage 모델에 저장),
    # path("<int:pk>/images/upload-url/", views.Cloudflare로부터 일회성 업로드 URL),
    # path("<int:pk>/sites/", views.특정 캠핑장의 모든 사이트 목록),
    # path("<int:pk>/reviews/", views.특정 캠핑장의 모든 리뷰 목록),
    # path("campsites/", views.내가 소유한 캠핑장 목록),
]
