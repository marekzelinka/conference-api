from datetime import datetime

from pydantic import BaseModel


class TalkBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime


class TalkCreate(TalkBase):
    speaker_id: int


class Talk(TalkBase):
    id: int
    speaker_id: int

    class Config:
        orm_mode = True


class SpeakerBase(BaseModel):
    name: str
    bio: str
    company: str


class SpeakerCreate(SpeakerBase):
    pass


class Speaker(SpeakerBase):
    id: int
    talks: list[Talk] = []

    class Config:
        orm_mode = True


class SpeakerWithTalks(Speaker):
    talks: list[Talk]
