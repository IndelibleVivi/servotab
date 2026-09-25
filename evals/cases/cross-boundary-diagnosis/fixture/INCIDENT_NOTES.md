# Observations available at handoff

Expected contract: active-relay tagged client uploads reach the service, including bursts. Ordinary untagged client admission retains its four-request fixture budget. A stale tag while the relay is disabled grants no exemption. gateway.py owns this policy for all clients; there is no per-device identity contract.

The user reports intermittent handheld stalls; ordinary desktop use normally sends one request. Local health checks report delivery success. The desktop and handheld both enter the shared client path, but the handheld also has recorded access delays.

A prior handset-specific exemption trial targeted an old client identifier. There is no receipt proving its match against the current handset or a comparable request workload. The user still reported stalls, and the exemption was rolled back. A later access-setting trial also failed to restore the overall experience.

One fresh gateway record shows tagged client traffic while the relay is active: eight attempts, four admission rejections. Separately, access observations contain late delivery on the handheld. Neither observation has been isolated in a controlled comparison. No new named-handheld observation is available here.
