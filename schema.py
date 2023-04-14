from typing import Optional, Type

import pydantic

from errors import HttpError


class CreateAnnounce(pydantic.BaseModel):

    title: str
    description: str
    author: str


class PatchAnnounce(pydantic.BaseModel):

    title: Optional[str]
    description: Optional[str]
    author: Optional[str]


def validate(input_data: dict, validation_model: Type[CreateAnnounce] | Type[PatchAnnounce]):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())
