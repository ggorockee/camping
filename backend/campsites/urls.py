from django.urls import re_path, path, include
from rest_framework_nested import routers
from . import views
from communities import views as commu_views


# /api/v1/campsites/
# DefaultRouter를 생성
router = routers.DefaultRouter()


# 'campsites'라는 경로에 CampsiteViewSet을 등록
router.register(
    prefix="",
    viewset=views.CampsiteViewSet,
    basename="campsite",
)

# 2. 'campsites' 라우터에 중첩될 'reviews' 라우터를 생성.
#    parent_prefix를 ""로 수정합니다.
reviews_router = routers.NestedDefaultRouter(
    parent_router=router,
    parent_prefix="",
    lookup="campsite",
)
reviews_router.register(
    prefix="reviews",
    viewset=commu_views.ReviewViewSet,
    basename="campsite-reviews",
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(reviews_router.urls)),
    # path("<int:pk>/images/", views. API를 통해 백엔드에 전달하여 CampsiteImage 모델에 저장),
    # path("<int:pk>/images/upload-url/", views.Cloudflare로부터 일회성 업로드 URL),
    # path("<int:pk>/sites/", views.특정 캠핑장의 모든 사이트 목록),
    # path("<int:pk>/reviews/", views.특정 캠핑장의 모든 리뷰 목록),
    # path("campsites/", views.내가 소유한 캠핑장 목록),
]
