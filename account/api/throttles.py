from rest_framework.throttling import SimpleRateThrottle


# could be AnonRateThrottle, UserRateThrottle
class RegisterThrottle(SimpleRateThrottle):
    scope = 'register_throttle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == 'GET':
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }
