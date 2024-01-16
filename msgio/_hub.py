from ._message import Message


__all__ = (
    "Hub",
    "HubMessageHandler"
)


class HubMessageHandler:
    def on(self, message: Message) -> None:
        raise NotImplementedError


class Hub:
    _handlers: list[HubMessageHandler]

    def __init__(self) -> None:
        self._handlers = []

    def dispatch(self, message: Message) -> None:
        for handler in self._handlers:
            handler.on(message)

    def register(self, handler: HubMessageHandler) -> None:
        self._handlers.append(handler)

    def unregister(self, handler: HubMessageHandler) -> None:
        self._handlers.remove(handler)
