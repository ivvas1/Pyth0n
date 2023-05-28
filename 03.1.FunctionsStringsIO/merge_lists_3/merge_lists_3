import heapq
import typing as tp


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    heap = []
    for i in range(len(input_streams)):
        inp = input_streams[i].readline()
        if inp != b'':
            heap.append((int(inp), inp, i))
    heapq.heapify(heap)
    while heap:
        a, byte,  num = heapq.heappop(heap)
        output_stream.write(byte)
        new_inp = input_streams[num].readline()
        if new_inp != b'':
            heapq.heappush(heap, (int(new_inp), new_inp, num))
