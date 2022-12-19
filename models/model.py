from pydantic import BaseModel, AnyUrl


class URL(BaseModel):
    url: str
    user_query: str | None


class UserQuery(URL):
    user_query: str
