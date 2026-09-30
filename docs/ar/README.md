<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/hero-ar-dark.svg">
  <img src="../../.github/assets/readme/hero-ar-light.svg" width="100%" alt="black-iris: مهارة واحدة، خمس عشرة قاعدة عمل لوكيل البرمجة، مع جدول الأنماط">
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/logo-dark.svg">
  <img src="../../.github/assets/readme/logo-light.svg" width="112" alt="black-iris logo, a geometric black iris">
</picture>
</p>

<h1 align="center">black-iris</h1>
<p align="center"><em>السوسنة السوداء</em></p>
<p align="center">مهارة واحدة، خمس عشرة قاعدة عمل لوكيل البرمجة.</p>

<p align="center"><a href="README.md">English</a> | <a href="../../docs/es/README.md">Espanol</a> | <a href="README.md">العربية</a></p>

<p align="center">مهارة واحدة لوكيل البرمجة، خمس عشرة قاعدة عمل. تُشكّل كل رد لقارئ لديه فرط الحركة ونقص الانتباه، وتحذف علامات النص المولَّد بالذكاء الاصطناعي من كل ما يكتبه الوكيل، وتُبقي تغييرات الكود دقيقة ومحدودة، وتكتب بوابات إنجاز قبل العمل الطويل، وتُطلق فروع أفكار معزولة، وتكتب أوامر لأدوات أخرى، وتُرتّب ذاكرة الجلسة، وتنقل الجلسة عبر الضغط، وتُبقي البيانات الضخمة خارج نافذة السياق، وتتولى رسائل الالتزام والتسمية ومراجعة الفروقات. موجّه من 200 سطر مع عشرة ملفات مرجعية.</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/section-install-ar-dark.svg">
  <img src="../../.github/assets/readme/section-install-ar-light.svg" width="100%" alt="التثبيت">
</picture>

Claude Code، إضافة مع خطاف بداية الجلسة:

```bash
claude plugin marketplace add MKAbuMattar/black-iris
claude plugin install black-iris@black-iris
```

أي وكيل يقرأ Agent Skills، المهارة فقط:

```bash
npx skills add MKAbuMattar/black-iris -g
```

بقية الوكلاء، ومنهم Codex وKimi وGemini CLI وOpenCode وZ Code وDeepSeek Harness
وCopilot وZed وHermes وPi وAntigravity وCursor، في [INSTALL.md](INSTALL.md).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/section-use-ar-dark.svg">
  <img src="../../.github/assets/readme/section-use-ar-light.svg" width="100%" alt="الاستخدام">
</picture>

اكتب `/black-iris` مرة واحدة فتُحمَّل كل الأنماط كاملة. تبقى Shape وBuild
وقائمة Cut فعّالة حتى تقول "stop black-iris". لتحميل نمط واحد فقط:
`/black-iris:deslop` في Claude Code، أو `/black-iris-deslop` في أي وكيل يقرأ
Agent Skills، أو اطلبه بكلماته المحفّزة. `/black-iris:black-iris` يحمّل الكل.

| | Claude Code | وكلاء آخرون | أو قل | ماذا يفعل |
|---|---|---|---|---|
| <img src="../../skills/black-iris/assets/logo.svg" width="28" alt="black-iris"> | `/black-iris:black-iris` | `/black-iris` | "black-iris" | كل الأنماط مع Shape وBuild وقائمة Cut |
| <img src="../../skills/black-iris/assets/modes/deslop.svg" width="28" alt="deslop"> | `/black-iris:deslop` | `/black-iris-deslop` | "deslop"، "humanize" | إزالة علامات الذكاء الاصطناعي مع الحفاظ على كل حقيقة |
| <img src="../../skills/black-iris/assets/modes/gates.svg" width="28" alt="gates"> | `/black-iris:gates` | `/black-iris-gates` | "gates"، "do not stop until done" | سجل قابل للتحقق قبل العمل الطويل |
| <img src="../../skills/black-iris/assets/modes/ideate.svg" width="28" alt="ideate"> | `/black-iris:ideate` | `/black-iris-ideate` | "ideate"، "brainstorm" | فروع متوازية معزولة ثم حكم نهائي |
| <img src="../../skills/black-iris/assets/modes/prompt.svg" width="28" alt="prompt"> | `/black-iris:prompt` | `/black-iris-prompt` | "write a prompt for X" | أمر واحد جاهز للصق في أداة محددة |
| <img src="../../skills/black-iris/assets/modes/council.svg" width="28" alt="council"> | `/black-iris:council` | `/black-iris-council` | "council this"، "pressure-test this" | خمسة مستشارين معزولين، مراجعة مجهولة، حكم واحد |
| <img src="../../skills/black-iris/assets/modes/jerash.svg" width="28" alt="jerash"> | `/black-iris:jerash` | `/black-iris-jerash` | "race this"، "try again" | مئة متسابق في جولات من النقد والتحكيم حتى تبقى إجابة واحدة |
| <img src="../../skills/black-iris/assets/modes/siq.svg" width="28" alt="siq"> | `/black-iris:siq` | `/black-iris-siq` | "handoff"، "resume where we left off" | تكتب القرارات والأدلة والتصحيحات قبل الضغط وتقرؤها بعده |
| <img src="../../skills/black-iris/assets/modes/memory.svg" width="28" alt="memory"> | `/black-iris:memory` | `/black-iris-memory` | "autodream"، "consolidate memory" | حصاد معرفة الجلسة والتحقق منها |
| <img src="../../skills/black-iris/assets/modes/context.svg" width="28" alt="context"> | `/black-iris:context` | `/black-iris-context` | "analyze this log" | استخلاص الإجابة من البيانات الكبيرة دون إغراق السياق |
| <img src="../../skills/black-iris/assets/modes/ship.svg" width="28" alt="ship"> | `/black-iris:ship` | `/black-iris-ship` | "commit message"، "PR body" | التزامات اصطلاحية مع سبب حقيقي |
| <img src="../../skills/black-iris/assets/modes/name.svg" width="28" alt="name"> | `/black-iris:name` | `/black-iris-name` | "rename"، "name this" | معرّفات صادقة في القراءة |
| <img src="../../skills/black-iris/assets/modes/review.svg" width="28" alt="review"> | `/black-iris:review` | `/black-iris-review` | "review this diff" | خمس ملاحظات مرتبة دون إعادة كتابة |

اضبط الطول عبر `/black-iris lite` أو `full` أو `deep`.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/section-store-ar-dark.svg">
  <img src="../../.github/assets/readme/section-store-ar-light.svg" width="100%" alt="أين تكتب">
</picture>

كل ما يخص المشروع يُحفظ تحت `~/.BLACK_IRIS_AGENTS/projects/<slug>/`: سجلات
البوابات، الذاكرة، الملفات المؤقتة. لا يُكتب شيء داخل مستودعك أو في
`~/.claude`. أنشئ `~/.BLACK_IRIS_AGENTS/always-on` ليُعيد خطاف Claude Code حقن
المهارة كاملة مع مراجعها وفهرس ذاكرة مشروعك عند كل بداية جلسة.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/readme/section-repo-ar-dark.svg">
  <img src="../../.github/assets/readme/section-repo-ar-light.svg" width="100%" alt="المستودع">
</picture>

- `skills/black-iris/` هو المهارة: `SKILL.md` و`references/` و`scripts/`.
- `hooks/` هو خطاف SessionStart الخاص بـ Claude Code.
- ملفات التعريف في الجذر تُغلّف المهارة نفسها لـ Codex وKimi وQwen وGemini
  وAntigravity وPi.

افحص قبل الالتزام: `python3 skills/black-iris/scripts/universal/check.py`.

الرخصة: GPL-2.0-only للمهارة وللمستودع كله. انظر [.github/LICENSE](../../.github/LICENSE).
