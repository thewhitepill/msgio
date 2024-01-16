import pytest

from msgio import Message, Pipeline, PipelineDirection


def test():
    pipeline = Pipeline([])

    with pytest.raises(NotImplementedError):
        pipeline.dispatch(Message(), PipelineDirection.BACKWARD)

    with pytest.raises(NotImplementedError):
        pipeline.dispatch(Message(), PipelineDirection.FORWARD)
