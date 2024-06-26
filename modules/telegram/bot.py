from fastapi import HTTPException, status

from modules.telegram.base import init_bot
from schemas.sending_messages import SendingMessageView


async def send_telegram_message(info: SendingMessageView):
    telegram_bot = init_bot(api_key=info._sender_bot_id.password)
    response_updates = telegram_bot.get_updates(offset=-1)
    if not response_updates:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot {info._sender_bot_id.login} dont have avaible chats",
        )
    for item in response_updates:
        for recipient in info.recipients:
            if item.message.chat.username == recipient:
                telegram_bot.send_message(
                    chat_id=item.message.chat.id,
                    text=info._message_id.subject + '\n' + info._message_id.text,
                )

    return HTTPException(status_code=status.HTTP_200_OK, detail="Succses")
