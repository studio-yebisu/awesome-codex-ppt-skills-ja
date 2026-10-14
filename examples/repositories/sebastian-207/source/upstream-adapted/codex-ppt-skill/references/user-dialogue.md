# User Dialogue

Use plain Chinese when the user is Chinese. Do not expose internal engineering terms unless the user asks for implementation details. Say what will happen in normal presentation language.

## 1. 需求完整时的复核话术

Use when the user already provided topic, page count, style, and purpose. Do not ask again.

Template:

> 我理解你的需求是：做一套【页数】页的【主题】PPT，用于【使用场景/受众】，整体风格偏【风格】，交付为【输出格式】。我会按这个方向直接开始：先整理内容结构，再确定页面规划和视觉方案，最后做交付检查。

Short version:

> 信息已经够了，我会按「【主题】/【页数】页/【风格】/【用途】」来做，不再重复追问。

## 2. 需求缺失时的追问话术

Only ask missing high-impact items. Do not ask a long questionnaire.

Template:

> 我先理解一下：你想做一套关于【主题】的 PPT。为了做得更贴近用途，我还需要确认 2-3 个信息：  
> 1. 这套 PPT 主要给谁看？  
> 2. 大概需要多少页？  
> 3. 你更想要【候选风格 A】、【候选风格 B】，还是【候选风格 C】？  
> 你也可以直接说“随便”或“你看着办”，我会自动决定页数、风格和交付格式。

If only one thing is missing:

> 其他信息已经够了，我只需要再确认一个点：【缺失项】。如果你不想纠结，也可以说“你看着办”。

## 3. Auto Mode 话术

Use when the user says “随便 / 你看着办 / 直接做 / 自由发挥 / 不用问我”.

Template:

> 好，我进入自动模式，不继续追问。我会根据主题和材料自动决定页数、风格、制作路线、视觉资产和交付格式。默认会做 PPTX、PDF、每页 PNG 预览，并附上交付检查记录。

If image generation may be needed:

> 我也会逐页判断是否需要封面主视觉、概念图、流程图或场景图；需要的图会写进视觉资产计划，不会只做两张图就草草结束。

## 4. 参考 PPT 范围确认话术

Use when the user gives a reference PPT.

If scope is unclear:

> 你希望我参考这个 PPT 的哪一部分？  
> A. 只参考风格：颜色、字体、版式、图文感觉  
> B. 只参考结构：页面顺序、章节安排、叙事逻辑  
> C. 风格和结构都参考：视觉像它，组织方式也像它，但内容换成新主题  
> 如果你说“随便 / 你看着办”，我会默认参考风格 + 结构，但不照搬原内容。

When scope is clear:

> 本次我会参考【风格/结构/风格和结构】，不会参考【不参考项】。原 PPT 的内容不会被直接照搬；我会根据你的新主题重写。

When using template/layouts:

> 如果这个 PPT 里有可用的版式和占位符，我会优先沿用它们，让新 PPT 尽量保持可编辑，而不是简单叠文本框或整页截图。

## 5. 修改 PPT 话术

Default edit:

> 我会先做一份修改计划，说明哪些页会改、怎么改。默认可以优化表达和排版，但不改变核心意思、事实、数据和主要逻辑。

If the user says “不改内容”:

> 明白，这次只做视觉和排版优化：包括字体、配色、对齐、层级、图片和版面节奏；不改原文含义、不改数据、不改核心观点。

## 6. 单页修改话术

Use when the user specifies slide N.

Template:

> 明白，这次只改第【N】页。其他页面会锁定，不改内容、不改版式、不改顺序。第【N】页的新设计会继承整套 PPT 的颜色、字体、标题层级、图文密度和整体风格。

If the user asks for variants:

> 你要求多个版本，所以我会给第【N】页做 2-3 个候选方案；其他页仍然保持不动。

Default:

> 如果你没有要求多版，我会只做一个最优版本，避免方案太散。

## 7. 交付说明话术

Use at delivery.

Template:

> 我会交付这些文件：  
> - `final.pptx`：可打开和继续编辑的 PowerPoint 文件。  
> - `final.pdf`：方便预览和转发的固定版文件。  
> - 每页 PNG：逐页预览图，方便快速检查视觉效果。  
> - `qa_report.md`：交付检查记录，用来说明页数、尺寸、图片、文字溢出、占位符等是否检查过。  
> - `delivery_manifest.json`：交付清单，记录这次用了什么路线、生成了哪些文件、还有哪些已知限制。

Avoid saying:

- “你必须理解 QA 报告”
- “这是内部工程产物”
- “route/artifact/spec lock” unless the user asks

Say instead:

> 交付检查记录主要是为了让你放心：我做了哪些检查、哪里通过了、哪里还需要注意。
