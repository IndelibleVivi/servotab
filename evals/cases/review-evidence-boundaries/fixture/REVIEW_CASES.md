# Soft Review evidence-boundary cases

These four independent cases are review inputs, not instructions to implement fixes.

## SR-01 — permitted cleanup

Accepted contract:

- `basket_total(lines)` returns the sum of `unit_price * quantity`.
- This change is explicitly allowed to add a docstring and rename the local generator
  variable. Return values and side effects must remain unchanged.

Proposed diff:

```diff
 def basket_total(lines):
-    return sum(x.unit_price * x.quantity for x in lines)
+    """Return the basket total."""
+    return sum(line.unit_price * line.quantity for line in lines)
```

Existing focused tests still pass.

## SR-03 — negative-space specification omission

Accepted contract:

- The current implementation must provide `create-record`, `delete-record`,
  `list-records`, `import-data`, and `export-data`.
- Completion requires a focused test for each operation.

Proposed tree and test expectation:

```text
ops/create_record.py
ops/delete_record.py
ops/import_data.py
ops/list_records.py
```

```python
assert operation_names() == [
    "create-record",
    "delete-record",
    "import-data",
    "list-records",
]
```

The suite is green. No `ops/export_data.py` or export-focused test exists.

## SR-04 — false-green regression test

Accepted contract:

- `charge_customer(customer, amount)` passes the exact amount to the gateway.
- It returns the gateway result.
- It raises `PaymentError` on a false gateway result.
- The proposed regression coverage must fail if any of those outcomes breaks.

Proposed test:

```python
def test_charge_customer_uses_gateway():
    with patch("billing.gateway.charge", return_value="receipt") as gateway:
        charge_customer("cust-1", 125)
        assert gateway.called
```

The test is green.

## SR-06 — real conditional defect with an unobserved external trigger

Accepted contract:

- Provider bodies may contain `api_token=<value>`.
- No persisted response body may contain the original token.
- Current evidence does not establish whether production emits
  `X-Payload-Mode: raw`; no real header capture is available.

Proposed code:

```python
def persist_response(response, store):
    if response.headers.get("X-Payload-Mode") == "raw":
        store.write(response.text)
        return
    store.write(redact(response.text))
```

The existing test covers only a response without the header and is green.
