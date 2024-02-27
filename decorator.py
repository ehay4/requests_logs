import functools
import logging
import requests
import types

logging.basicConfig(filename = 'logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_function_call(func):
    """Decorator to log function calls and responses."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logging.info(f"Calling {func.__name__} with args {signature}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper

def decorate_module_functions(module, decorator):
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if callable(attribute):
            # Decorate the callable if it's a function or a method in the module
            if isinstance(attribute, types.FunctionType) or isinstance(attribute, types.MethodType):
                decorated_attribute = decorator(attribute)
                setattr(module, attribute_name, decorated_attribute)

# Apply the decorator to all callables in the requests module
decorate_module_functions(requests, log_function_call)

def clear_log_file():
    with open('logs.txt', 'w'):
        pass

clear_log_file()

response = requests.get('https://docs.google.com/spreadsheets/d/1fJSZn1Ww0tSoeifcvegJW8_bshJh-FZdWJvN3HZtyhU/edit#gid=0')

