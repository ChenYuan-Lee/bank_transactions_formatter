from pydantic.main import BaseModel
from pydantic.types import constr, conint


class Header(BaseModel):
    name: constr(min_length=1) = None
    col_num: conint(ge=0)
