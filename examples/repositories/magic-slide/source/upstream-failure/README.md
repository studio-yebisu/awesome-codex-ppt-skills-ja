# Raw upstream execution

The original injector ran unchanged. Local ordinary preview emitted ReferenceError: msAuthFetch is not defined. The archived browser-observations.json records it. QA calls were outside the closure defining msAuthFetch. Derived changes.diff shares that same authenticated closure; no plain-fetch bypass.
