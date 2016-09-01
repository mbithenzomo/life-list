from rest_framework import permissions


class IsOwnerOrReadOnlyBucketlist(permissions.BasePermission):
    """
    Custom permission to only allow owners of a bucket list to edit or
    delete it. Read only permission for non-owners of the bucket list.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class IsOwnerOrReadOnlyItem(permissions.BasePermission):
    """
    Custom permission to only allow owners of a item to edit or
    delete it. Read only permission for non-owners of the item.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.item_bucketlist.created_by == request.user
