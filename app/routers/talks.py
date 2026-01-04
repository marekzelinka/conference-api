from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from app import models
from app.db import schema
from app.db.session import SessionDep

router = APIRouter(prefix="/talks", tags=["talks"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.Talk)
async def create_talk(
    *, session: SessionDep, talk: Annotated[models.TalkCreate, Body()]
):
    talk_dict = talk.model_dump()
    db_talk = schema.Talk(**talk_dict)
    session.add(db_talk)
    session.commit()
    session.refresh(db_talk)
    return db_talk


@router.get("/", response_model=list[models.Talk])
async def read_talks(
    *,
    session: SessionDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
):
    talks = session.query(schema.Talk).offset(skip).limit(limit).all()
    return talks


@router.get("/{talk_id}", response_model=models.Talk)
async def read_talk(*, session: SessionDep, talk_id: Annotated[int, Path()]):
    db_talk = session.query(schema.Talk).filter(schema.Talk.id == talk_id).first()
    if not db_talk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Talk not found"
        )
    return db_talk
