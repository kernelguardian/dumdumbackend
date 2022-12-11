from pydantic import BaseModel, AnyUrl


class URL(BaseModel):
    url: AnyUrl
