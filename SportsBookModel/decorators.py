# https://realpython.com/lessons/who-are-you-really/

import functools
import time


def decorator(func):

    # functools.wraps preserves the functions properties after decorating
    #  i.e if you call print(func) it will show func address or using dunder
    #  methods func.__name__
    #  help(func)
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        #  Do something before funct

        # return is here if the function we are passing through returns values
        value = func(*args,**kwargs)

        # do something after
        return value
    return wrapper_decorator



def debug(func):
    """
    https://realpython.com/lessons/debugging-code-decorators/

    Function to debug code when

    Args:
        func (method/function): function which has called the decorator 

    Returns:
        [type]: [description]
    """
    # functools.wraps preserves the functions properties after decorating
    #  i.e if you call print(func) it will show func address or using dunder
    #  methods func.__name__
    #  help(func)
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        #  Do something before funct
        args_repr=[repr(a) for a in args]
        kwargs_repr=[f"{k}={v!r}" for k.v in kwargs.items()]
        signature=", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}"({signature}))
        # return is here if the function we are passing through returns values
        value = func(*args,**kwargs)

        # do something after
        print(f"Calling {func.__name__} return{value!r}")
        return value
    return wrapper_debug
