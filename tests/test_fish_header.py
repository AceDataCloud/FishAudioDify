"""The production /fish/tts contract declares model in a header, never in JSON."""

import json

import dify_plugin  # noqa: F401 - patch before requests/SSL imports
import pytest
import requests
from dify_plugin.config.config import DifyPluginEnv
from dify_plugin.core.plugin_registration import PluginRegistration
from dify_plugin.entities.tool import ToolRuntime


@pytest.mark.parametrize("model", ["s1", "s2-pro", "s2.1-pro"])
def test_selected_fish_model_reaches_the_serialized_http_header(model, monkeypatch):
    calls = []

    def send(method, url, **kwargs):
        prepared = requests.Request(
            method,
            url,
            headers=kwargs["headers"],
            json=kwargs.get("json"),
            params=kwargs.get("params"),
        ).prepare()
        calls.append(prepared)
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"task_id":"wire-fixture","status":"pending"}'
        response.close = lambda: None
        return response

    monkeypatch.setattr(requests, "request", send)
    registration = PluginRegistration(DifyPluginEnv())
    provider = next(iter(registration.tools_mapping))
    cls = registration.get_tool_cls(provider, "fish_generate_audio")
    tool = cls(
        ToolRuntime(credentials={"acedata_bearer_token": "fixture"}, user_id=None, session_id=None),
        None,
    )
    list(tool._invoke({"text": "Offline wire check", "model": model}))
    assert len(calls) == 1
    assert calls[0].method == "POST" and calls[0].url == "https://api.acedata.cloud/fish/tts"
    assert calls[0].headers["model"] == model
    assert "model" not in json.loads(calls[0].body)
