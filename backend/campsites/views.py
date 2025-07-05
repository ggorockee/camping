from rest_framework import viewsets, permissions

from common import permissions as common_perm
from . import models, serializers


class CampsiteViewSet(viewsets.ModelViewSet):
    """
    캠핑장 정보 CRUD를 위한 ViewSet
    - list: 캠핑장 목록 조회
    - retrieve: 캠핑장 상세 정보 조회
    - create: 캠핑장 정보 생성
    - update/partial_update: 캠핑장 정보 수정
    - destroy: 캠핑장 정보 삭제
    """

    queryset = models.Campsite.objects.all()

    # 기본 권한: 인증된 사용자만 쓰기 가능, 읽기는 누구나
    # 추가 권한: IsOwnerOrReadOnly를 통해 객체 소유자만 수정/삭제 가능
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        common_perm.IsOwnerOrReadOnly,
    ]

    # 요청(action)에 따라 다른 serializer를 사용하도록 설정
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.CampsiteListSerializer
        return serializers.CampsiteDetailSerializer

    def perform_create(self, serializer):
        """
        create 요청 시, 현재 로그인된 사용자를 자동으로 owner로 설정.
        """
        serializer.save(owner=self.request.user)
