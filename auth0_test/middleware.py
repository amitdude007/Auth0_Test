import requests
from django.conf import settings
from jose import jwt
from django.http import JsonResponse


class Auth0Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization', None)
        if token:
            try:
                payload = self._decode_jwt(token)
                request.auth = payload
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=401)
        return self.get_response(request)

    def get_token_from_header(self, request):
        auth = request.headers.get('Authorization', None)
        if auth:
            parts = auth.split()
            if parts[0].lower() != 'bearer':
                raise ValueError('Authorization header must start with Bearer')
            elif len(parts) == 1:
                raise ValueError('Token not found')
            elif len(parts) > 2:
                raise ValueError('Authorization header must be Bearer token')
            token = parts[1]
            return token
        else:
            return None

    def _decode_jwt(self, token):
        header = jwt.get_unverified_header(token)
        rsa_key = self._get_rsa_key(header)
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=settings.API_IDENTIFIER,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
        return payload

    def _get_rsa_key(self, header):
        jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        return rsa_key
