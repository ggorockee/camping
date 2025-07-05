from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


import requests

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


class ImageUploadURLView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/images/v2/direct_upload"
        # 인증 헤더
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
        }

        try:
            # Cloudflare에 일회용 업로드 URL 요청
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킴

            data = response.json()

            if data.get("success"):
                # 프론트엔드에 필요한 정보만 담아 전달
                return Response(data["result"])
            else:
                return Response({"errors": data.get("errors")}, status=400)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
