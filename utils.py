import json
from typing import Callable


def get_messages() -> list[dict]:
    with open("temp/messages.json", encoding="utf-8") as f:
        return json.load(f)

def science(metric: str) -> None:
    with open("temp/science.json", encoding="utf-8") as f:
        science = json.load(f)
    
    science.update({metric: science.get(metric, 0) + 1})
    
    with open("temp/science.json", "w", encoding="utf-8") as f:
        json.dump(science, f, indent=2)

def paginate(array: list | tuple | set, count: int = 100, debug: bool = False, logger: Callable = print) -> list:
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