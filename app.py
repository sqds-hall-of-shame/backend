import pytz
from datetime import datetime

# import asqlite
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

import utils
import config


app = FastAPI(debug=config.DEBUG)


@app.get("/messages")
async def get_messages(
    items: int = Query(100, ge=1, le=config.MAX_ITEMS_PER_PAGE),
    page: int = Query(1, ge=1)
):
    all_messages = utils.get_messages()
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


@app.get("/ping")
async def ping():
    return {"message": "pong"}


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