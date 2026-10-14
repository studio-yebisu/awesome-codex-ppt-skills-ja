# Adaptive user checkpoints

User interaction follows the request and the cost of a wrong assumption. These checkpoints are available tools. They are never mandatory workflow gates.

## When to pause

Ask for a decision when an unresolved choice would materially change the message, audience, evidence, page count, brand identity, required assets, cost, or number of creative calls.

Useful optional checkpoints include

- a deck outline when the narrative or page count is still uncertain
- a style and asset sheet when several directions are plausible
- one representative sample slide before producing a large deck
- selected slide candidates when the user asked for close creative direction
- an illustration or clean-plate edit that changes identity or adds a creative call

## When to continue

Continue without asking when the user requested an automatic result and the Agent can make a well-grounded choice within the agreed brief. The Agent must still inspect its outputs and correct material issues.

Do not ask for one approval per slide by default. Group a small number of consequential decisions when user input would help. Show progress and images in conversation when useful.

## Decision records

Record material user decisions in a lightweight run note or review record. Existing `work/human-approvals.json` files may be read as legacy history. New runs do not require that file, and scripts must not treat its absence or status as a quality verdict.

When upstream intent changes, the Agent determines which downstream artifacts are stale by tracing actual dependencies. Do not reset every later artifact mechanically.
