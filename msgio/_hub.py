from typing import Callable, Generic, TypeVar

from pydantic import BaseModel


__all__ = (
    "Hub",
    "HubSubscriber"
)


M = TypeVar("M", bound=BaseModel)


HubSubscriber = Callable[[M], None]


class Hub(Generic[M]):
    _subscribers: set[HubSubscriber]

    def __init__(self) -> None:
        self._subscribers = []

    def dispatch(self, message: M) -> None:
        for subscriber in self._subscribers:
            subscriber(message)

    def subscribe(self, subscriber: HubSubscriber) -> Callable[[], None]:
        self._subscribers.add(subscriber)

        def unsubscribe() -> None:
            self._subscribers.remove(subscriber)

        return unsubscribe
