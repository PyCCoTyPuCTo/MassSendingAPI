from fastapi import HTTPException, status


from modules.emails.base import create_email_message, get_stmp_conn, get_stmp_ssl_conn
from schemas.sending_messages import SendingMessageView

async def send_smtp_email(info: SendingMessageView):
    email = info._sender_bot_id
    message = create_email_message(info)
    if "gmail.com" in email.login:
        try:
            server = get_stmp_conn("smtp.gmail.com", email.login, email.password)
            server.send_message(message)
            server.quit()
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}"
            ) from e
        finally:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Succses"
            )
    elif "mail.ru" in email.login:
        try:
            server = get_stmp_ssl_conn("smtp.mail.ru", email.login, email.password)
            server.send_message(message)
            server.quit()
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}"
            ) from e
        finally:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Succses"
            )
