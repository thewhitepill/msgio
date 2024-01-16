from enum import StrEnum, auto

from ._message import Message

from typing import Any, Callable


__all__ = (
    "Pipeline",
    "PipelineDirection",
    "PipelineDispatch",
    "PipelineMessageHandler"
)


class PipelineDirection(StrEnum):
    BACKWARD = auto()
    FORWARD = auto()


PipelineDispatch = Callable[[Message, PipelineDirection], Any]


class PipelineMessageHandler:
    dispatch: PipelineDispatch | None = None

    def _bind(self, dispatch: PipelineDispatch) -> None:
        self.dispatch = dispatch

    def on(self, message: Message, direction: PipelineDirection) -> Any:
        return self.dispatch(message, direction)


class _Head(PipelineMessageHandler):
    def on(self, message: Message, direction: PipelineDirection) -> Any:
        match direction:
            case PipelineDirection.BACKWARD:
                raise NotImplementedError(
                    f"Message '{message.__class__.__name__}' has reached the"
                    "head of a pipeline without being handled"
                )
            case PipelineDirection.FORWARD:
                return self.dispatch(message, direction)
            case _:
                raise RuntimeError


class _Tail(PipelineMessageHandler):
    def on(self, message: Message, direction: PipelineDirection) -> Any:
        match direction:
            case PipelineDirection.BACKWARD:
                return self.dispatch(message, direction)
            case PipelineDirection.FORWARD:
                raise NotImplementedError(
                    f"Message '{message.__class__.__name__}' has reached the"
                    "tail of a pipeline without being handled"
                )
            case _:
                raise RuntimeError


def _create_dispatch(
    handlers: list[PipelineMessageHandler],
    index: int | None
) -> PipelineDispatch:
    def dispatch(message: Message, direction: PipelineDirection) -> Any:
        match direction:
            case PipelineDirection.BACKWARD:
                next_handler = (
                    handlers[index - 1]
                        if index is not None
                        else handlers[-1]
                )
            case PipelineDirection.FORWARD:
                next_handler = (
                    handlers[index + 1]
                        if index is not None
                        else handlers[0]
                )
            case _:
                raise RuntimeError

        return next_handler.on(message, direction)

    return dispatch


def _bind_handlers(
    handlers: list[PipelineMessageHandler]
) -> list[PipelineMessageHandler]:
        bound = [_Head(), *handlers, _Tail()]

        for index, handler in enumerate(bound):
            handler._bind(_create_dispatch(bound, index))

        return bound


class Pipeline:
    dispatch: PipelineDispatch

    def __init__(self, handlers: list[PipelineMessageHandler]) -> None:
        self._handlers = _bind_handlers(handlers)
        self.dispatch = _create_dispatch(self._handlers, None)
