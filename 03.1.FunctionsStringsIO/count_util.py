import typing as tp


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    fm = False
    fl = False
    fL = False
    fw = False
    if flags is None or flags == "":
        fm = True
        fl = True
        fL = True
        fw = True
    else:
        for i in flags:
            if i == "m":
                fm = True
            if i == "l":
                fl = True
            if i == "L":
                fL = True
            if i == "w":
                fw = True
    ans = dict()
    if fm:
        ans.fromkeys("chars")
        ans["chars"] = len(text)
    if fl:
        ans.fromkeys("lines")
        ans["lines"] = text.count("\n")
    if fw:
        l = text.split()
        ans.fromkeys("words")
        ans["words"] = len(l)
    if fL:
        mx = 0
        l = text.split("\n")
        for i in l:
            mx = max(mx, len(i))
        ans.fromkeys("longest_line")
        ans["longest_line"] = mx

    return ans
