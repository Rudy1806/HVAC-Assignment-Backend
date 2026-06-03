from urllib.parse import urlparse


class LocalDevCorsMiddleware:
    allowed_hosts = {
        'localhost',
        '127.0.0.1',
    }

    allowed_ports = {'5173', '5174'}

    allowed_headers = 'Accept, Authorization, Content-Type, Origin, X-Requested-With'
    allowed_methods = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS':
            response = self._build_preflight_response(origin)
            if response is not None:
                return response

        response = self.get_response(request)
        self._add_cors_headers(response, origin)
        return response

    def _is_allowed_origin(self, origin):
        if not origin:
            return False

        parsed_origin = urlparse(origin)
        if parsed_origin.scheme != 'http':
            return False

        if parsed_origin.port and str(parsed_origin.port) not in self.allowed_ports:
            return False

        host = parsed_origin.hostname
        if host in self.allowed_hosts:
            return True

        if host and host.startswith('192.168.'):
            return True

        if host and host.startswith('10.'):
            return True

        if host and host.startswith('172.'):
            second_octet = host.split('.')[1]
            if second_octet.isdigit() and 16 <= int(second_octet) <= 31:
                return True

        return False

    def _build_preflight_response(self, origin):
        if not self._is_allowed_origin(origin):
            return None

        from django.http import HttpResponse

        response = HttpResponse(status=200)
        self._add_cors_headers(response, origin)
        return response

    def _add_cors_headers(self, response, origin):
        if self._is_allowed_origin(origin):
            response['Access-Control-Allow-Origin'] = origin
            response['Vary'] = 'Origin'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = self.allowed_headers
            response['Access-Control-Allow-Methods'] = self.allowed_methods
