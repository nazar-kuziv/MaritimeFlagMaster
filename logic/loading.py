from threading import Thread
from collections.abc import Callable

loader_thread: Thread = None

def load_thread(loading_function: Callable):
    global loader_thread
    loader_thread = Thread(target=loading_function, daemon=True)
    loader_thread.start()

def check_thread_active_status() -> bool:
    return (loader_thread and loader_thread.is_alive())