from sqlalchemy import and_
from sqlalchemy.orm import Session
from dbase.models.bots import Bots
from schemas.bots import BotsCreate, BotsUpdate


def create_new_bot(bot: BotsCreate, db: Session):
    bot = Bots(**bot.model_dump())
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


def get_bots(owner_id: int, db: Session):
    bots = db.query(Bots).filter(Bots.owner_id == owner_id).all()
    return bots


def get_bot_by_id(bot_id: int, owner_id: int, db: Session):
    bot = db.query(Bots).filter(and_(Bots.id == bot_id, Bots.owner_id == owner_id)).first()
    return bot


def get_bots_by_social_network(owner_id: int, social_network_id: int, db: Session):
    bots = (
        db.query(Bots)
        .filter(and_(Bots.owner_id == owner_id, Bots.social_network_id == social_network_id))
        .all()
    )
    return bots


def update_bot(bot_id: int, bot: BotsUpdate, owner_id: int, db: Session):
    findig_bot = db.query(Bots).filter(and_(Bots.id == bot_id, Bots.owner_id == owner_id)).first()
    if not findig_bot:
        return
    findig_bot.login = bot.login
    findig_bot.password = bot.password
    findig_bot.is_active = bot.is_active
    db.add(findig_bot)
    db.commit()
    return findig_bot
