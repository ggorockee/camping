from rest_framework import viewsets

from . import models, serializers


class CampsiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    캠핑장 정보 조회를 위한 ViewSet
    - list: 캠핑장 목록 조회
    - retrieve: 캠핑장 상세 정보 조회
    """

    queryset = models.Campsite.objects.all()

    # 요청(action)에 따라 다른 serializer를 사용하도록 설정
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.CampsiteListSerializer
        return serializers.CampsiteDetailSerializer
