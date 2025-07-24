from functools import wraps

class UnevaluatedApp:
    __slots__ = ["__func", "__args", "__kwargs","__evaluated", "__result"]
    def __init__(self, func, args, kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__evaluated = False
        self.__result = None

    @property
    def result(self):
        if not self.__evaluated:
            self.__result = self.__func(*self.__args, **self.__kwargs)
            self.__evaluated = True
        return self.__result

def pull(arg):
    while isinstance(arg, UnevaluatedApp):
        arg = arg.result
    return arg

def tail_call(func, *args, **kwargs):
    return UnevaluatedApp(func, args, kwargs)

def tramp(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        return pull(func(*args, **kwargs))

    return wrapped_func


def tail(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        return tail_call(func, *args, **kwargs)

    return wrapped_func
