from collections import UserList
import typing as tp


# https://github.com/python/mypy/issues/5264#issuecomment-399407428
if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    REVERSED = ["reversed", "R"]
    FIRST = ["first", "F"]
    LAST = ["last", "L"]
    SIZE = ["size", "S"]

    def __getattr__(self, oper: str) -> tp.Any:
        if oper in self.REVERSED:
            return list(reversed(self.data))
        elif oper in self.FIRST:
            return self.data[0]
        elif oper in self.LAST:
            return self.data[-1]
        elif oper in self.SIZE:
            return len(self.data)
        else:
            return super().__getattribute__(oper)

    def __setattr__(self, key: str, value: tp.Any):
        if key in self.FIRST:
            self.data[0] = value
        elif key in self.LAST:
            self.data[-1] = value
        elif key in self.SIZE:
            sz = len(self.data)
            if sz <= value:
                for i in range(sz, value):
                    self.data += [None]
            else:
                del self.data[value:]
        else:
            return super().__setattr__(key, value)

