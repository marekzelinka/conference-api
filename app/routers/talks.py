from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlmodel import select

from app.db.schema import Talk, TalkCreate, TalkPublic, TalkPublicWithSpeaker
from app.db.session import SessionDep

router = APIRouter(prefix="/talks", tags=["talks"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TalkPublic)
async def create_talk(*, session: SessionDep, talk: Annotated[TalkCreate, Body()]):
    db_talk = Talk.model_validate(talk)
    session.add(db_talk)
    session.commit()
    session.refresh(db_talk)
    return db_talk


@router.get("/", response_model=list[TalkPublic])
async def read_talks(
    *,
    session: SessionDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
):
    talks = session.exec(select(Talk).offset(skip).limit(limit)).all()
    return talks


@router.get("/{talk_id}", response_model=TalkPublicWithSpeaker)
async def read_talk(*, session: SessionDep, talk_id: Annotated[int, Path()]):
    talk = session.get(Talk, talk_id)
    if not talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Talk not found"
        )
    return talk
