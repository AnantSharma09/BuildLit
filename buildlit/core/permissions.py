from rest_framework.permissions import BasePermission

class IsRole(BasePermission):
  required_role=None
  def has_permission(self, request, view): 
    prof = getattr(request.user, "profile", None) 
  
    return bool(request.user and request.user.is_authenticated and prof and prof.role == self.required_role) 
  

class IsJoiner(IsRole):
  required_role="joiner"


class IsBuilder(IsRole):
  required_role="builder"
