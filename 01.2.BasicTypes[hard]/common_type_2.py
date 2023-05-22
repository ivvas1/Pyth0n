import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    lst = False
    it = False
    flt = False
    bol = False
    sr = False
    it01 = False
    non = 0
    ans = list()
    for i in data:
        if i == "" or i is None:
            non += 1
        elif type(i) == list or type(i) == tuple:
            lst = True
        elif type(i) == int and i != 1 and i != 0:
            it = True
        elif type(i) == float:
            flt = True
        elif type(i) == str:
            sr = True
        elif type(i) == bool:
            bol = True
        elif i == 1 or i == 0:
            it01 = True
    if lst:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append(list())
            else:
                if type(data[i]) != str and type(data[i]) != int and type(data[i]) != bool:
                    ans.append(list(data[i]))
                else:
                    s = list()
                    s.append(data[i])
                    ans.append(s)
    elif sr:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append("")
            else:
                ans.append(str(data[i]))
    elif flt:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append(0.0)
            else:
                ans.append(float(data[i]))
    elif it:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append(0)
            else:
                ans.append(int(data[i]))
    elif bol:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append(False)
            else:
                ans.append(bool(data[i]))
    elif it01:
        for i in range(len(data)):
            if data[i] == "" or data[i] is None:
                ans.append(0)
            else:
                ans.append(int(data[i]))
    else:
        for i in range(len(data)):
            ans.append("")
    return ans
