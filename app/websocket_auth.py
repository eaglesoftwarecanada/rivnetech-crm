from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user(token):
    auth = JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(token)
        return auth.get_user(validated_token)
    except Exception as e:
        return AnonymousUser()


class WebSocketTokenAuthMiddleware:
    """Authentication for WebSockets """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """ Get user if is token else anonymous  """
        if scope['subprotocols']:
            token = scope['subprotocols'][0]
            if token:
                scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)
