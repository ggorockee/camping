from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "password", "phone_number")

    # def create(self, validated_data):
    #     # ModelSerializer의 create 메소드를 오버라이드하여 비밀번호를 해싱
    #     user = User.objects.create_user(
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #         password=validated_data["password"],
    #         phone_number=validated_data.get("phone_number", ""),
    #     )
    #     return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # API 응답에 포함될 필드 목록
        fields = ("id", "email", "username", "phone_number")
