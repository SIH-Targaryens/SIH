from pydantic import BaseModel

class GATENotification(BaseModel):
    title: str
    url: str
    published_at: str