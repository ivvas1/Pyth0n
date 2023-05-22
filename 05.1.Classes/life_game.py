

class LifeGame(object):
    """
    Class for Game life
    """
    EMPTY = 0
    CLIFF = 1
    FISH = 2
    SHR = 3

    def __init__(self, field: list[list[int]]):
        self.board = field
        self.h = len(field)
        self.w = len(field[0])

    def _get_condition(self, i, j) -> int:
        H = self.h
        W = self.w
        el = self.board[i][j]
        if el == self.FISH or el == self.SHR:
            kol_nei = -1
            for u in range(max(i - 1, 0), min(i + 2, H)):
                for v in range(max(j - 1, 0), min(j + 2, W)):
                    if self.board[u][v] == el:
                        kol_nei += 1
            if kol_nei == 2 or kol_nei == 3:
                return el
            else:
                return self.EMPTY


        elif el == self.EMPTY:
            kol_nei_fish = 0
            kol_nei_shr = 0
            for u in range(max(i - 1, 0), min(i + 2, H)):
                for v in range(max(j - 1, 0), min(j + 2, W)):
                    if self.board[u][v] == self.FISH:
                        kol_nei_fish += 1
                    elif self.board[u][v] == self.SHR:
                        kol_nei_shr += 1
            if kol_nei_fish == 3:
                return self.FISH
            elif kol_nei_shr == 3:
                return self.SHR
            else:
                return self.EMPTY
        else:
            return self.CLIFF


    def get_next_generation(self) -> list[list[int]]:
        H = self.h
        W = self.w
        ans = [0] * H
        for i in range(H):
            ans[i] = [0] * W
        for i in range(H):
            for j in range(W):
                ans[i][j] = self._get_condition(i, j)
        self.board = ans
        return self.board
