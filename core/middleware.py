from django.shortcuts import redirect

class UserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for authenticated routes
        if request.path.startswith('/dashboard') and request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/admin/')  # staff users not allowed here
        return self.get_response(request)
