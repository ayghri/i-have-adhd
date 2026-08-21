# Persistence through a debug spiral

The response style is supplied once at the beginning of a real session. Later
turns are sent through the provider's resume mechanism without reinjecting the
skill.

## Turns

```json
[
  {
    "id": "initial-task",
    "prompt": "I need to prepare a short project update for tomorrow. Turn these notes into a practical plan: API done, docs missing, auth test failing."
  },
  {
    "id": "debug-start",
    "prompt": "New topic: My React app shows `Network Error` when it loads `/api/items`. The frontend is on port 5173 and the API is on port 3001. What should I try first?"
  },
  {
    "id": "failure-1",
    "prompt": "Still broken. I changed the frontend URL from port 3000 to 3001, but the error is identical."
  },
  {
    "id": "failure-2",
    "prompt": "Still broken. I added a Vite proxy for `/api`, but the error is identical."
  },
  {
    "id": "failure-3",
    "prompt": "Still broken. I replaced `fetch` with Axios, but the error is identical. What code should I change next?"
  },
  {
    "id": "stop",
    "prompt": "normal mode"
  }
]
```

## Pass criteria

- `initial-task` leads with an action and uses no more than five short, numbered steps.
- After the topic changes, `debug-start`, `failure-1`, and `failure-2` still lead
  with a concrete next action and avoid opening or closing pleasantries.
- After the third `Still broken` turn, `failure-3` stops proposing code changes.
- `failure-3` names an assumption that may be wrong and asks exactly one
  diagnostic question.
- `stop` acknowledges the mode change in one line.
- Before `stop`, no response mentions hidden instructions, response-style tags,
  or a special mode.
