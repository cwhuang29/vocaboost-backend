from pydantic import BaseModel, constr


class GREWord(BaseModel):
    id: constr(ge=0)
    word: constr(min_length=3, max_length=40)
