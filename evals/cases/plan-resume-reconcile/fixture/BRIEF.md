# Accepted outcome
JSON, CSV, and count must each cover every unique record, in first-observed order.
A record's id defines identity; equal titles do not. Support empty sources. Existing
CLI entry points and standard-library serialization are sufficient.

Earlier implementation proposal: fetch_page() probably returns all rows. That
proposal has not been checked against provider.py. Keep the source API unchanged.
No network, new dependencies, background services, or publication is required.
