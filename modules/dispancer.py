from requests import Session
from dbase.models.users import User
from dbase.repository.bot import get_bot_by_id
from modules.emails.bot import send_smtp_email
from modules.telegram.bot import send_telegram_message
from schemas.sending_messages import SendingMessageView


async def send_info_for_bots(message_info: list[SendingMessageView], current_user: User, db: Session):
    if not message_info:
        return
    for info in message_info:
        bot = get_bot_by_id(info.sender_bot_id, current_user.id, db)
        if bot.social_network_id == 1:
            response = await send_smtp_email(info)
        elif bot.social_network_id == 2:
            response = await send_telegram_message(info)

    return response
