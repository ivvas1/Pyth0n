import enum
from typing import Dict, List


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
        ) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    visit = dict()
    ansvis = dict()
    for i in graph.keys():
        ansvis[i] = False
        visit[i] = False
    ans = list()
    for u in graph.keys():
        if not visit[u]:
            stack = [u]
            visit[u] = True
            while stack:
                v = stack[-1]
                j = 0
                for i in graph[v]:
                    if not visit[i]:
                        visit[i] = True
                        stack.append(i)
                        break
                    j += 1
                if j == len(graph[v]):
                    if not ansvis[v]:
                        ans.append(v)
                        ansvis[v] = True
                    stack.pop()
    return list(reversed(ans))


def build_graph(
        words: list[str]
        ) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    ans = dict()
    for i in words:
        for j in i:
            ans[j] = set()

    for i in range(len(words) - 1):
        u = words[i]
        v = words[i + 1]
        j = 0
        while j < min(len(u), len(v)) and u[j] == v[j]:
            j += 1
        if j < min(len(u), len(v)):
            ans[u[j]].add(v[j])

    return ans


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
        ) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
