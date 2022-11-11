from enum import Enum
from typing import Annotated, Union, NamedTuple

from pydantic import BaseModel, validator, Field


class CourseUpdateSchema(BaseModel):
    Category: str
    SubCategory: str
    Tittle: str
    subTittle: str
    Description: str
    language: str
    level: str
    cost: Union[int, float]
    currency: str


class CourseScheme(BaseModel):
    Category: str
    SubCategory: int
    Tittle: str
    subTittle: str
    Description: str
    language: str
    level: str
    cost: Union[int, float]
    currency: str
    CourseActivated: bool
    CourseContentIsNull: bool
    user_id: int
    video: str
    image: str


class Lang(str, Enum):
    id_ID = "id_ID"
    de_DE = "de_DE"
    en_US = "en_US"
    es_ES = "es_ES"
    fr_FR = "fr_FR"
    it_IT = "it_IT"
    nl_NL = "nl_NL"
    pl_PL = "pl_PL"
    pt_BR = "pt_BR"
    ro_RO = "ro_RO"
    tr_TR = "tr_TR"
    ru_RU = "ru_RU"
    th_TH = "th_TH"
    zh_TW = "zh_TW"
    zh_CN = "zh_CN"
    ja_JP = "ja_JP"
    ko_KR = "ko_KR"


class Level(str, Enum):
    proffesional = "proffesional"
    middle = "middle"
    junior = "junior"
    all_levels = "all_levels"


class CourseInScheme(BaseModel):
    Category: str = "Mentor"
    SubCategory: int

    Tittle: Annotated[str, Field(max_length=60)]
    subTittle: Annotated[str, Field(max_length=60)]

    Description: Annotated[str, Field(min_length=200)]
    language: Lang = Lang.ru_RU
    level: Level = Level.all_levels

    cost: Union[int, float] = 0.00
    currency: Annotated[str, Field(max_length=3)] = "som"

    @validator('Subcategory', check_fields=False)
    def name_must_Subcategory_space(cls, v):
        if not len(v):
            raise ValueError('Fields Subcategory is emty!')
        return v

    @validator('language_of_course', check_fields=False)
    def name_must_language_space(cls, v):
        if not len(v):
            raise ValueError('Fields language is emty!')
        return v


class CourseItemFileSchema(BaseModel):
    file: str
    CourseItemId: int
    CourseId: int


class CourseItemSchema(BaseModel):
    Tittle: str
    Description: str
    CourseId: int


class CourseItemSchemaIn(BaseModel):
    Tittle: str
    Description: str
