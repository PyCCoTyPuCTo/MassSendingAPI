from sqlalchemy.orm import Session

from dbase.models.bots import Bots
from dbase.models.message import Message
from dbase.models.sending_messages import SendingMessages
from schemas.message import MessageCreate
from schemas.sending_messages import SendMessageCreate


def get_send_messages_by_owner(owner_id: int, db: Session):
    messages = (
        db.query(SendingMessages)
        .filter(SendingMessages.sender_bot_id == Bots.id)
        .filter(Bots.owner_id == owner_id)
        .all()
    )
    for item in messages:
        item.id_message = item._message_id
        item.sender_bot_id = item._sender_bot_id
    return messages


def get_message(id_message: int, db: Session):
    message = db.query(Message).filter(Message.id == id_message).first()
    return message


def add_message(new_message: MessageCreate, db: Session):
    message = Message(**new_message.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def add_sended_message(message: SendMessageCreate, db: Session):
    send_message = SendingMessages(**message.model_dump())
    db.add(send_message)
    db.commit()
    db.refresh(send_message)
    return send_message
