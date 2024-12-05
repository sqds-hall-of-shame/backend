import os
import json
import config
from typing import Any, Callable


def get_messages() -> dict[str, dict]:
    with open(f"{config.DATABASE_STORAGE}/messages.json") as f:
        messages = json.load(f)

    users = get_users()
    for id in messages:
        messages[id]["uploader"] = users[messages[id]["uploader"]["id"]]

    return messages


def get_users() -> dict[str, dict]:
    with open(f"{config.DATABASE_STORAGE}/users.json") as f:
        return json.load(f)


def get_attachments(id: int) -> dict[str, dict] | None:
    filename = f"{id}.json"

    if filename in os.listdir(f"{config.DATABASE_STORAGE}/messages"):
        with open(f"{config.DATABASE_STORAGE}/messages/{filename}") as f:
            return json.load(f).get("attachments")


def get_statistics() -> dict[str, Any]:
    with open(f"{config.DATABASE_STORAGE}/statistics.json") as f:
        return json.load(f)


def science(metric: str) -> None:
    with open(f"{config.DATABASE_STORAGE}/science.json", encoding="utf-8") as f:
        science = json.load(f)

    science.update({metric: science.get(metric, 0) + 1})

    with open(f"{config.DATABASE_STORAGE}/science.json", "w", encoding="utf-8") as f:
        json.dump(science, f, indent=2)


def paginate(
    array: list | tuple | set,
    count: int = 100,
    debug: bool = False,
    logger: Callable = print,
) -> list:
    """Efficient paginator for making a multiple lists out of a list which are sorted in a page-vise order.

    For example:
    ```py
    >>> abc = [1, 2, 3, 4, 5]
    >>> print(paginate(abc, count=2)
    [[1, 2], [3, 4], [5]]
    ```

    That was just the basic usage. By default the count variable is set to 100.
    """
    array = list(array)
    paginated = []

    temp = []
    for item in array:
        if len(temp) == count:
            paginated.append(temp)
            temp = []

        temp.append(item)

        if debug:
            logger(len(temp), item)

    if len(temp) > 0:
        paginated.append(temp)

    return paginated
