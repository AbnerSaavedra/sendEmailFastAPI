from typing import List
from fastapi import BackgroundTasks, FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr


app = FastAPI()

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "ingenieroabnersaavedra@gmail.com",
    MAIL_PASSWORD = "DevChrist77*",
    MAIL_FROM = "ingenieroabnersaavedra@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME= "FastAPI",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
)

app = FastAPI()



@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@app.post("/emailbackground")
async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="Simple background task",
        subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})

'''@app.post("/file")
async def send_file(background_tasks: BackgroundTasks, file_path: str, email: EmailStr) -> JSONResponse:
    with open(file_path, "rb") as f:
    file_data = f.read()
    message = MessageSchema(
    subject="Fastapi mail module",
    recipients=[email],
    body="Simple background task",
    subtype=MessageType.html,
    attachments=[("filename.ext", file_data)])
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
'''
@app.post("/file")
async def send_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    email:EmailStr = Form(...)
    ) -> JSONResponse:

    message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[email],
            body="Simple background task",
            subtype=MessageType.html,
            attachments=[file])

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})

