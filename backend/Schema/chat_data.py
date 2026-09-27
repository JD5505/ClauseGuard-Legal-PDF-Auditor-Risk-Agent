from pydantic import BaseModel
from uuid import UUID

class CheckInput(BaseModel):
    user_msg: str
    thread_id : UUID
    