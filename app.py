import secrets
from typing import Literal

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import utils
import config


class Science(BaseModel):
    metric: str


class User(BaseModel):
    username: str
    display_name: str
    id: str
    avatar: str


class Attachment(BaseModel):
    filename: str
    content_type: str
    id: str
    spoiler: bool
    height: int
    width: int
    content: str


class Message(BaseModel):
    attachments: list[Attachment]
    content: str
    id: str
    timestamp: float
    uploader: User


app = FastAPI(
    debug=config.DEBUG, openapi_url=None if not config.DEBUG else "/openapi.json"
)
app.mount("/cdn", StaticFiles(directory="static"), name="cdn")


@app.get("/", response_class=PlainTextResponse)
async def root() -> (
    Literal[
        "Hey there fellow curious traveller!\n"
        "Looks like you've reached sqd's HOS' API.\n"
        "You can find the documentation here: https://sqdnoises.gitbook.io/the-hos-documentation"
    ]
):

    utils.science("visited_api_/")

    return (
        "Hey there fellow curious traveller!\n"
        "Looks like you've reached sqd's HOS' API.\n"
        "You can find the documentation here: https://sqdnoises.gitbook.io/the-hos-documentation"
    )


@app.get("/.env", response_class=PlainTextResponse)
async def env() -> (
    Literal[
        "# Mmmm this is totally a proper .env file\n"
        'API_KEY="Mmm this a really good API key"\n'
        'Imagine="Being such a noob"\n'
        'Oh="You don\'t need to imagine"'
    ]
):

    utils.science("visited_env")

    return (
        "# Mmmm this is totally a proper .env file\n"
        'API_KEY="Mmm this a really good API key"\n'
        'Imagine="Being such a noob"\n'
        'Oh="You don\'t need to imagine"'
    )


@app.get("/messages", response_class=JSONResponse)
async def get_messages(
    items: int = Query(100, ge=1, le=config.MAX_ITEMS_PER_PAGE),
    page: int = Query(1, ge=1),
):
    all_messages = utils.get_messages().values()
    paginated_messages = utils.paginate(all_messages, items)
    messages = paginated_messages[page - 1 : page][0]

    return {
        "message": "OK",
        "payload": {
            "messages": messages,
            "pages": len(paginated_messages),
            "current_page": page,
        },
    }


@app.get("/messages/pages", response_class=JSONResponse)
async def get_messages(items: int = Query(100, ge=1, le=config.MAX_ITEMS_PER_PAGE)):
    all_messages = utils.get_messages().values()
    paginated_messages = utils.paginate(all_messages, items)

    return {"message": "OK", "payload": {"pages": len(paginated_messages)}}


@app.get("/messages/random")
async def random():
    all_messages = list(utils.get_messages().values())

    return {"message": "OK", "payload": {"message": secrets.choice(all_messages)}}


@app.get("/messages/{message_id}")
async def get_message(message_id: int):
    all_messages = utils.get_messages()

    message = all_messages.get(str(message_id))

    if message:
        return {"message": "OK", "payload": {"message": message}}
    else:
        return JSONResponse(
            {
                "message": "The message with the given ID could not be found.",
                "payload": {"message": None},
            },
            status_code=404,
        )


@app.get("/messages/{message_id}/attachments")
async def get_message_attachments(message_id: int):
    attachments = utils.get_attachments(message_id)

    if attachments:
        return {"message": "OK", "payload": {"attachments": attachments}}
    elif message_id in utils.get_messages():
        return {
            "message": "OK",
            "payload": {"attachments": []},
        }  # No attachments, but the message exists.
    else:
        return JSONResponse(
            {
                "message": "The message with the given ID could not be found.",
                "payload": {"attachments": None},
            },
            status_code=404,
        )


@app.get("/users")
async def get_users():
    all_users = list(utils.get_users().values())
    return {"message": "OK", "payload": {"users": all_users}}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    all_users = utils.get_users()

    user = all_users.get(str(user_id))

    if user:
        return {"message": "OK", "payload": {"user": user}}
    else:
        return JSONResponse(
            {
                "message": "The user with the given ID could not be found.",
                "payload": {"user": None},
            },
            status_code=404,
        )


@app.get("/ping")
async def ping():
    utils.science("pinged")
    return {"message": "pong"}


@app.get("/statistics")
async def get_statistics():
    return utils.get_statistics()


@app.get("/science")
async def science_get():
    utils.science("visited_science")
    return {"message": "OK"}


@app.post("/science")
async def science_post(data: Science):
    utils.science(data.metric)
    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        app if not config.DEBUG else "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
    )
