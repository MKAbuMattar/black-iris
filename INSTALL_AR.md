# تثبيت black-iris

مجلد مهارة واحد، `skills/black-iris/`، يعمل في كل وكيل يقرأ Agent Skills. كل
المسارات أدناه تنتهي بالشيء نفسه: هذا المجلد، مع مراجعه، في مكان يفحصه
وكيلك. Claude Code وحده يحصل أيضاً على خطاف SessionStart؛ بقية الوكلاء تحصل
على المهارة ويمكنها إضافة مقتطف دائم التفعيل يدوياً.

تفترض الأوامر أن المستودع منشور على `github.com/MKAbuMattar/black-iris`. إلى
أن يُنشر، استخدم مسارات الملفات المحلية.

ما تشترك فيه كل المسارات:

- استدعِ بالاسم. `/black-iris` حيث توجد مهارات الشرطة المائلة، و`$black-iris`
  في Codex، أو اطلبها بالكلمات. تبقى Shape وBuild وقائمة Cut فعّالة حتى
  "stop black-iris" أو "normal mode".
- ملفات كل مشروع تذهب إلى `~/.BLACK_IRIS_AGENTS/projects/<slug>/`. لا يُكتب
  شيء في مستودعك أو في `~/.claude`.
- علَم التفعيل الدائم:
  `mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/always-on`.
  مسار إضافة Claude Code وحده يقرأه.

## Claude Code

مسار الإضافة، يعطي المهارة والخطاف:

```bash
claude plugin marketplace add MKAbuMattar/black-iris
claude plugin install black-iris@black-iris
```

مسار الإضافة المحلي، دون نشر، جلسة واحدة في كل مرة:

```bash
claude --plugin-dir /path/to/black-iris
```

مسار المهارة فقط، دون خطاف:

```bash
python3 skills/black-iris/scripts/universal/install.py               # رابط في ~/.claude/skills
python3 skills/black-iris/scripts/universal/install.py --always-on   # مع تفعيل العلَم أيضاً
python3 skills/black-iris/scripts/universal/install.py --uninstall
```

`scripts/linux/install.sh` و`scripts/mac/install.sh` و
`scripts/windows/install.ps1` تفعل الشيء نفسه في صدفة كل منصة.

التحقق: ابدأ جلسة جديدة واكتب `/black-iris`، أو شغّل `claude plugin list`.
التحديث: `claude plugin marketplace update black-iris`. الإزالة:
`claude plugin uninstall black-iris` ثم `claude plugin marketplace remove black-iris`.

مع تفعيل العلَم وتحميل الإضافة، يُعاد حقن جسم المهارة والمراجع التسعة
و`MEMORY.md` الخاص بالمشروع عند كل بداية جلسة واستئناف ومسح وضغط، نحو 1700 سطر. من دون الإضافة لا يفعل العلَم
شيئاً.

Claude for IDE (إضافتا VS Code وJetBrains) يشغّل Claude Code نفسه في الخلفية
ويقرأ `~/.claude/skills` وقائمة الإضافات نفسها. أي مسار أعلاه يغطيه؛ افتح
محادثة جديدة في المحرر بعد التثبيت.

## Codex

```bash
codex plugin marketplace add MKAbuMattar/black-iris --ref main
codex plugin add black-iris@black-iris
```

يشحن المستودع `.codex-plugin/plugin.json` وملف سوق Codex في
`.agents/plugins/marketplace.json`، وهو ما يقرأه الأمر الأول. اكتب
`$black-iris`. تسمح المهارة بالاستدعاء الضمني، فقد يلتقطها Codex من
الوصف أيضاً. بديل المهارة فقط:

```bash
npx skills add MKAbuMattar/black-iris -a codex        # أو انسخ skills/black-iris إلى ~/.codex/skills/
```

التحديث: `codex plugin marketplace upgrade black-iris` ثم أزل وأضف. الإزالة:
`codex plugin remove black-iris` و`codex plugin marketplace remove black-iris`.
التفعيل الدائم: الصق المقتطف في نهاية هذا الملف داخل `~/.codex/AGENTS.md`.

## Kimi Code CLI

داخل الجلسة: `/plugins`، اختر Custom، الصق
`https://github.com/MKAbuMattar/black-iris`، اختر Trust and install. استدعِ
بـ `/skill:black-iris`. التحديث: `/plugins`، حرّك المؤشر إلى Black Iris، اضغط
`R`. الإزالة: القائمة نفسها، اضغط `D`.

## Gemini CLI

```bash
gemini extensions install https://github.com/MKAbuMattar/black-iris
```

تحمّل الإضافة `GEMINI.md` الذي يستورد المهارة كاملة، فتنطبق القواعد من أول
رسالة. هذا المسار دائم التفعيل بطبيعته. يحتاج `git`. التحقق:
`gemini extensions list`. التحديث: `gemini extensions update black-iris`.
الإزالة: `gemini extensions uninstall black-iris`.

## OpenCode

يقرأ OpenCode مهارات Agent Skills أصلاً ويستدعيها النموذج عبر أداة المهارات
من الوصف.

```bash
npx skills add MKAbuMattar/black-iris -a opencode -y     # مساحة العمل هذه
npx skills add MKAbuMattar/black-iris -a opencode -g -y  # كل المشاريع
```

يدوياً: انسخ `skills/black-iris` إلى `.agents/skills/` في المشروع أو إلى
`~/.config/opencode/skills/`. اطلبها بالكلمات ("use black-iris"). لا خطاف ولا
علَم؛ الصق المقتطف أدناه في `~/.config/opencode/AGENTS.md`.

## Z Code

يقرأ Z Code مهارات Agent Skills من `~/.zcode/skills/<skill-name>/SKILL.md`
ويسمح للمهارة بالإشارة إلى ملفات أخرى في مجلدها، فتُحل المراجع.

```bash
mkdir -p ~/.zcode/skills
cp -R skills/black-iris ~/.zcode/skills/
```

أو في Z Code: Settings ثم Skills ثم Import، ووجّهه إلى `skills/black-iris`
كـ Symlink (يتابع هذا المستودع) أو Copy، Global أو Project. اضغط Refresh إن لم
يظهر مجلد منسوخ يدوياً. استدعِ بـ `$black-iris` في المحادثة، أو من مجموعة
Skills في قائمة `/`. أزل بحذف المجلد أو الاستيراد. لا خطاف ولا علَم؛ استخدم
المقتطف أدناه في قواعد Z Code.

## DeepSeek Harness (dsh)

يقرأ dsh مهارات Agent Skills كمجلدات `<name>/SKILL.md` من، بترتيب الأولوية:
`<project>/.dsh/skills` و`<project>/.agents/skills` وأي `customSkillDirs` في
الإعدادات و`~/.dsh/skills` و`~/.agents/skills`. جذر المشروع هو أقرب مجلد
يحوي `.git`. يجب أن يطابق اسم المجلد `name` في الترويسة، وهذا متحقق، وتُحل
مسارات `references/` النسبية عبر مجلد المهارة.

```bash
mkdir -p ~/.dsh/skills
cp -R skills/black-iris ~/.dsh/skills/                              # كل المشاريع
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/  # هذا المشروع فقط
```

`npx skills add MKAbuMattar/black-iris -a codex` يضعها في `.agents/skills/`
الذي يفحصه dsh أيضاً. انسخ بدلاً من الربط؛ تتبّع الروابط الرمزية إعداد في
المزوّد قد يكون معطلاً. يحترم dsh مفتاحي الترويسة `disable-model-invocation`
و`user-invocable` كما يفعل Claude Code، وكلاهما true افتراضياً، لذا تكون
black-iris متاحة لأداة المهارات في النموذج ولك بالاسم. لا خطاف ولا علَم؛ ضع
المقتطف أدناه في system prompt الخاص بالملف الشخصي أو في `AGENTS.md`. مسار
الإضافة (`dsh plugin add github:<owner>/<repo>`) يحتاج إضافة Cordis تسجّل
SkillProvider؛ لا تشحن black-iris واحدة، لأن جذر المهارات يؤدي المهمة نفسها.

## T3 Code

T3 Code واجهة سطح مكتب تشغّل Codex أو Claude Code في الخلفية. لا مخزن مهارات
خاصاً به. ثبّت black-iris في الوكيل الذي يستخدمه T3 Code، بمسار Claude Code أو
Codex أعلاه، ثم استدعِها في محادثة T3 Code بالطريقة نفسها. مع مسار إضافة
Claude Code يعمل الخطاف هناك أيضاً.

## GitHub Copilot (VS Code وCopilot CLI)

يقرأ Copilot مهارات Agent Skills أصلاً من `.github/skills/` و`.claude/skills/`
و`.agents/skills/` في المشروع، ومن `~/.copilot/skills/` و`~/.claude/skills/`
و`~/.agents/skills/` عالمياً.

```bash
npx skills add MKAbuMattar/black-iris -a github-copilot        # هذا المشروع
npx skills add MKAbuMattar/black-iris -a github-copilot -g     # كل المشاريع
```

يدوياً: `cp -R skills/black-iris ~/.copilot/skills/`. اكتب `/black-iris` في
المحادثة. تثبيت المهارة فقط في Claude Code يكفي Copilot أيضاً، لأنه يفحص
`~/.claude/skills/`. التحديث: `npx skills update black-iris`. الإزالة:
`npx skills remove black-iris`. التفعيل الدائم: المقتطف أدناه في
`.github/copilot-instructions.md`.

## Zed

يقرأ وكيل Zed مهارات Agent Skills. انسخ المجلد كاملاً، لأن الاستيراد عبر
الرابط يأخذ SKILL.md فقط وblack-iris تحتاج مجلد `references/`:

```bash
cp -R skills/black-iris ~/.config/zed/skills/
```

اكتب `/black-iris` في Agent Panel. تحقق في مدير Skills. الإزالة: احذف
`~/.config/zed/skills/black-iris`. التفعيل الدائم: المقتطف أدناه في
`~/.config/zed/AGENTS.md`.

## Hermes

```bash
hermes skills install MKAbuMattar/black-iris/skills/black-iris
```

اكتب `/black-iris`. التحقق: `hermes skills list`. التحديث:
`hermes skills update black-iris`. الإزالة: `hermes skills uninstall black-iris`.
التفعيل الدائم: المقتطف أدناه في `AGENTS.md` الخاص بمجلد العمل، أو في
`SOUL.md` الخاص بالشخصية لكل الجلسات.

## Pi

```bash
pi install https://github.com/MKAbuMattar/black-iris
```

تعرض الحزمة المهارة؛ اكتب `/skill:black-iris`. التحقق: `pi list`. التحديث:
`pi update https://github.com/MKAbuMattar/black-iris`. الإزالة:
`pi remove https://github.com/MKAbuMattar/black-iris`. لا تُشحن إضافة Pi، فلا
مفتاح في التذييل ولا علَم تفعيل دائم في Pi.

## Antigravity

```bash
agy plugin install https://github.com/MKAbuMattar/black-iris
```

التحقق: `agy plugin list`. التحديث: أزل ثم ثبّت. الإزالة:
`agy plugin uninstall black-iris`، أو `agy plugin disable black-iris`
للاحتفاظ بها. التفعيل الدائم: المقتطف أدناه في `~/.gemini/GEMINI.md`.

## Cline

```bash
npx skills add MKAbuMattar/black-iris -a cline        # هذا المشروع، .agents/skills/
npx skills add MKAbuMattar/black-iris -a cline -g     # كل المشاريع، ~/.agents/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.agents/skills/` أو `~/.agents/skills/`.
اطلبها بالاسم في المحادثة. التفعيل الدائم: المقتطف أدناه في `.clinerules`.

## TRAE

```bash
npx skills add MKAbuMattar/black-iris -a trae         # هذا المشروع، .trae/skills/
npx skills add MKAbuMattar/black-iris -a trae -g      # كل المشاريع، ~/.trae/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.trae/skills/` أو `~/.trae/skills/`.
التفعيل الدائم: المقتطف أدناه في قواعد مشروع TRAE.

## Qoder

```bash
npx skills add MKAbuMattar/black-iris -a qoder        # هذا المشروع، .qoder/skills/
npx skills add MKAbuMattar/black-iris -a qoder -g     # كل المشاريع، ~/.qoder/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.qoder/skills/` أو `~/.qoder/skills/`.
التفعيل الدائم: المقتطف أدناه في قواعد Qoder.

## Droid (Factory)

```bash
npx skills add MKAbuMattar/black-iris -a droid        # هذا المشروع، .agents/skills/
npx skills add MKAbuMattar/black-iris -a droid -g     # كل المشاريع، ~/.factory/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.agents/skills/` أو `~/.factory/skills/`.
أعد تشغيل `droid` ليعيد فحص المهارات؛ يستدعي من تلقاء نفسه المهارات التي
تطابق الوصف. التفعيل الدائم: المقتطف أدناه في `AGENTS.md`.

## Kilo Code

```bash
npx skills add MKAbuMattar/black-iris -a kilo         # هذا المشروع، .agents/skills/
npx skills add MKAbuMattar/black-iris -a kilo -g      # كل المشاريع، ~/.kilo/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.agents/skills/` أو `~/.kilo/skills/`.
التفعيل الدائم: المقتطف أدناه في `.kilocode/rules/`.

## Roo Code

```bash
npx skills add MKAbuMattar/black-iris -a roo          # هذا المشروع، .roo/skills/
npx skills add MKAbuMattar/black-iris -a roo -g       # كل المشاريع، ~/.roo/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.roo/skills/` أو `~/.roo/skills/`.
التفعيل الدائم: المقتطف أدناه في `.roo/rules/`.

## Crush

```bash
npx skills add MKAbuMattar/black-iris -a crush        # هذا المشروع، .crush/skills/
npx skills add MKAbuMattar/black-iris -a crush -g     # كل المشاريع، ~/.config/crush/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `.crush/skills/` أو
`~/.config/crush/skills/`. التفعيل الدائم: المقتطف أدناه في `CRUSH.md` أو
`AGENTS.md`، اللذين يقرأهما Crush كسياق.

## Goose

يقرأ Goose `.goose/skills/` و`.agents/skills/` في المشروع
و`~/.config/goose/skills/` عالمياً، ويلتقط أيضاً `~/.claude/skills/`، فتثبيت
المهارة فقط في Claude Code يغطيه من الأصل. يجب أن يطابق اسم المجلد اسم
الترويسة، وهذا متحقق.

```bash
npx skills add MKAbuMattar/black-iris -a goose        # هذا المشروع، .goose/skills/
npx skills add MKAbuMattar/black-iris -a goose -g     # كل المشاريع، ~/.config/goose/skills/
```

التفعيل الدائم: المقتطف أدناه في `.goosehints`.

## Eigent

يشحن Eigent فهرس مهارات: `npx @eigent-ai/agent-skills list` و
`npx @eigent-ai/agent-skills install <name>`. لا تذكر وثائقه أين تُخزَّن على
القرص ولا كيف تُضاف مهارة من خارج الفهرس، فلا مسار مُتحقَّق منه لـ black-iris
بعد. ما يعمل اليوم: الصق المقتطف الدائم أدناه في system prompt الوكيل أو في
تعليمات المهمة، واحتفظ بـ `skills/black-iris` في مجلد مساحة عمل يمكن للوكيل
قراءته، واطلبها بالاسم. افتح مشكلة إن وجدت مسار المهارات المخصصة في إعدادات
Eigent.

## OpenClaw

لدى OpenClaw مثبّت مهارات أصلي ويقرأ مجلدات `SKILL.md` بترويسة `name`
و`description`.

```bash
openclaw skills install MKAbuMattar/black-iris/skills/black-iris            # skills/ في مساحة العمل النشطة
openclaw skills install MKAbuMattar/black-iris/skills/black-iris --global   # ~/.openclaw/skills/
```

يدوياً: انسخ `skills/black-iris` إلى `~/.openclaw/skills/` أو إلى مجلد
`skills/` في مساحة العمل. تُسمّى المهارة من ترويستها، فالمجلد الفرعي مقبول.
التفعيل الدائم: المقتطف أدناه في شخصية الوكيل أو تعليمات مساحة العمل.

## SillyTavern

SillyTavern واجهة محادثة بلا محمّل مهارات. خياران صادقان:

1. الصق المقتطف الدائم أدناه في system prompt الخاص بإعدادك المسبق، أو في
   وصف بطاقة شخصية، فتنطبق Shape وقائمة Cut.
2. لنمط كامل، الصق جسم المرجع الذي تحتاجه (مثل `references/deslop.md`)
   كـ Author's Note أو كمدخل lorebook مضبوط على التفعيل الدائم، واستدعِه
   بالاسم في المحادثة.

لا خطاف، لا مخزن، لا أمر `/black-iris`.

## Qwen Code

```bash
qwen extensions install MKAbuMattar/black-iris
```

يوجّه ملف `qwen-extension.json` المرفق Qwen Code إلى `skills/`. يقرأ Qwen Code
أيضاً مهارات Agent Skills من `~/.qwen/skills/` و`.qwen/skills/` مباشرة بحسب
وثائق مهاراته، فالنسخ البسيط يعمل كذلك. اكتب `/black-iris`، أو شغّل `/skills`
لتأكيد ظهورها. التحقق: `qwen extensions list`. التحديث:
`qwen extensions update black-iris`. الإزالة:
`qwen extensions uninstall black-iris`.

## Windsurf

يقرأ Cascade `.windsurf/skills/` في المشروع و`~/.codeium/windsurf/skills/`
عالمياً بحسب وثائق مهارات Windsurf.

```bash
npx skills add MKAbuMattar/black-iris -a windsurf        # هذا المشروع
npx skills add MKAbuMattar/black-iris -a windsurf -g     # كل المشاريع
```

التفعيل الدائم: المقتطف أدناه في قاعدة Windsurf بمحفّز دائم.

## Warp

تقرأ وكلاء Warp مهارات Agent Skills من `.agents/skills/` في المشروع
و`~/.agents/skills/` عالمياً بحسب وثائق Warp.

```bash
npx skills add MKAbuMattar/black-iris -a warp            # هذا المشروع
npx skills add MKAbuMattar/black-iris -a warp -g         # كل المشاريع
```

التفعيل الدائم: المقتطف أدناه في قواعد وكيل Warp.

## Junie (JetBrains)

يقرأ Junie `.junie/skills/` في المشروع و`~/.junie/skills/` عالمياً بحسب
وثائق مهارات الوكيل لديه. انسخ `skills/black-iris` إلى أيهما. التفعيل
الدائم: المقتطف أدناه في `.junie/guidelines.md`.

## JetBrains AI Assistant

يحمّل AI Assistant مجلدات المهارات المضبوطة في Settings ثم Tools ثم AI
Assistant ثم Skills بحسب صفحة مساعدته. وجّهه إلى نسخة من `skills/black-iris`.
التفعيل الدائم: المقتطف أدناه في قواعد مشروع المساعد.

## Mistral Vibe

يتبع Vibe مواصفة Agent Skills ويقرأ `~/.vibe/skills/` و`.vibe/skills/` بحسب
وثائق Mistral Vibe. انسخ `skills/black-iris` إلى أيهما واستدعِ بالاسم.

## OpenHands

يقرأ OpenHands `.agents/skills/` (الموصى به) و`.openhands/skills/` القديم بحسب
وثائق مهاراته.

```bash
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/
```

التفعيل الدائم: المقتطف أدناه في `.openhands/microagents/repo.md`.

## أهداف أخرى لأداة skills

تعرف أداة skills مجلد المهارات لوكلاء كثيرين آخرين. هذه المسارات من جدول
الوكلاء في تلك الأداة ولم تُراجَع مع وثائق كل مورّد؛ اعتبرها نقطة بداية.

```bash
npx skills add MKAbuMattar/black-iris -a augment       # .augment/skills, ~/.augment/skills
npx skills add MKAbuMattar/black-iris -a continue      # .continue/skills, ~/.continue/skills
npx skills add MKAbuMattar/black-iris -a devin         # .devin/skills, ~/.config/devin/skills (Devin for Terminal)
npx skills add MKAbuMattar/black-iris -a tabnine       # .tabnine/agent/skills
npx skills add MKAbuMattar/black-iris -a kiro          # .kiro/skills; مقتطف المحرر يذهب إلى .kiro/steering/
npx skills add MKAbuMattar/black-iris -a replit        # .agents/skills
npx skills add MKAbuMattar/black-iris -a grok          # .grok/skills
npx skills add MKAbuMattar/black-iris --all            # كل وكيل تكتشفه الأداة على هذا الجهاز
```

تغطي الأداة نفسها الذيل الطويل: Lingma وCodeBuddy وCodeArts Agent وRovo Dev
وCortex Code وMiniMax Code وiFlow CLI وAiderDesk وZencoder وغيرها. يثبّت
`--all` في ما يجده منها.

## وكلاء بلا محمّل مهارات

Aider وAmazon Q Developer وGemini Code Assist وSourcegraph Cody وVoid وXcode
وBolt وv0 وLovable وManus وDevin السحابي لا تقرأ مجلدات مهارات. لهؤلاء، الصق
المقتطف الدائم أدناه في التعليمات الدائمة التي يقرؤونها فعلاً: قواعد Amazon
Q، أو `GEMINI.md` أو `AGENTS.md` لـ Gemini Code Assist، أو ملف قواعد المشروع
في غيرها. الأنماط التي تحتاج ملف مرجع غير متاحة هناك.

## Cursor وAmp وبقية أُطر agent-skills

```bash
npx skills add MKAbuMattar/black-iris                  # مساحة العمل هذه
npx skills add MKAbuMattar/black-iris -g               # كل المشاريع
npx skills add MKAbuMattar/black-iris -a cursor -y     # وكيل واحد فقط
npx skills add MKAbuMattar/black-iris --all            # كل وكيل تكتشفه الأداة
```

يدوياً: انسخ `skills/black-iris` إلى المسار الذي يفحصه وكيلك، مثل
`~/.cursor/skills/`. انسخ ولا تربط؛ لا يتبع Cursor الروابط الرمزية على كل
المنصات. محادثة جديدة، اكتب `/black-iris`. التحقق: `npx skills list`
(`npx skills ls -g` إن كان عالمياً). التحديث: `npx skills update black-iris`.
الإزالة: `npx skills remove black-iris`. التفعيل الدائم: Cursor Settings ثم
Rules ثم User Rules، أو قاعدة مشروع في `.cursor/rules/` مع `alwaysApply: true`.

## أي وكيل آخر (يدوياً)

1. انسخ `skills/black-iris/` كاملاً، مع `references/`، إلى المجلد الذي يفحصه
   وكيلك بحثاً عن المهارات. إن لم يفحص شيئاً، ضعه في أي مكان يمكن للوكيل
   قراءته.
2. إن لم يستطع الوكيل قراءة ترويسة YAML، أعطه الجسم فقط:

   ```bash
   awk '/^---[[:space:]]*$/ && c<2 { c++; next } c>=2' skills/black-iris/SKILL.md
   ```

   الصق ذلك في system prompt أو في ملف القواعد، وأخبر الوكيل بمكان مجلد
   `references/` لتُحل مسارات جدول التوجيه.
3. استدعِ بالاسم في أول رسالة من الجلسة.

## مقتطف التفعيل الدائم للوكلاء بلا خطاف

الصقه في ملف القواعد الدائمة للوكيل. يحمل النواة الدائمة فقط؛ بقية الأنماط ما
زالت تحتاج مجلد المهارة مثبتاً.

```markdown
## black-iris core

Shape every response for a reader with ADHD. Line one is the answer or the
action. Number multi-step work, fewest steps that work. Restate state every
turn. Numbers, thresholds, and scoped conditions stay exact. A warning is the
last thing to cut. An answer stops at its point; a deliverable ships bare.
Estimates in concrete units, saying whose time. Show what now works. Cap lists
at five. End with one action under two minutes, or the blocking question, and
nothing after it.

Build: read the flow the change touches, surface assumptions, every changed
line traces to the request, state the check before the work, minimum code in
the repo's idiom, comments carry the why.

Cut: no em or en dashes, no AI vocabulary (delve, leverage, seamless,
robust, crucial, showcase, utilize), no "not just X but Y", no filler, no
rule of three, name the actor, no decorative emoji or title case, never sign
work as AI. Delete any opener that announces and any closer that recaps.

Break these when asked to explain, before a destructive action, after three
failed fixes, or when a wrong guess costs a rewrite. "stop black-iris" turns
them off.
```

المقتطف مُبقى بالإنجليزية عن قصد: فهو نص تعليمات للنموذج، والقواعد تسمّي
كلمات إنجليزية محددة.

## التحقق من أنه يعمل

اسأل أي وكيل سؤالاً قصيراً من نوع "كيف أفعل" بعد استدعاء المهارة. يجب أن
يكون السطر الأول أمراً أو حكماً، وألا توجد شرطات طويلة ولا عرض ختامي، وأن يقف
التحذير بجانب الخطوة التي يحميها. إن ظلت الردود تبدأ بـ "Sure" أو تنتهي بـ
"Let me know"، ابدأ جلسة جديدة؛ تُفهرس المهارات عند بداية الجلسة.

## استكشاف الأخطاء

- `/black-iris` غائب من الإكمال التلقائي: أعد تشغيل الوكيل.
- علَم التفعيل الدائم بلا أثر: يحتاج مسار إضافة Claude Code، لا رابط المهارة،
  وجلسة جديدة بعد تحميل الإضافة.
- `marketplace add` يفشل: استخدم صيغة `owner/repo`، أو مساراً محلياً إلى جذر
  المستودع، لا إلى `.claude-plugin/`.
- مسار مرجع لا يُحل: وصل الوكيل إلى SKILL.md دون مجلده. أعد تثبيت مجلد
  `skills/black-iris/` كاملاً.
