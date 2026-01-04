from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class SpeakerBase(SQLModel):
    name: str = Field(index=True)
    bio: str
    company: str


class Speaker(SpeakerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    talks: list[Talk] = Relationship(back_populates="speaker")


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerPublic(SpeakerBase):
    id: int


class SpeakerPublicWithTalks(SpeakerPublic):
    talks: list[Talk] = []


class SpeakerUpdate(SQLModel):
    name: str | None = None
    bio: str | None = None
    company: str | None = None


class TalkBase(SQLModel):
    title: str = Field(index=True)
    description: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime = Field(default_factory=datetime.now)

    speaker_id: int | None = Field(default=None, foreign_key="speaker.id")


class Talk(TalkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    speaker: Speaker | None = Relationship(back_populates="talks")


class TalkCreate(TalkBase):
    pass


class TalkPublic(TalkBase):
    id: int


class TalkPublicWithSpeaker(TalkPublic):
    speaker: Speaker | None = None


class TalkUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    speaker_id: int | None = None
