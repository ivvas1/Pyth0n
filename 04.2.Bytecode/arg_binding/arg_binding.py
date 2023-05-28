from types import FunctionType
from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8
ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for argument'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from args and kwargs to corresponding arguments of func
        :param func: function to be inspected
        :param args: positional arguments to be bound
        :param kwargs: keyword arguments to be bound
        :return: dict[argument_name] = argument_value if binding was successful,
                 raise TypeError with one of ERR_* error descriptions otherwise
    """
    code = func.__code__
    kwdefaults = func.__kwdefaults__
    defaults = func.__defaults__
    co_var = code.co_flags & CO_VARARGS == CO_VARARGS
    co_kwar = code.co_flags & CO_VARKEYWORDS == CO_VARKEYWORDS
    arg_names = code.co_varnames[:(code.co_argcount + co_var + co_kwar + code.co_kwonlyargcount)]
    arg_ = None
    kw_ = None

    res: dict[str, Any] = {}

    if co_var:
        arg_ = code.co_varnames[(code.co_argcount + code.co_kwonlyargcount)]
        res[arg_] = ()
        if (code.co_flags // CO_VARKEYWORDS) % 2 == 1:
            kw_ = code.co_varnames[(code.co_argcount + code.co_kwonlyargcount + 1)]
            res[kw_] = {}
    elif co_kwar:
        kw_ = code.co_varnames[(code.co_argcount + code.co_kwonlyargcount)]
        res[kw_] = {}
    for i in range(len(args)):
        if i < code.co_argcount:
            res[arg_names[i]] = args[i]
        elif arg_ is None:
            raise TypeError(ERR_TOO_MANY_POS_ARGS)
        else:
            res[arg_] += (args[i],)
    for elem in kwargs:
        if elem in arg_names[:code.co_posonlyargcount]:
            if kw_ is not None:
                res[kw_][elem] = kwargs[elem]
            else:
                raise TypeError(ERR_POSONLY_PASSED_AS_KW)
        elif elem in arg_names:
            if elem in res:
                raise TypeError(ERR_MULT_VALUES_FOR_ARG)
            res[elem] = kwargs[elem]
        else:
            if kw_ is None:
                raise TypeError(ERR_TOO_MANY_KW_ARGS)
            else:
                res[kw_][elem] = kwargs[elem]
    if kwdefaults is not None:
        for elem, val in kwdefaults.items():
            if elem not in res:
                res[elem] = val
    if defaults is not None:
        for i in range(-len(defaults), 0):
            if arg_names[:code.co_argcount][i] not in res:
                res[arg_names[:code.co_argcount][i]] = defaults[i]
    for name in arg_names[:code.co_argcount]:
        if name not in res:
            raise TypeError(ERR_MISSING_POS_ARGS)
    for name in arg_names[code.co_argcount:code.co_argcount + code.co_kwonlyargcount]:
        if name not in res:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)
    return res
