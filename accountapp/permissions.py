import jwt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission





class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthorized')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Login time is expired. Please login again')
        
        return True