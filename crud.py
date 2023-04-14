from sqlalchemy.orm import Session

from errors import HttpError


def get_announce(session: Session, Announce, announce_id: int):
    announce = session.get(Announce, announce_id)
    if announce is None:
        raise HttpError(404, 'announce not found')
    return announce


def create_announce(session: Session, Announce, json_data):
    new_announce = Announce(**json_data)
    session.add(new_announce)
    session.commit()
    return new_announce


def patch_announce(session: Session, announce, json_data):
    for field, value in json_data.items():
        setattr(announce, field, value)
    session.add(announce)
    session.commit()
    return announce


def delete_announce(session: Session, announce):
    session.delete(announce)
    session.commit()
