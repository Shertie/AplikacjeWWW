import copy
from rest_framework import permissions

class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

class CanEditOthersPosts(permissions.BasePermission):
    """
    Custom permission to allow owners of an object to edit it.
    Moderators with 'posts.can_edit_others_posts' can also edit.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
            
        # If not owner, check for custom permission
        return request.user.has_perm('posts.can_edit_others_posts')
