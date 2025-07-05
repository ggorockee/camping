from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import serializers


# --- Helper Function ---
def get_tokens_for_user(user):
    """
    사용자에게 새로운 Refresh, Access 토큰을 생성하여 반환
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# --- Views ---


# 1. 회원가입 View (+ 자동 로그인)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # 회원가입은 누구나 접근 가능

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # serializer의 create 메소드가 호출됨

        # 사용자 생성 후, 해당 유저에 대한 토큰 생성
        tokens = get_tokens_for_user(user)

        # response
        response = Response(
            {
                "user": serializer.data,
                "message": "회원가입이 완료되었슴둥",
                "access_token": tokens["access"],  # Access Token은 본문에 포함
            },
            status=status.HTTP_201_CREATED,
        )

        # Refresh Token은 HttpOnly 쿠키에 저장
        response.set_cookie(
            "refresh_token",
            tokens["refresh"],
            httponly=True,
            samesite="Lax",
        )
        return response


# 로그인 View (이전과 동일, Refresh Token을 쿠키에 저장)
class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data["refresh"]
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite="Lax",
            )
            del response.data["refresh"]

        return response


# 토큰 재발급 View (이전과 동일, 쿠키의 Refresh Token 사용)
class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200 and "refresh" in response.data:
            new_refresh_token = response.data["refresh"]
            response.set_cookie(
                "refresh_token",
                new_refresh_token,
                httponly=True,
                samesite="Lax",
            )
            del response.data["refresh"]
        return response


# 로그아웃 View (이전과 동일, 쿠키 삭제)
class LogoutView(APIView):
    def post(self, request):
        response = Response(
            {"message": "로그아웃 되었음둥."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("refresh_token")
        return response


class MyInfoView(generics.RetrieveUpdateAPIView):
    """
    현재 로그인된 사용자의 정보를 조회 및 수정
    GET: 내 정보 조회
    PUT/PATCH: 내 정보 수정
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        # 현재 요청을 보낸 사용자 객체 return
        return self.request.user
