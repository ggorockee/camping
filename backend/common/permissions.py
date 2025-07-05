from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만 수정할 수 있도록 허용하는 커스텀 권한입니다.
    읽기(GET, HEAD, OPTIONS) 요청은 누구나 허용합니다.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 대해 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 객체의 소유자(owner)에게만 허용
        return obj.owner == request.user
