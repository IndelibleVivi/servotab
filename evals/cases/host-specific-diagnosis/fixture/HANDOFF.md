# Available evidence

Contract: a handheld draft survives host suspension and resume. On this host, a native wake token changes before the resume callback. The desktop browser neither suspends this way nor supplies that token.

Desktop tests repeatedly pass. Handheld logs record an old token being read after wake; whether that mismatch causes draft loss has not been isolated. Prior shared storage and transport probes have completed with their expected outcomes. The named handheld is offline, and no trustworthy local implementation of its native resume-token behavior is available. No code mutation or owner interaction is authorized for this diagnostic task.
