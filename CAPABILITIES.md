# Fish Audio capability mapping

Compared with [MCPs at f0eed10abf31](https://github.com/AceDataCloud/MCPs/tree/f0eed10abf310824cb4c33d4944c63d3654ac95b/fish) and the public API contract at PlatformBackend `fa94598267a82545fb1afed6ee26bafd6cbb9ca7`.

Supports TTS, saved voices, multiple voice IDs and reference samples. For one-shot references, provide references as [{"audio":"https://...","text":"exact transcript"}]. Voice creation requires authorized source recordings.

| MCP function | Dify equivalent | Notes |
|---|---|---|
| `fish_get_usage_guide` |  | Model/action selectors and the API reference; informational guidance does not submit a request. |
| `fish_list_models` |  | Model/action selectors and the API reference; informational guidance does not submit a request. |
| `fish_get_model` |  | Model/action selectors and the API reference; informational guidance does not submit a request. |
| `fish_generate_audio` | `fish_generate_audio` |  |
| `fish_get_task` | `fish_task_retrieve` | Set action=retrieve |
| `fish_get_tasks_batch` | `fish_tasks_retrieve_batch` | Set action=retrieve_batch |

## Parameter equivalents

- `fish_list_models`: `page_size` → limit, `title` → query.
- `fish_generate_audio`: `prompt` → text, `voice_id` → reference_id, `reference_audio_url` → references[].audio, `reference_text` → references[].text, `async_` → Dify submit/poll output: async=true, stream=false.
- `fish_get_tasks_batch`: `task_ids` → ids.

## Verification boundary

Contract examples and regression tests cover request validation, transport and task handling. Actual Dify browser cases are recorded separately in `tests/e2e-results.json` and `tests/e2e-audit.json` when available. A schema test is not a successful paid generation. Unsupported service availability and untested advanced combinations must not be described as passed.
