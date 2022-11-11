from typing import List, Optional, Union, Dict
from jinja2 import Environment, select_autoescape, FileSystemLoader
from starlette import status
from schema.ResetPasswordSchema import TemplateCorfirmSzhema
from .config import config
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from starlette.responses import JSONResponse


env = Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape(['html', 'xml']))


conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME", default=""),
    MAIL_PASSWORD=config("MAIL_PASSWORD", default=""),
    MAIL_FROM=config("MAIL_FROM", default=""),
    MAIL_PORT=int(config("MAIL_PORT", default="")),
    MAIL_SERVER=config("MAIL_SERVER", default=""),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_to_email(subject: str, recipients: List[str], data: TemplateCorfirmSzhema = None, subtype: str = "html"):
    try:
        HOST = config("HOST")
        PORT = config("PORT")
        template = env.get_template('confirmEmail.html')
        html = template.render(first_name=data.firstname, url_confirm=data.url_confirm, HOST=f"{HOST}:{PORT}/")
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            subtype=subtype,
            html=html
        )
        rf = FastMail(conf)
        await rf.send_message(message)
        return JSONResponse(status_code=200,
                            content={"message": f"Ссылка восстановление отправлено на {recipients[0]}"})
    except ConnectionError as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Что то пошло не так с сервером. Повторите позже."})
