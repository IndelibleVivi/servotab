# Embedded export boundary

The repository has a green unit contract in `test_contract.py`, a green build, and an HTTP smoke that proves the embedded resource contains the export code. None of those checks executes the host capability envelope.

The embedded host reports `chat_file` as an object with a `state` field:

```text
available -> {"chat_file": {"state": "available"}}
denied    -> {"chat_file": {"state": "denied"}}
missing   -> {}
```

Production currently selects `chat-file` for the denied envelope because any non-empty object is truthy. The exact named host remains the final acceptance surface, including its real policy and user-interaction behavior. Local work should reproduce only this observable capability contract.
