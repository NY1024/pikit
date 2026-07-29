"""Register safe test fixture tools with Hermes."""

from . import schemas, tools


def register(ctx):
    ctx.register_tool(
        name="pikit_read_document",
        toolset="pikit_fixture",
        schema=schemas.READ_DOCUMENT,
        handler=tools.read_document,
    )
    ctx.register_tool(
        name="pikit_record_sink",
        toolset="pikit_fixture",
        schema=schemas.RECORD_SINK,
        handler=tools.record_sink,
    )
