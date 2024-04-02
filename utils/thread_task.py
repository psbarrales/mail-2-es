from threading import Thread, Event as ThreadEvent


def thread_task(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, daemon=True,
                        args=(*args,), kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
