from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TalkBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime


class TalkCreate(TalkBase):
    speaker_id: int


class Talk(TalkBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    speaker_id: int


class SpeakerBase(BaseModel):
    name: str
    bio: str
    company: str


class SpeakerCreate(SpeakerBase):
    pass


class Speaker(SpeakerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    talks: list[Talk] = []


class SpeakerWithTalks(Speaker):
    talks: list[Talk]
