from abc import ABC, abstractmethod
from typing import Any
from users.models import User

class AuthService(ABC):

    @abstractmethod
    def create_session(self, user:User) -> Any:
        pass
    
    @abstractmethod
    def session_to_dict(self, session:Any) -> dict:
        pass