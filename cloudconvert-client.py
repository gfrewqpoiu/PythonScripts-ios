import asyncio
import pickle
from collections import deque
import sys
if sys.platform == "ios":
    import dialogs
else:
    raise EnvironmentError("This script is written specifically for Pythonista on iOS")

host = "127.0.0.1"
Print = ""

async def get_queue(host: str) -> deque:
    reader, writer = await asyncio.open_connection(host, 8890)
    data = await reader.read()
    queue = pickle.loads(data)
    return queue


async def main():
    global Print
    queue = await get_queue(host)
    Print += "Currently running Job:" + "\n"
    Print += str(queue.popleft()) + "\n"
    Print += "Other Jobs:" + "\n"
    for item in queue:
        Print += (str(item)) + "\n"
    dialogs.text_dialog("Results:", Print)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
