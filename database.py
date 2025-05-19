from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    photo_url: Optional[str]
    auth_date: int