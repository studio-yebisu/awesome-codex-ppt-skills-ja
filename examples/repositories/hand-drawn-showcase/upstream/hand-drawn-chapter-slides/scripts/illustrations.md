# Illustration Library

Ready-to-use SVG illustrations for hand-drawn chapter slides. All illustrations use
a 600x500 viewBox with off-white fill (`#FAF8F2`) and thick black strokes (`#141413`).

## How to Use

Each illustration is a complete SVG string. In your Node.js script:

```javascript
const FILL = "#FAF8F2";
const STROKE = "#141413";
function getIllustration(name) {
  return illustrations[name];
}
```

Convert to PNG with sharp:
```javascript
const sharp = require("sharp");
async function svgToBase64Png(svgString, width, height) {
  const buf = await sharp(Buffer.from(svgString))
    .resize(width, height, { fit: 'contain', background: { r:0, g:0, b:0, alpha:0 } })
    .png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
```

---

## Catalog

### 1. Magnifying Glass
**Topics**: Search, Discovery, Observability, Logging, Debugging, Investigation, QA

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <ellipse cx="280" cy="200" rx="140" ry="135" fill="#FAF8F2" stroke="#141413" stroke-width="7"/>
  <ellipse cx="280" cy="200" rx="105" ry="100" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <path d="M 220 140 Q 200 170, 215 195" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 375 310 Q 390 330, 440 400 Q 455 425, 480 445 Q 490 452, 485 460 Q 475 470, 465 462 Q 445 445, 420 410 Q 385 355, 365 325" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="235" cy="155" r="6" fill="#FAF8F2" opacity="0.7"/>
</svg>
```

### 2. Speech Bubbles
**Topics**: Communication, Feedback, User feedback loops, Discussion, Dialogue, Chat

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 100 80 Q 95 75, 200 70 Q 350 62, 430 78 Q 470 88, 475 130 Q 480 200, 472 240 Q 465 275, 420 282 Q 350 292, 250 288 L 200 340 Q 195 345, 195 330 L 195 290 Q 120 285, 105 260 Q 90 230, 92 160 Q 93 100, 100 80 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="155" y1="140" x2="410" y2="138" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="155" y1="175" x2="380" y2="173" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="155" y1="210" x2="350" y2="208" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 320 310 Q 315 305, 380 302 Q 480 295, 520 310 Q 545 322, 548 355 Q 550 390, 540 410 Q 530 430, 500 435 Q 460 440, 420 438 L 400 470 Q 398 475, 397 462 L 396 440 Q 345 438, 328 420 Q 312 400, 315 365 Q 316 325, 320 310 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <line x1="365" y1="345" x2="500" y2="343" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="365" y1="375" x2="485" y2="373" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 3. Coin Stack
**Topics**: Cost, Finance, Budget, Optimization, Money, Revenue, Pricing

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <ellipse cx="300" cy="380" rx="160" ry="50" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <path d="M 140 350 L 140 380 Q 140 430, 300 430 Q 460 430, 460 380 L 460 350" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <ellipse cx="300" cy="350" rx="160" ry="50" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="200" y1="350" x2="400" y2="350" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 160 260 L 160 290 Q 160 340, 300 340 Q 440 340, 440 290 L 440 260" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <ellipse cx="300" cy="260" rx="140" ry="45" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="215" y1="260" x2="385" y2="260" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 180 175 L 180 205 Q 180 250, 300 250 Q 420 250, 420 205 L 420 175" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <ellipse cx="300" cy="175" rx="120" ry="40" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="230" y1="175" x2="370" y2="175" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <text x="285" y="120" font-family="Georgia" font-size="50" fill="#141413" font-weight="bold">$</text>
</svg>
```

### 4. Rocket
**Topics**: Launch, Deployment, Pipelines, Shipping, Release, Speed, Startup

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 40 Q 295 35, 270 120 Q 250 190, 245 260 Q 242 300, 250 340 L 350 340 Q 358 300, 355 260 Q 350 190, 330 120 Q 310 40, 300 40 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="300" cy="195" r="32" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <circle cx="300" cy="195" r="20" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <path d="M 250 280 Q 220 300, 195 360 Q 190 375, 205 370 Q 230 355, 250 340 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 350 280 Q 380 300, 405 360 Q 410 375, 395 370 Q 370 355, 350 340 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 260 340 Q 275 380, 265 420 Q 300 390, 335 420 Q 325 380, 340 340" fill="#FAF8F2" stroke="#141413" stroke-width="3.5" stroke-linejoin="round"/>
  <path d="M 240 420 Q 225 430, 240 440 Q 255 450, 240 460" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 360 420 Q 375 430, 360 440 Q 345 450, 360 460" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 5. Two People (Team)
**Topics**: Collaboration, Team, Partnership, Cooperation, Community, Onboarding

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <circle cx="195" cy="110" r="55" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <path d="M 120 170 Q 115 175, 100 240 Q 90 290, 95 340 Q 98 360, 120 365 L 270 365 Q 292 360, 295 340 Q 300 290, 290 240 Q 278 178, 270 170 Q 245 160, 195 158 Q 145 160, 120 170 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 270 220 Q 300 210, 330 215 Q 345 220, 350 230" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <circle cx="405" cy="110" r="55" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <path d="M 330 170 Q 325 175, 310 240 Q 300 290, 305 340 Q 308 360, 330 365 L 480 365 Q 502 360, 505 340 Q 510 290, 500 240 Q 488 178, 480 170 Q 455 160, 405 158 Q 355 160, 330 170 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 330 220 Q 305 210, 280 215 Q 265 220, 260 230" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 275 230 Q 300 245, 325 230" fill="none" stroke="#141413" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M 280 248 Q 300 260, 320 248" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 6. Open Book
**Topics**: Fundamentals, Basics, Learning, Knowledge, Documentation, Reading, Education

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 120 Q 295 115, 100 140 Q 70 145, 65 170 L 65 380 Q 68 400, 100 395 Q 295 375, 300 370 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 300 120 Q 305 115, 500 140 Q 530 145, 535 170 L 535 380 Q 532 400, 500 395 Q 305 375, 300 370 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="300" y1="120" x2="300" y2="370" stroke="#141413" stroke-width="3"/>
  <line x1="130" y1="195" x2="260" y2="180" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="130" y1="230" x2="260" y2="215" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="130" y1="265" x2="260" y2="250" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="130" y1="300" x2="240" y2="288" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="340" y1="180" x2="470" y2="195" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="340" y1="215" x2="470" y2="230" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="340" y1="250" x2="470" y2="265" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="340" y1="288" x2="450" y2="300" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 7. Lightbulb
**Topics**: Ideas, Creativity, Innovation, Insight, Brainstorming, Inspiration

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 50 Q 200 55, 170 140 Q 145 215, 195 290 Q 220 330, 235 360 L 365 360 Q 380 330, 405 290 Q 455 215, 430 140 Q 400 55, 300 50 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 240 360 L 240 400 Q 242 425, 300 428 Q 358 425, 360 400 L 360 360" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <line x1="255" y1="380" x2="345" y2="380" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="260" y1="400" x2="340" y2="400" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 260 180 Q 250 210, 260 250" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="300" y1="30" x2="300" y2="10" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="420" y1="80" x2="440" y2="65" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="180" y1="80" x2="160" y2="65" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 8. Lock
**Topics**: Security, Safety, Privacy, Authentication, Compliance, Encryption

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 195 210 L 195 150 Q 195 60, 300 58 Q 405 60, 405 150 L 405 210" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <rect x="160" y="210" width="280" height="220" rx="20" ry="20" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <circle cx="300" cy="305" r="28" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="300" y1="330" x2="300" y2="375" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
</svg>
```

### 9. Gear / Cog
**Topics**: Settings, Configuration, Systems, Processes, Mechanics, Engine

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 275 60 L 325 60 L 335 110 Q 370 120, 390 145 L 440 125 L 465 165 L 425 200 Q 435 230, 430 260 L 480 285 L 465 330 L 410 320 Q 390 345, 365 360 L 375 415 L 330 435 L 305 385 Q 295 388, 280 385 L 260 435 L 215 415 L 230 360 Q 205 345, 190 320 L 135 330 L 120 285 L 170 260 Q 165 230, 175 200 L 135 165 L 160 125 L 210 145 Q 230 120, 265 110 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="300" cy="250" r="60" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <circle cx="300" cy="250" r="25" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
</svg>
```

### 10. Hourglass
**Topics**: Time, Waiting, Deadline, Context window, Duration, Scheduling

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <line x1="190" y1="50" x2="410" y2="50" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <line x1="190" y1="450" x2="410" y2="450" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <path d="M 210 50 Q 208 140, 250 200 Q 285 240, 300 250 Q 315 240, 350 200 Q 392 140, 390 50" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 210 450 Q 208 360, 250 300 Q 285 260, 300 250 Q 315 260, 350 300 Q 392 360, 390 450" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 250 420 Q 300 390, 350 420" fill="none" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 260 400 Q 300 375, 340 400" fill="none" stroke="#141413" stroke-width="2" stroke-linecap="round"/>
  <circle cx="300" cy="250" r="5" fill="#141413"/>
</svg>
```

### 11. Compass
**Topics**: Navigation, Direction, Reference, Guidance, Exploration, Strategy

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <circle cx="300" cy="250" r="170" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <circle cx="300" cy="250" r="140" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <path d="M 300 130 L 320 240 L 300 250 L 280 240 Z" fill="#141413" stroke="#141413" stroke-width="2"/>
  <path d="M 300 370 L 320 260 L 300 250 L 280 260 Z" fill="#FAF8F2" stroke="#141413" stroke-width="2"/>
  <path d="M 180 250 L 290 230 L 300 250 L 290 270 Z" fill="#FAF8F2" stroke="#141413" stroke-width="2"/>
  <path d="M 420 250 L 310 230 L 300 250 L 310 270 Z" fill="#141413" stroke="#141413" stroke-width="2"/>
  <circle cx="300" cy="250" r="8" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
</svg>
```

### 12. Folder
**Topics**: Files, Organization, Structure, File system, Storage, Archive

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 100 150 L 100 120 Q 102 95, 130 93 L 250 93 Q 270 95, 280 115 L 300 150" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <rect x="80" y="150" width="440" height="260" rx="15" ry="15" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <line x1="150" y1="260" x2="350" y2="260" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="150" y1="300" x2="300" y2="300" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 13. Puzzle Piece
**Topics**: Problem-solving, Integration, Patterns, Modularity, Fit, Compatibility

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 150 100 L 250 100 Q 250 70, 280 65 Q 310 60, 320 70 Q 335 85, 320 100 L 450 100 L 450 200 Q 480 200, 485 230 Q 490 260, 480 270 Q 465 285, 450 270 L 450 380 L 320 380 Q 320 410, 290 415 Q 260 420, 250 410 Q 235 395, 250 380 L 150 380 L 150 270 Q 120 270, 115 240 Q 110 210, 120 200 Q 135 185, 150 200 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
</svg>
```

### 14. Bar Chart
**Topics**: Data, Analytics, Metrics, Evaluation, Reporting, Statistics, Dashboard

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <line x1="100" y1="400" x2="520" y2="400" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <line x1="100" y1="100" x2="100" y2="400" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <rect x="140" y="280" width="65" height="120" rx="5" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <rect x="230" y="200" width="65" height="200" rx="5" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <rect x="320" y="140" width="65" height="260" rx="5" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <rect x="410" y="230" width="65" height="170" rx="5" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <path d="M 172 260 Q 262 170, 352 120 Q 420 95, 442 210" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round" stroke-dasharray="8,6"/>
</svg>
```

### 15. Chain Links
**Topics**: Linking, Chaining, Connections, Dependencies, Blockchain, Prompt chaining

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 200 150 Q 200 100, 250 100 L 350 100 Q 400 100, 400 150 L 400 250 Q 400 300, 350 300 L 310 300" fill="none" stroke="#141413" stroke-width="7" stroke-linecap="round"/>
  <path d="M 400 250 Q 400 200, 350 200 L 250 200 Q 200 200, 200 250 L 200 350 Q 200 400, 250 400 L 350 400 Q 400 400, 400 350" fill="none" stroke="#141413" stroke-width="7" stroke-linecap="round"/>
  <path d="M 290 200 L 250 200 Q 200 200, 200 250" fill="none" stroke="#FAF8F2" stroke-width="12"/>
  <path d="M 290 200 L 250 200 Q 200 200, 200 250" fill="none" stroke="#141413" stroke-width="7" stroke-linecap="round"/>
</svg>
```

### 16. Shield
**Topics**: Protection, Defense, Trust, Verification, Firewall

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 50 Q 180 60, 130 100 Q 120 110, 120 150 L 120 250 Q 125 350, 200 400 Q 260 440, 300 460 Q 340 440, 400 400 Q 475 350, 480 250 L 480 150 Q 480 110, 470 100 Q 420 60, 300 50 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 250 250 L 285 290 L 365 195" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 17. Wrench
**Topics**: Tools, Maintenance, Repair, Setup, DevOps, Tooling

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 380 80 Q 430 60, 470 80 Q 510 105, 520 155 Q 525 190, 505 225 L 360 370 Q 340 395, 310 395 Q 275 395, 258 372 Q 240 350, 245 320 Q 250 295, 270 275 L 415 130 Q 395 110, 380 80 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 270 275 L 150 395 Q 130 420, 140 445 Q 150 465, 175 465 Q 200 465, 220 445 L 340 320" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <circle cx="175" cy="440" r="8" fill="#141413"/>
</svg>
```

### 18. Pencil
**Topics**: Writing, Editing, Drafting, Authoring, Content creation, Copywriting

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 420 50 Q 430 42, 445 48 L 475 78 Q 482 88, 475 98 L 210 420 Q 205 428, 195 430 L 120 450 Q 108 454, 105 442 L 115 365 Q 116 355, 125 348 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="170" y1="355" x2="430" y2="90" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="200" y1="385" x2="460" y2="120" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 125 348 L 115 365 L 120 450 L 195 430 L 210 420" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
  <line x1="120" y1="450" x2="175" y2="395" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 19. Stacked Books
**Topics**: Library, Reference, Documentation, Study, Resources, Handbook

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <rect x="140" y="320" width="320" height="55" rx="6" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="165" y1="325" x2="165" y2="370" stroke="#141413" stroke-width="3"/>
  <rect x="155" y="260" width="290" height="55" rx="6" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="180" y1="265" x2="180" y2="310" stroke="#141413" stroke-width="3"/>
  <rect x="170" y="200" width="260" height="55" rx="6" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <line x1="195" y1="205" x2="195" y2="250" stroke="#141413" stroke-width="3"/>
  <path d="M 200 195 L 200 120 Q 202 100, 220 98 L 380 98 Q 398 100, 400 120 L 400 195" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <line x1="300" y1="105" x2="300" y2="190" stroke="#141413" stroke-width="3"/>
  <line x1="240" y1="135" x2="290" y2="135" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="240" y1="160" x2="280" y2="160" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 20. Ascending Stairs
**Topics**: Progress, Growth, Steps, Milestones, Iteration, Leveling up

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 80 420 L 180 420 L 180 330 L 300 330 L 300 240 L 420 240 L 420 150 L 540 150 L 540 420" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 130 400 Q 155 370, 180 310" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round"/>
  <path d="M 240 310 Q 265 280, 300 220" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round"/>
  <path d="M 360 220 Q 385 190, 420 130" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round"/>
  <path d="M 460 130 Q 490 95, 530 70" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round"/>
</svg>
```

### 21. Globe
**Topics**: International, Global, Localization, i18n, Worldwide, Internet, Web

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <circle cx="300" cy="250" r="170" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <ellipse cx="300" cy="250" rx="80" ry="170" fill="none" stroke="#141413" stroke-width="3"/>
  <line x1="130" y1="250" x2="470" y2="250" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 145 170 Q 300 200, 455 170" fill="none" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 145 330 Q 300 300, 455 330" fill="none" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 22. Cloud
**Topics**: Cloud computing, SaaS, Hosting, Infrastructure, AWS, Serverless

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 160 310 Q 100 310, 95 260 Q 90 215, 135 200 Q 130 150, 185 130 Q 230 112, 275 135 Q 310 95, 365 90 Q 430 85, 460 130 Q 510 120, 530 160 Q 555 200, 520 240 Q 540 275, 510 310 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="220" y1="350" x2="220" y2="390" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="300" y1="350" x2="300" y2="410" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="380" y1="350" x2="380" y2="380" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 205 390 L 235 390" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 285 410 L 315 410" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 365 380 L 395 380" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 23. Clipboard with Checklist
**Topics**: Checklist, Tasks, To-do, Requirements, Acceptance criteria, Audit

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <rect x="150" y="80" width="300" height="380" rx="15" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <path d="M 250 60 L 250 80 Q 250 100, 270 100 L 330 100 Q 350 100, 350 80 L 350 60 Q 348 45, 330 42 L 270 42 Q 252 45, 250 60 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <rect x="195" y="155" width="20" height="20" rx="3" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <path d="M 198 165 L 205 172 L 215 157" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="235" y1="165" x2="400" y2="165" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <rect x="195" y="210" width="20" height="20" rx="3" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <path d="M 198 220 L 205 227 L 215 212" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="235" y1="220" x2="380" y2="220" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <rect x="195" y="265" width="20" height="20" rx="3" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <line x1="235" y1="275" x2="360" y2="275" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <rect x="195" y="320" width="20" height="20" rx="3" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <line x1="235" y1="330" x2="390" y2="330" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 24. Eye
**Topics**: Vision, Perception, Monitoring, Observability, Review, Oversight

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 60 250 Q 150 120, 300 115 Q 450 120, 540 250 Q 450 380, 300 385 Q 150 380, 60 250 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="300" cy="250" r="80" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <circle cx="300" cy="250" r="40" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
  <circle cx="285" cy="235" r="12" fill="#141413"/>
</svg>
```

### 25. Scales / Balance
**Topics**: Trade-offs, Balance, Comparison, Justice, Fairness, A/B testing

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <line x1="300" y1="60" x2="300" y2="400" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <line x1="120" y1="140" x2="480" y2="140" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <circle cx="300" cy="60" r="15" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <path d="M 120 140 L 90 280 Q 88 300, 120 310 Q 180 320, 210 310 Q 240 300, 238 280 L 210 140" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 390 140 L 360 250 Q 358 270, 390 280 Q 450 290, 480 280 Q 510 270, 508 250 L 480 140" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <rect x="275" y="390" width="50" height="30" rx="5" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
</svg>
```

### 26. Warning Triangle
**Topics**: Errors, Warnings, Alerts, Exceptions, Risk, Caution, Error handling

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 60 Q 295 55, 80 415 Q 72 430, 85 442 L 515 442 Q 528 430, 520 415 Q 305 55, 300 60 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="300" y1="175" x2="300" y2="320" stroke="#141413" stroke-width="7" stroke-linecap="round"/>
  <circle cx="300" cy="375" r="12" fill="#141413"/>
</svg>
```

### 27. Circular Arrows (Cycle)
**Topics**: Iteration, Cycles, CI/CD, Refresh, Loop, Continuous improvement

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 80 Q 430 80, 470 180 Q 510 280, 440 370" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <path d="M 440 370 L 460 340 L 470 380" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 440 370 Q 370 440, 250 420 Q 140 395, 120 290" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <path d="M 120 290 L 100 320 L 90 280" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 120 290 Q 100 180, 200 120 Q 250 90, 300 80" fill="none" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <path d="M 300 80 L 320 105 L 280 105" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 28. Paper Airplane
**Topics**: Sending, Email, Message, Notification, Delivery, Outreach

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 100 230 L 500 100 L 350 410 L 280 280 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="500" y1="100" x2="280" y2="280" stroke="#141413" stroke-width="4"/>
  <line x1="280" y1="280" x2="280" y2="380" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 280 380 Q 290 350, 320 340" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 29. Map Pin / Location
**Topics**: Location, Maps, Geography, Local, Place, Address, Geolocation

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 440 Q 295 435, 190 290 Q 140 215, 145 155 Q 150 80, 300 60 Q 450 80, 455 155 Q 460 215, 410 290 Q 305 435, 300 440 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="300" cy="170" r="55" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <circle cx="300" cy="170" r="25" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
</svg>
```

### 30. Bell (Notification)
**Topics**: Notifications, Alerts, Reminders, Events, Webhooks, Triggers

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 55 Q 298 50, 300 45 Q 302 40, 305 45 Q 308 50, 305 55" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
  <path d="M 300 55 Q 210 70, 185 160 Q 165 240, 155 310 Q 148 350, 130 370 L 470 370 Q 452 350, 445 310 Q 435 240, 415 160 Q 390 70, 300 55 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="130" y1="370" x2="470" y2="370" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 260 380 Q 265 415, 300 418 Q 335 415, 340 380" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round"/>
</svg>
```

### 31. Heart
**Topics**: Health, Wellness, Favorites, Likes, User satisfaction, Care

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 420 Q 150 320, 100 230 Q 60 155, 110 100 Q 160 50, 220 70 Q 270 90, 300 140 Q 330 90, 380 70 Q 440 50, 490 100 Q 540 155, 500 230 Q 450 320, 300 420 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 195 130 Q 165 140, 150 175" fill="none" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
</svg>
```

### 32. Key
**Topics**: API keys, Tokens, Access, Permissions, Authorization, Credentials

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <circle cx="210" cy="200" r="90" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <circle cx="210" cy="200" r="40" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
  <path d="M 290 230 L 490 230 L 490 280 L 460 280 L 460 260 L 430 260 L 430 280 L 400 280 L 400 260" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
</svg>
```

### 33. Telescope
**Topics**: Vision, Long-term, Roadmap, Forecast, Future, Research, Exploration

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 100 160 Q 95 150, 105 140 L 420 70 Q 435 65, 440 80 L 470 160 Q 475 175, 460 180 L 145 250 Q 130 255, 125 240 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <line x1="400" y1="78" x2="430" y2="170" stroke="#141413" stroke-width="3"/>
  <path d="M 240 230 L 200 430 Q 198 445, 185 445 L 175 445" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 280 220 L 340 430 Q 342 445, 355 445 L 365 445" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
</svg>
```

### 34. Microphone
**Topics**: Voice, Audio, Podcast, Recording, Speech, Presentation, Talk

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <rect x="240" y="60" width="120" height="220" rx="60" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <line x1="270" y1="120" x2="330" y2="120" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="270" y1="160" x2="330" y2="160" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <line x1="270" y1="200" x2="330" y2="200" stroke="#141413" stroke-width="3" stroke-linecap="round"/>
  <path d="M 170 220 Q 170 340, 300 345 Q 430 340, 430 220" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <line x1="300" y1="345" x2="300" y2="420" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <line x1="230" y1="420" x2="370" y2="420" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
</svg>
```

### 35. Laptop / Screen
**Topics**: Computing, Software, Interface, UI, Desktop, Development, Code

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <rect x="130" y="80" width="340" height="250" rx="12" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <rect x="155" y="105" width="290" height="195" rx="4" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
  <line x1="185" y1="155" x2="320" y2="155" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="185" y1="185" x2="280" y2="185" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="185" y1="215" x2="350" y2="215" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 100 340 L 130 330 L 470 330 L 500 340 Q 510 348, 500 355 L 100 355 Q 90 348, 100 340 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
</svg>
```

### 36. Camera
**Topics**: Photography, Image, Snapshot, Screenshot, Visual, Media

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 220 120 L 250 80 Q 255 72, 265 72 L 335 72 Q 345 72, 350 80 L 380 120" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <rect x="100" y="120" width="400" height="280" rx="20" fill="#FAF8F2" stroke="#141413" stroke-width="6"/>
  <circle cx="300" cy="260" r="85" fill="#FAF8F2" stroke="#141413" stroke-width="5"/>
  <circle cx="300" cy="260" r="55" fill="#FAF8F2" stroke="#141413" stroke-width="4"/>
  <circle cx="270" cy="235" r="15" fill="#FAF8F2" stroke="#141413" stroke-width="2"/>
  <circle cx="440" cy="165" r="12" fill="#FAF8F2" stroke="#141413" stroke-width="3"/>
</svg>
```

### 37. Plant / Seedling
**Topics**: Growth, Nurturing, Sustainability, Environment, Organic, Cultivation

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 300 420 Q 298 350, 300 280 Q 302 220, 300 180" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 300 280 Q 230 250, 200 190 Q 180 140, 220 110 Q 260 85, 300 120 Q 310 140, 300 180" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 300 220 Q 370 190, 400 130 Q 420 80, 380 55 Q 340 35, 300 70 Q 290 90, 300 130" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 300 180 Q 250 175, 230 150" fill="none" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 300 130 Q 350 125, 370 100" fill="none" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M 180 420 Q 240 400, 300 420 Q 360 440, 420 420" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
</svg>
```

### 38. Flag
**Topics**: Milestones, Goals, Feature flags, Checkpoints, Achievements, Markers

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <line x1="180" y1="60" x2="180" y2="440" stroke="#141413" stroke-width="6" stroke-linecap="round"/>
  <path d="M 180 80 Q 280 50, 350 90 Q 420 130, 480 100 L 480 270 Q 420 300, 350 260 Q 280 220, 180 250 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
  <line x1="250" y1="120" x2="400" y2="140" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="250" y1="155" x2="380" y2="170" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="230" y1="190" x2="360" y2="200" stroke="#141413" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

### 39. Trophy / Cup
**Topics**: Achievement, Award, Competition, Success, Winner, Gamification

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 200 80 L 200 200 Q 205 300, 300 320 Q 395 300, 400 200 L 400 80 Z" fill="#FAF8F2" stroke="#141413" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 200 120 Q 150 120, 130 160 Q 110 210, 150 250 Q 175 270, 210 240" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 400 120 Q 450 120, 470 160 Q 490 210, 450 250 Q 425 270, 390 240" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <line x1="300" y1="320" x2="300" y2="380" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 230 380 L 370 380 L 380 410 L 220 410 Z" fill="#FAF8F2" stroke="#141413" stroke-width="5" stroke-linejoin="round"/>
</svg>
```

### 40. Fingerprint
**Topics**: Identity, Biometrics, Unique, Authentication, Persona, User profile

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="500" viewBox="0 0 600 500">
  <path d="M 210 350 Q 180 280, 190 200 Q 200 130, 300 110 Q 400 130, 410 200" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 240 370 Q 220 310, 230 230 Q 240 165, 300 150 Q 360 165, 370 230" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 275 380 Q 265 320, 270 260 Q 280 200, 300 190 Q 320 200, 330 260 Q 335 320, 325 380" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 360 360 Q 375 290, 370 230 Q 365 170, 340 155" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
  <path d="M 390 340 Q 410 260, 400 190" fill="none" stroke="#141413" stroke-width="5" stroke-linecap="round"/>
</svg>
```

---

## Creating New Illustrations

When a topic doesn't match any existing illustration, create a new SVG following these rules:

1. **ViewBox**: Always `width="600" height="500" viewBox="0 0 600 500"`
2. **Fill**: Always `#FAF8F2`
3. **Stroke**: Always `#141413`, main outlines 5-7px, detail lines 2.5-3.5px
4. **Style**: Use Bezier curves (`Q`, `C`) for organic feel — avoid perfect geometry
5. **Complexity**: 2-5 main shapes, keep it simple and iconic
6. **No decorations**: Avoid scattered dots, sparkles, or decorative elements
7. **Test**: Render at 900x750px to verify it looks good at slide scale

The aesthetic should always feel like a casual pen-and-ink whiteboard sketch — charming
imperfection is the goal. If it looks too precise, add slight offsets to coordinates.
