import sys
import builtins
from pprint import pprint

from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager


def get_object_or_null(model, **kwargs):
    if isinstance(model, QuerySet) or isinstance(model, BaseManager):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()




# # for import
# from analizetools.analize import (
#     p_dir, p_mro, p_glob, p_loc, p_type,
#     delimetr, p_content, show_builtins, show_doc,
# )

# p_dir, p_mro, p_glob, p_loc, p_content, show_builtins, show_doc, delimiter


def p_dir(obj):
    return pprint(dir(obj))


def p_mro(obj):
    if isinstance(obj, type):
        return pprint(obj.mro())
    return pprint(type(obj).mro())


def p_glob():
    return pprint(globals())


def p_loc():
    return pprint(locals())


def p_content(obj):
    if hasattr(obj, '__iter__'):
        return pprint(obj)
    return pprint("Can't show elements of obj")


def show_builtins():
    # import builtins
    # pp(dir(builtins) == dir(globals()['__builtins__'])) # True
    # pp(builtins == globals()['__builtins__']) # True
    # pp(type(builtins)) # <class 'module'>
    # pp(type(builtins).mro()) # [<class 'module'>, <class 'object'>]
    key_builtins = globals().get('__builtins__')
    if key_builtins:
        if isinstance(key_builtins, dict):
            return pprint(key_builtins)
        return pprint(dir(key_builtins))
    else:
        return pprint("Can't show builtins")


def show_doc(obj):
    return print(obj.__doc__)


def delimiter(sym='-+', quant=50):
    return print('\n', sym * quant, end='\n')


# потом можно улучшить чтобы передавался также **kwargs, и тогда выводился
# также имя переменной и её значенте
# поможет setattr
def console(*args, delimetr='- ', length=50):
    print('\n', '=' * 100)
    for elem in args:
        print(elem)
        print(delimetr * length)
    print('=' * 100, '\n')


def p_type(obj):
    return print(type(obj))