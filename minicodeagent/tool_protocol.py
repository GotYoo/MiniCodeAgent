"""Unified tool response protocol.

Tools return a structured envelope for observability, while the runtime can
still pass the compact `text` field back to the model as the observation.
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any


class ToolStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"


class ErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    ACCESS_DENIED = "ACCESS_DENIED"
    INVALID_PARAM = "INVALID_PARAM"
    TIMEOUT = "TIMEOUT"
    EXECUTION_ERROR = "EXECUTION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    APPROVAL_DENIED = "APPROVAL_DENIED"
    READ_ONLY_BLOCKED = "READ_ONLY_BLOCKED"
    UNKNOWN_TOOL = "UNKNOWN_TOOL"
    REPEATED_TOOL_CALL = "REPEATED_TOOL_CALL"


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def build_response(
    status: ToolStatus | str,
    *,
    data: dict[str, Any] | None,
    text: str,
    params_input: dict[str, Any] | None,
    time_ms: int = 0,
    context: dict[str, Any] | None = None,
    error_code: ErrorCode | str | None = None,
    error_message: str | None = None,
) -> dict[str, Any]:
    status_value = status.value if isinstance(status, ToolStatus) else str(status)
    payload: dict[str, Any] = {
        "status": status_value,
        "data": _ensure_dict(data),
        "text": str(text),
        "stats": {"time_ms": max(0, int(time_ms or 0))},
        "context": {"params_input": _ensure_dict(params_input), **_ensure_dict(context)},
    }
    if status_value == ToolStatus.ERROR.value:
        code = error_code.value if isinstance(error_code, ErrorCode) else str(error_code or ErrorCode.INTERNAL_ERROR.value)
        payload["error"] = {
            "code": code,
            "message": str(error_message or text),
        }
    return payload


def success_response(
    *,
    data: dict[str, Any] | None = None,
    text: str,
    params_input: dict[str, Any] | None = None,
    time_ms: int = 0,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_response(
        ToolStatus.SUCCESS,
        data=data,
        text=text,
        params_input=params_input,
        time_ms=time_ms,
        context=context,
    )


def partial_response(
    *,
    data: dict[str, Any] | None = None,
    text: str,
    params_input: dict[str, Any] | None = None,
    time_ms: int = 0,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_response(
        ToolStatus.PARTIAL,
        data=data,
        text=text,
        params_input=params_input,
        time_ms=time_ms,
        context=context,
    )


def error_response(
    *,
    code: ErrorCode | str,
    message: str,
    params_input: dict[str, Any] | None = None,
    time_ms: int = 0,
    data: dict[str, Any] | None = None,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_response(
        ToolStatus.ERROR,
        data=data,
        text=message,
        params_input=params_input,
        time_ms=time_ms,
        context=context,
        error_code=code,
        error_message=message,
    )


def is_tool_response(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and value.get("status") in {ToolStatus.SUCCESS.value, ToolStatus.PARTIAL.value, ToolStatus.ERROR.value}
        and isinstance(value.get("data"), dict)
        and isinstance(value.get("stats"), dict)
        and isinstance(value.get("context"), dict)
    )


def response_text(value: Any) -> str:
    if is_tool_response(value):
        return str(value.get("text", ""))
    return str(value)


def response_status(value: Any) -> str:
    if is_tool_response(value):
        return str(value.get("status", ""))
    return ""


def response_error_code(value: Any) -> str:
    if not is_tool_response(value):
        return ""
    error = value.get("error")
    if not isinstance(error, dict):
        return ""
    return str(error.get("code", ""))


def response_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
