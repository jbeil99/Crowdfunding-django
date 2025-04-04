class LoginCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Accessible non-auth endpoints
        public_paths = ['/api/register/', '/api/activate/', '/api/token/', '/api/token/refresh/']
        
        # Check if the request is for a protected resource and if the user is not active
        if not any(request.path.startswith(path) for path in public_paths):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                from rest_framework_simplejwt.authentication import JWTAuthentication
                jwt_auth = JWTAuthentication()
                try:
                    validated_token = jwt_auth.get_validated_token(auth_header.split(' ')[1])
                    user = jwt_auth.get_user(validated_token)
                    if not user.is_active:
                        from django.http import JsonResponse
                        return JsonResponse(
                            {"detail": "Account is not activated."},
                            status=403
                        )
                except:
                    pass

        response = self.get_response(request)
        return response