from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, Field

mcp = MCPServer("Pipeline Operations")


class PipelineStatus(BaseModel):
    pipeline_id: str
    run_id: str
    status: Literal["success", "failed", "running"]
    rows_processed: int
    error_code: str | None = None


PIPELINES = {
    "software_inventory_daily": PipelineStatus(
        pipeline_id="software_inventory_daily",
        run_id="run-001",
        status="failed",
        rows_processed=0,
        error_code="UPSTREAM_TIMEOUT",
    ),
    "database_performance_daily": PipelineStatus(
        pipeline_id="database_performance_daily",
        run_id="run-002",
        status="success",
        rows_processed=125_000,
    ),
}


@mcp.tool()
def list_pipelines() -> list[str]:
    """List pipeline identifiers available in this demonstration."""
    return sorted(PIPELINES)


@mcp.tool()
def get_pipeline_status(
    pipeline_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=80,
            pattern=r"^[a-z][a-z0-9_]*$",
        ),
    ],
) -> PipelineStatus:
    """Read the latest run status for a known pipeline."""
    pipeline = PIPELINES.get(pipeline_id)

    if pipeline is None:
        raise ToolError("Pipeline not found.")

    return pipeline


if __name__ == "__main__":
    mcp.run()