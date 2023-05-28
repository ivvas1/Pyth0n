"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import importlib
import types
import typing as tp

CO_VARARGS = 4
CO_VARKEYWORDS = 8
ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(code: types.CodeType, defaults: tuple[tp.Any],
              kwdefaults: dict[str, tp.Any],
              *args: tp.Any,
              **kwargs: tp.Any) -> dict[str, tp.Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`
    :param code: function's code
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
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


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.9/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None
        self.index: int = 0
        self.instructions = list(dis.get_instructions(self.code))

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n:
            ret = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return ret
        else:
            return []

    def run(self) -> tp.Any:

        while self.index < len(self.instructions):
            instruction = self.instructions[self.index]
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
            self.index += 1

        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3496
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def call_function_ex_op(self, arg: tp.Any) -> None:
        if arg % 2 == 0:
            args = self.pop()
            f = self.pop()
            self.push(f(*args))
            return
        kwargs, args, f = self.popn(3)
        self.push(f(*args, **kwargs))

    def call_function_kw_op(self, arg: int) -> None:
        keys = self.pop()
        key_len = len(keys)
        words = self.popn(key_len)
        args = self.popn(arg - key_len)
        kwargs = dict(zip(keys, words))
        f = self.pop()
        self.push(f(*args, **kwargs))

    def load_name_op(self, arg: str) -> None:

        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])

    def load_global_op(self, arg: str) -> None:

        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])

    def store_global_op(self, arg: str) -> None:
        self.globals[arg] = self.pop()

    def load_const_op(self, arg: tp.Any) -> None:
        self.push(arg)

    def load_closure_op(self, arg: str) -> None:
        self.load_name_op(arg)

    def load_deref_op(self, arg: str) -> None:
        self.load_name_op(arg)

    def return_value_op(self, arg: tp.Any) -> None:

        self.return_value = self.pop()
        self.index = len(list(dis.get_instructions(self.code)))

    def pop_top_op(self, arg: tp.Any) -> None:
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
                Operation description:
                    https://docs.python.org/release/3.9.7/library/dis.html#opcode-MAKE_FUNCTION

                Operation realization:
                    https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3571

                Parse stack:
                    https://github.com/python/cpython/blob/3.9/Objects/call.c#L671

                Call function in cpython:
                    https://github.com/python/cpython/blob/3.9/Python/ceval.c#L4950
                """

        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)
        kwdefaults: dict[str, tp.Any] = {}
        if arg & 2 == 2:
            kwdefaults = self.pop()
        defaults: tuple[tp.Any] = ((),)
        if arg & 1 == 1:
            defaults = self.pop()


        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:

            parsed_args: dict[str, tp.Any] = bind_args(code, defaults, kwdefaults, *args, **kwargs)

            f_globals = dict(self.globals)
            f_globals.update(self.locals)
            frame = Frame(code, self.builtins, f_globals, parsed_args)  # Run code in prepared environment
            res = frame.run()
            self.globals.update(f_globals)
            return res

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        self.locals[arg] = self.pop()

    def store_fast_op(self, arg: tp.Any) -> None:
        self.locals[arg] = self.pop()

    def delete_fast_op(self, arg: tp.Any) -> None:
        del self.locals[arg]

    def load_fast_op(self, arg: tp.Any) -> None:
        self.push(self.locals[arg])

    def load_attr_op(self, arg: str) -> None:
        self.push(getattr(self.pop(), arg))

    def store_attr_op(self, arg: str) -> None:
        setattr(self.pop(), arg, self.pop())

    def delete_attr_op(self, arg: str) -> None:
        delattr(self.pop(), arg)

    def dup_top_two_op(self, arg: tp.Any) -> None:
        self.push(self.top(), self.data_stack[-2])

    def dup_top_op(self, arg: tp.Any) -> None:
        self.push(self.top())

    def rot_two_op(self, arg: tp.Any) -> None:
        st2, st1 = self.popn(2)
        self.push(st1, st2)

    def rot_three_op(self, arg: tp.Any) -> None:
        st3, st2, st1 = self.popn(3)
        self.push(st1, st3, st2)

    def rot_four_op(self, arg: tp.Any) -> None:
        st4, st3, st2, st1 = self.popn(4)
        self.push(st1, st4, st3, st2)

    def extended_arg_op(self, arg: tp.Any) -> None:
        pass

    def jump_forward_op(self, arg: tp.Any) -> None:
        self.index = arg // 2 - 1

    def jump_absolute_op(self, arg: tp.Any) -> None:
        self.index = arg // 2 - 1

    def pop_jump_if_false_op(self, arg: tp.Any) -> None:
        if not self.pop():
            self.jump_absolute_op(arg)

    def pop_jump_if_true_op(self, arg: tp.Any) -> None:
        if self.pop():
            self.jump_absolute_op(arg)

    def jump_if_true_or_pop_op(self, arg: tp.Any) -> None:
        if self.top():
            self.jump_absolute_op(arg)
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, arg: tp.Any) -> None:
        if not self.top():
            self.jump_absolute_op(arg)
        else:
            self.pop()

    def jump_if_not_exc_match_op(self, arg: tp.Any) -> None:
        if not isinstance(self.data_stack[-2], Exception):
            self.jump_absolute_op(arg)
            self.popn(2)

    def unpack_sequence_op(self, arg: int) -> None:
        seq = self.pop()
        for i in range(arg):
            self.push(seq[arg - 1 - i])

    def build_tuple_op(self, arg: int) -> None:
        tuple_ = tuple(self.popn(arg))
        self.push(tuple_)

    def build_list_op(self, arg: int) -> None:
        list_ = list(self.popn(arg))
        self.push(list_)

    def build_set_op(self, arg: int) -> None:
        set_ = set(self.popn(arg))
        self.push(set_)

    def build_map_op(self, arg: int) -> None:
        got = self.popn(2 * arg)
        self.push(dict(zip(got[0::2], got[1::2])))

    def build_const_key_map_op(self, arg: int) -> None:
        key = self.pop()
        val = self.popn(arg)
        self.push(dict(zip(key, val)))

    def format_value_op(self, arg: tp.Any) -> None:
        pass

    def build_string_op(self, arg: int) -> None:
        string: str = ''.join(self.popn(arg))
        self.push(string)

    def list_to_tuple_op(self, arg: int) -> None:
        self.push(tuple(self.pop()))

    def set_update_op(self, arg: tp.Any) -> None:
        set2 = self.pop()
        set1 = self.pop()
        set.update(set1, set2)
        self.push(set1)

    def list_extend_op(self, arg: tp.Any) -> None:
        lst2 = self.pop()
        lst1 = self.pop()
        list.extend(lst1, lst2)
        self.push(lst1)

    def dict_update_op(self, arg: tp.Any) -> None:
        dict2 = self.pop()
        dict1 = self.pop()
        dict.update(dict1, dict2)
        self.push(dict1)

    def dict_merge_op(self, arg: tp.Any) -> None:
        dict2: dict[tp.Any, tp.Any] = self.pop()
        dict1: dict[tp.Any, tp.Any] = self.pop()
        for key, value in dict2.items():
            if key in dict1.keys():
                raise Exception
            else:
                dict1[key] = value
        self.push(dict1)

    def load_method_op(self, arg: str) -> None:
        item = self.pop()
        try:
            meth = getattr(item, arg)
            self.push(meth)
        except AttributeError:
            self.push(None, callable(tp.Any))

    def call_method_op(self, arg: int) -> None:
        args = self.popn(arg)
        method = self.pop()
        self.push(method(*args))

    def build_slice_op(self, arg: int) -> None:
        self.push(slice(*self.popn(arg)))

    def store_subscr_op(self, arg: tp.Any) -> None:
        val, obj, ind = self.popn(3)
        obj[ind] = val
        self.push(obj)

    def delete_subscr_op(self, arg: tp.Any) -> None:
        obj, ind = self.popn(3)
        del obj[ind]
        self.push(obj)

    def raise_varargs_op(self, arg: int) -> None:
        if arg == 0:
            pass
        elif arg == 1:
            raise self.pop()
        else:
            pass

    for_comp_op: dict[str, tp.Callable[[tp.Any, tp.Any], tp.Any]] = {
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y,
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
    }

    def compare_op_op(self, arg: tp.Any) -> None:
        x, y = self.popn(2)
        self.push(self.for_comp_op[arg](x, y))

    def is_op_op(self, arg: int) -> None:
        x, y = self.popn(2)
        if arg:
            self.push(x is not y)
        else:
            self.push(x is y)

    def contains_op_op(self, arg: int) -> None:
        x, y = self.popn(2)
        if arg:
            self.push(x not in y)
        else:
            self.push(x in y)

    for_binary: dict[str, tp.Callable[[tp.Any, tp.Any], tp.Any]] = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '-': lambda x, y: x - y,
        '/': lambda x, y: x / y,
        '//': lambda x, y: x // y,
        'and': lambda x, y: x & y,
        'or': lambda x, y: x | y,
        '**': lambda x, y: x ** y,
        '@': lambda x, y: x @ y,
        '%': lambda x, y: x % y,
        '[]': lambda x, y: x[y],
        '<<': lambda x, y: x << y,
        '>>': lambda x, y: x >> y,
        '^': lambda x, y: x ^ y
    }

    def binary_op(self, op: str) -> None:
        x, y = self.popn(2)
        self.push(self.for_binary[op](x, y))

    def binary_add_op(self, arg: tp.Any) -> None:
        self.binary_op('+')

    def binary_subtract_op(self, arg: tp.Any) -> None:
        self.binary_op('-')

    def binary_multiply_op(self, arg: tp.Any) -> None:
        self.binary_op('*')

    def binary_true_divide_op(self, arg: tp.Any) -> None:
        self.binary_op('/')

    def binary_power_op(self, arg: tp.Any) -> None:
        self.binary_op('**')

    def binary_floor_divide_op(self, arg: tp.Any) -> None:
        self.binary_op('//')

    def binary_modulo_op(self, arg: tp.Any) -> None:
        self.binary_op('%')

    def binary_and_op(self, arg: tp.Any) -> None:
        self.binary_op('and')

    def binary_or_op(self, arg: tp.Any) -> None:
        self.binary_op('or')

    def binary_xor_op(self, arg: tp.Any) -> None:
        self.binary_op('^')

    def binary_matrix_multiply_op(self, arg: tp.Any) -> None:
        self.binary_op('@')

    def binary_subscr_op(self, arg: tp.Any) -> None:
        self.binary_op('[]')

    def binary_lshift_op(self, arg: tp.Any) -> None:
        self.binary_op('<<')

    def binary_rshift_op(self, arg: tp.Any) -> None:
        self.binary_op('>>')

    def inplace_op(self, op: str) -> None:
        x, y = self.popn(2)
        self.push(self.for_binary[op](x, y))

    def inplace_add_op(self, arg: tp.Any) -> None:
        self.inplace_op('+')

    def inplace_subtract_op(self, arg: tp.Any) -> None:
        self.inplace_op('-')

    def inplace_multiply_op(self, arg: tp.Any) -> None:
        self.inplace_op('*')

    def inplace_true_divide_op(self, arg: tp.Any) -> None:
        self.inplace_op('/')

    def inplace_power_op(self, arg: tp.Any) -> None:
        self.inplace_op('**')

    def inplace_floor_divide_op(self, arg: tp.Any) -> None:
        self.inplace_op('//')

    def inplace_and_op(self, arg: tp.Any) -> None:
        self.inplace_op('and')

    def inplace_or_op(self, arg: tp.Any) -> None:
        self.inplace_op('or')

    def inplace_xor_op(self, arg: tp.Any) -> None:
        self.inplace_op('^')

    def inplace_matrix_multiply_op(self, arg: tp.Any) -> None:
        self.inplace_op('@')

    def inplace_modulo_op(self, arg: tp.Any) -> None:
        self.inplace_op('%')

    def inplace_subscr_op(self, arg: tp.Any) -> None:
        self.inplace_op('[]')

    def inplace_lshift_op(self, arg: tp.Any) -> None:
        self.inplace_op('<<')

    def inplace_rshift_op(self, arg: tp.Any) -> None:
        self.inplace_op('>>')


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
