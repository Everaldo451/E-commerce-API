from abc import ABC, abstractmethod
from typing import Any

class AuthService(ABC):

    @abstractmethod
    def create_session(self, user) -> Any:
        pass
    
    @abstractmethod
    def session_to_dict(self, session:Any) -> dict:
        pass