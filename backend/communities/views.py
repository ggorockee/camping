from rest_framework import viewsets, permissions


from common import permissions as common_perm
from campsites import models as campsite_models  # Campsite 모델 임포트

from . import models, serializers


class ReviewViewSet(viewsets.ModelViewSet):
    """
    특정 캠핑장에 대한 리뷰 CRUD를 위한 ViewSet
    """

    serializer_class = serializers.ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        common_perm.IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        """
        URL에 있는 campsite_pk를 이용해 해당 캠핑장의 리뷰만 필터링.
        """
        # URL로부터 campsite_pk 값을 가져옴. (예: /campsites/1/reviews/ -> 1)
        campsite_pk = self.kwargs["campsite_pk"]
        return models.Review.objects.filter(campsite_id=campsite_pk)

    def perform_create(self, serializer):
        """
        리뷰 생성 시, URL의 campsite와 요청 보낸 user를 자동으로 설정.
        """
        campsite_instance = campsite_models.Campsite.objects.get(
            pk=self.kwargs["campsite_pk"]
        )

        # serializer.save()를 호출할 때 추가적인 데이터를 전달
        serializer.save(user=self.request.user, campsite=campsite_instance)
