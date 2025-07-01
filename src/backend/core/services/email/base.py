from abc import ABC, abstractmethod
from typing import List, Literal, TypedDict

ContentType = Literal["text/plain", "text/html"]

class EmailContentPart(TypedDict):
    content_type: ContentType
    content: str

class EmailService(ABC):

    @abstractmethod
    def send_email(
        self, 
        subject, 
        content, 
        from_email, 
        to:List[str], 
        content_type:ContentType
    ) -> None:
        pass

    @abstractmethod
    def send_multipart_email(
        self, 
        subject, 
        from_email, 
        to:List[str], 
        content:List[EmailContentPart]
    ) -> None:
        pass