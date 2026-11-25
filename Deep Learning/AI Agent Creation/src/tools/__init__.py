"""External tools the agent can call. Each one documents when the agent uses it."""
from src.tools import data_tool, file_tool
from src.tools.base import ToolResult, ToolSpec, safe_tool_call
from src.tools.sql_tool import SPEC as SQL_SPEC
from src.tools.sql_tool import SqlTool

TOOL_SPECS = [file_tool.SPEC, data_tool.SPEC, SQL_SPEC]

__all__ = ["SqlTool", "TOOL_SPECS", "ToolResult", "ToolSpec", "data_tool", "file_tool", "safe_tool_call"]
