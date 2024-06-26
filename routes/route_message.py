import csv
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from dbase.datebase import get_db
from dbase.models.users import User
from dbase.repository.bot import get_bot_by_id
from dbase.repository.message import (
    add_message,
    add_sended_message,
    get_send_messages_by_owner,
)
from modules.dispancer import send_info_for_bots
from routes.route_user import get_current_user
from schemas.message import MessageCreate
from schemas.sending_messages import SendMessageCreate, SendingMessageView

route = APIRouter(prefix="/message", tags=["message"])

@route.get(
    "/all", response_model=list[SendingMessageView], status_code=status.HTTP_200_OK
)
def get_all_messages_by_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    messages = get_send_messages_by_owner(owner_id=current_user.id, db=db)
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sending messages from user {current_user.id} not found",
        )
    return messages

@route.post("/send")
async def send_post(
    sending_bots: Annotated[list[int], Query()],
    input_subject: str = Form(max_length=20),
    input_message: str = Form(max_length=1000),
    recipients_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bots = []
    for id_bots in sending_bots:
        bots.append(get_bot_by_id(bot_id=id_bots, owner_id=current_user.id, db=db))
    if not recipients_file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Download no csv file"
        )

    new_message = MessageCreate(subject=input_subject, text=input_message)
    prepared_message = add_message(new_message=new_message, db=db)
    contents = await recipients_file.read()
    csv_data = contents.decode("utf-8").splitlines()
    csv_reader = csv.DictReader(csv_data)
    sended_message = []
    for bot in bots:
        recipients = []
        for row in csv_reader:
            if bot.social_network_id == int(row["network"]):
                recipients.append(row["recipient"])
        if recipients:
            new_senders = SendMessageCreate(
                id_message=prepared_message.id,
                sender_bot_id=bot.id,
                recipients=recipients,
            )
            sended_message.append(add_sended_message(message=new_senders, db=db))
        csv_reader = csv.DictReader(csv_data)
    response = await send_info_for_bots(sended_message, current_user, db)
    return response
