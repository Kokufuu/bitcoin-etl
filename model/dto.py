from pydantic import BaseModel


class DTOModel(BaseModel):
    class Config:
        validate_by_name= True
