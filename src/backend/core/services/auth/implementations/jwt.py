from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from backend.core.services.auth.base import AuthService


class JWTAuthService(AuthService):

    def create_session(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return {
            'access_token': access_token, 
            'refresh_token': refresh_token
        }
    
    def get_token_data(self, token:UntypedToken):
        return {
            'value': str(token),
            'lifetime': token.lifetime.total_seconds()
        }
    
    def session_to_dict(self, session):
        access_token = self.get_token_data(session.get('access_token'))
        refresh_token = self.get_token_data(session.get('refresh_token'))
        return {
            'tokens': {
                'access_token': access_token, 
                'refresh_token': refresh_token
            }
        }