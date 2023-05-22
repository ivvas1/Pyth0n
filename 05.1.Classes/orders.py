from dataclasses import dataclass, field, InitVar
from abc import abstractmethod, ABC
from typing import Union

DISCOUNT_PERCENTS = 15


@dataclass(order=True, frozen=True)
class Item:
    item_id: int = field(compare=False)
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title
        assert self.cost > 0


# Do not remove `# type: ignore`
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
@dataclass  # type: ignore
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> Union[float, int]:
        pass
@dataclass
class CountedPosition(Position):
    count: int = 1

    @property
    def cost(self) -> Union[float, int]:
        return self.count * self.item.cost


@dataclass
class WeightedPosition(Position):
    weight: float = 1.0

    @property
    def cost(self) -> Union[float, int]:
        return self.weight * self.item.cost

@dataclass
class Order:
    order_id: int
    positions: list[Position] = field(default_factory=list)
    cost: int = field(init=False)
    have_promo: InitVar[bool] = False

    def __post_init__(self, have_promo: bool) -> None:
        cost = sum(x.cost for x in self.positions)
        if have_promo:
            promo_multiplier = (1.0 - DISCOUNT_PERCENTS / 100)
            cost *= promo_multiplier
        self.cost = int(cost)
