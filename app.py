import secrets
from datetime import datetime

# import asqlite
import pytz
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import utils
import config

class Science(BaseModel):
    metric: str


app = FastAPI(debug=config.DEBUG, openapi_url=None)
app.mount("/cdn", StaticFiles(directory="static"), name="cdn")


@app.get("/")
async def root():
    utils.science("visited_api_/")
    return PlainTextResponse("Hey there fellow curious traveller!\n"
                             "Looks like you've reached sqd's HOS' API.\n"
                             "You can find the documentation here: https://sqdnoises.gitbook.io/the-hos-documentation")


@app.get("/.env")
async def root():
    utils.science("visited_env")
    return PlainTextResponse("# Mmmm this is totally a proper .env file\n"
                             'API_KEY="Mmm this a really good API key"\n'
                             'Imagine="Being such a noob"\n'
                             'Oh="You don\'t need to imagine"')


@app.get("/messages")
async def get_messages(
    items: int = Query(100, ge=1, le=config.MAX_ITEMS_PER_PAGE),
    page: int = Query(1, ge=1)
):
    all_messages = utils.get_messages().values()
    paginated_messages = utils.paginate(all_messages, items)
    messages = paginated_messages[page-1:page]
    
    return {
        "message": "OK",
        "payload": {
            "messages": messages
        }
    }


@app.get("/messages/{message_id}")
async def get_message(message_id: int):
    all_messages = utils.get_messages()
    
    message = all_messages.get(str(message_id))

    if message:
        return {"message": "OK", "payload": {"message": message}}
    else:
        return JSONResponse({"message": "The message with the given ID could not be found.",
                             "payload": {"message": None}}, status_code=404)


@app.get("/messages/{message_id}/attachments")
async def get_message_attachments(message_id: int):
    attachments = utils.get_attachments(message_id)
    
    if attachments:
        return {"message": "OK", "payload": {"attachments": attachments}}
    elif message_id in utils.get_messages():
        return {"message": "OK", "payload": {"attachments": []}}  # No attachments, but the message exists.
    else:
        return JSONResponse({"message": "The message with the given ID could not be found.",
                             "payload": {"attachments": None}}, status_code=404)


@app.get("/users")
async def get_users(avatar: bool):
    all_users = utils.get_users().values()
    
    if not avatar:
        for user in all_users:
            del user["avatar"]
    
    return {"message": "OK", "payload": {"users": all_users}}


@app.get("/users/{user_id}")
async def get_user(user_id: int, avatar: bool):
    all_users = utils.get_users()
    
    user = all_users.get(str(user_id))
    if avatar:
        del user["avatar"]
    
    if user:
        return {"message": "OK", "payload": {"user": user}}
    else:
        return JSONResponse({"message": "The user with the given ID could not be found.",
                             "payload": {"user": None}}, status_code=404)


@app.get("/users/{user_id}/avatar")
async def get_user_avatar(user_id: int):
    all_users = utils.get_users()
    
    user = all_users.get(str(user_id))
    
    if user:
        return {"message": "OK", "payload": {"avatar": user["avatar"]}}
    else:
        return JSONResponse({"message": "The user with the given ID could not be found.",
                             "payload": {"user": user["avatar"]}}, status_code=404)


@app.get("/messages/{message_id}")
async def get_message(message_id: int):
    all_messages = utils.get_messages()
    
    message = None
    for msg in all_messages:
        if msg["id"] == message_id:
            message = msg
            break

    if message:
        return {"message": "OK", "payload": {"message": message}}
    else:
        return JSONResponse({"message": "The message with the given ID could not be found.",
                             "payload": {"message": None}}, status_code=404)


@app.get("/random")
async def random():
    all_messages = utils.get_messages()
    
    return {
        "message": "OK",
        "payload": {
            "message": secrets.choice(all_messages)
        }
    }


@app.get("/ping")
async def ping():
    utils.science("pinged")
    return {"message": "pong"}


@app.get("/science")
async def science_get():
    utils.science("visited_science")
    return {"message": "OK"}


@app.post("/science")
async def science_post(data: Science):
    utils.science(data.metric)
    return {"message": "OK"}


@app.get("/statistics")
async def get_statistics():
    last_update_time = datetime.now(pytz.UTC).timestamp()
    return {"last_database_update": int(last_update_time)}


if __name__ == "__main__":
    uvicorn.run(
        app if not config.DEBUG else "app:app",
        host=config.HOST, port=config.PORT,
        reload=config.DEBUG
    )