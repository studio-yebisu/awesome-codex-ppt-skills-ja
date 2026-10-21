# Workflow Gates

Use gates to avoid producing the wrong deck quickly.

## Always Gate

- Requirement check
- Route decision
- Design/style confirmation, unless Auto Mode is active
- Image-first sample approval
- Reference PPT scope confirmation when ambiguous
- QA before delivery

## Do Not Gate Repeatedly

Do not keep asking after the user says:

- 随便
- 你看着办
- 自由发挥
- 直接做
- 不用问我

In Auto Mode, proceed with documented assumptions.

## Stop And Ask

Ask before:

- Uploading user files to an external service
- Calling external image/OCR/TTS/search APIs
- Running third-party install scripts
- Writing global directories or user config
- Changing facts, numbers, core conclusions, or logic in an existing PPT
- Modifying non-target slides in a single-slide edit

## Proceed Without Asking

Proceed when:

- The user provided topic/content or target file
- Missing fields can be safely inferred
- The user asked you to decide
- The action stays within the project/run directory
- The change is reversible and logged
