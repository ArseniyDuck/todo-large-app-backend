from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class CsrfHeaderMiddleware(MiddlewareMixin):
   def process_response(self, request, response):
      if "CSRF_COOKIE" in request.META:
         response["X-CSRFTOKEN"] = get_token(request)
      return response