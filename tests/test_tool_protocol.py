from minicodeagent.tool_protocol import (
    ErrorCode,
    ToolStatus,
    error_response,
    is_tool_response,
    response_error_code,
    response_status,
    response_text,
    success_response,
)


def test_success_response_has_standard_envelope():
    response = success_response(
        data={"path": "README.md"},
        text="read README.md",
        params_input={"path": "README.md"},
        time_ms=12,
        context={"cwd": "."},
    )

    assert is_tool_response(response)
    assert response["status"] == ToolStatus.SUCCESS.value
    assert response["data"] == {"path": "README.md"}
    assert response["text"] == "read README.md"
    assert response["stats"]["time_ms"] == 12
    assert response["context"]["params_input"] == {"path": "README.md"}
    assert response["context"]["cwd"] == "."
    assert response_text(response) == "read README.md"
    assert response_status(response) == "success"


def test_error_response_exposes_code_and_text():
    response = error_response(
        code=ErrorCode.ACCESS_DENIED,
        message="path escapes workspace",
        params_input={"path": "../secret.txt"},
    )

    assert is_tool_response(response)
    assert response["status"] == ToolStatus.ERROR.value
    assert response["error"]["code"] == ErrorCode.ACCESS_DENIED.value
    assert response_error_code(response) == ErrorCode.ACCESS_DENIED.value
    assert response_text(response) == "path escapes workspace"
