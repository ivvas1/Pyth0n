import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from inp stream, reformats it and prints to out stream

    Expected input format: <sha-1>\t<date>\t<author>\t<email>\t<message>
    Output format: <first 7 symbols of sha-1>.....<message>
    """
    while log_ := inp.readline():
        log = log_.strip().split("\t")
        sha = log[0][0:7]
        message = log[4]
        out.write(sha+(80 - len(message) - len(sha)) * "."+message+'\n')
