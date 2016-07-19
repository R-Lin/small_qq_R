import re

def deco(function):
    def inner(*args, **kwargs):
        function(*args, **kwargs)
    return inner

@deco
def f(*args, **kwargs):
    print str(args)[1:-1]
    print ' '.join(map(lambda x : str(x),args))

f('1', '2', {'a': 2})
