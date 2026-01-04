from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from app import models
from app.db import schema
from app.db.session import SessionDep

router = APIRouter(prefix="/speakers", tags=["speakers"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.Speaker)
async def create_speaker(
    *, session: SessionDep, speaker: Annotated[models.SpeakerCreate, Body()]
):
    speaker_dict = speaker.model_dump()
    db_speaker = schema.Speaker(**speaker_dict)
    session.add(db_speaker)
    session.commit()
    session.refresh(db_speaker)
    return db_speaker


@router.get("/", response_model=list[models.Speaker])
async def read_speakers(
    *,
    session: SessionDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
):
    speakers = session.query(schema.Speaker).offset(skip).limit(limit).all()
    return speakers


@router.get("/{speaker_id}", response_model=models.SpeakerWithTalks)
async def read_speaker(*, session: SessionDep, speaker_id: Annotated[int, Path()]):
    db_speaker = (
        session.query(schema.Speaker).filter(schema.Speaker.id == speaker_id).first()
    )
    if not db_speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found"
        )
    return db_speaker
