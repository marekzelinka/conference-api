from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.db.schema import Speaker, SpeakerCreate, SpeakerPublic, SpeakerPublicWithTalks
from app.db.session import SessionDep

router = APIRouter(prefix="/speakers", tags=["speakers"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SpeakerPublic)
async def create_speaker(
    *, session: SessionDep, speaker: Annotated[SpeakerCreate, Body()]
):
    db_speaker = Speaker.model_validate(speaker)
    session.add(db_speaker)
    session.commit()
    session.refresh(db_speaker)
    return db_speaker


@router.get("/", response_model=list[SpeakerPublic])
async def read_speakers(
    *,
    session: SessionDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
):
    speakers = session.exec(select(Speaker).offset(skip).limit(limit)).all()
    return speakers


@router.get("/{speaker_id}", response_model=SpeakerPublicWithTalks)
async def read_speaker(*, session: SessionDep, speaker_id: Annotated[int, Path()]):
    speaker = session.get(Speaker, speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found"
        )
    return speaker
