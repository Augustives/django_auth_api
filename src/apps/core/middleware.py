from django.http import HttpResponse
from health_check.views import MainView


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health-check/":
            health_check_view = MainView.as_view()
            response = health_check_view(request)

            if hasattr(response, "render") and callable(response.render):
                response = response.render()

            return response

        return self.get_response(request)
