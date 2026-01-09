from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated

class UserInput(BaseModel):
    new_string:Annotated[str,Field(...,max_length=20000,description='Enter the news body here')]