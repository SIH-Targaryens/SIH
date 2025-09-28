from pydantic import BaseModel

class NTANotification(BaseModel):
    title: str
    url: str
    published_at: str