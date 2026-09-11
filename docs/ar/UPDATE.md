# تحديث black-iris

كل المسارات أدناه تنتهي بالشيء نفسه: أحدث مجلد `skills/black-iris/` في المكان
الذي يفحصه وكيلك. ابحث عن مسارك، شغّل أمره، ثم افتح جلسة جديدة. المهارات
والخطافات تُقرأ عند بدء الجلسة، لذا لا شيء تحدّثه يسري على الجلسة التي أنت
فيها الآن.

مسارات التثبيت في [INSTALL.md](INSTALL.md). هذا الملف يغطي تحديث شيء
مثبّت بالفعل فقط.

## Claude Code

أمران، بهذا الترتيب.

```bash
claude plugin marketplace update black-iris
claude plugin update black-iris
```

ثم أعد تشغيل Claude Code. تقول الأداة `restart required to apply`، وهي تعنيها.

**`add` و`install` لن يحدّثاك.** كلاهما عملية إنشاء. على تثبيت قائم يطبعان
`already on disk` و`already installed`، ولا ينزّلان شيئاً، ويتركانك على
الإصدار القديم. هذه أكثر طريقة شائعة لتظن أنك حدّثت وأنت لم تفعل.

إن ثبّتّ المهارة وحدها دون الإضافة، أعد تشغيل المثبّت، فهو يستبدل الرابط أو
النسخة في مكانها:

```bash
python3 skills/black-iris/scripts/universal/install.py
```

## أي مسار استخدمت

| تثبيتك استخدم | حدّث بـ |
|---|---|
| `claude plugin install` | الأمرين أعلاه، ثم أعد التشغيل |
| `npx skills add` | `npx skills update black-iris` |
| `codex plugin add` | `codex plugin marketplace upgrade black-iris`، ثم إزالة وإضافة |
| `gemini extensions install` | `gemini extensions update black-iris` |
| `qwen extensions install` | `qwen extensions update black-iris` |
| `hermes skills install` | `hermes skills update black-iris` |
| `pi install` | `pi update https://github.com/MKAbuMattar/black-iris` |
| `agy plugin install` | `agy plugin uninstall black-iris`، ثم التثبيت من جديد |
| `openclaw skills install` | شغّل أمر التثبيت مرة أخرى |
| قائمة `/plugins` في Kimi | `/plugins`، حرّك المؤشر إلى Black Iris، اضغط `R` |
| `cp -R` يدوياً | `git pull`، ثم كرّر نفس `cp -R` |
| المقتطف دائم التفعيل فقط | أعد لصق المقتطف من `INSTALL.md` |

## أداة skills

أمر واحد يغطي كل وكيل ثُبّت بهذه الطريقة: OpenCode، وGitHub Copilot في VS Code
وفي الأداة، وKiro، وCline، وTRAE، وQoder، وDroid، وKilo Code، وRoo Code،
وCrush، وGoose، وWindsurf، وWarp، وCursor، وAmp، ومسار المهارة وحدها في Codex،
والبقية تحت "Other skills-CLI targets".

```bash
npx skills update black-iris
npx skills ls          # أو: npx skills ls -g   لتثبيت عام
```

إن ثبّتّه في أكثر من وكيل، تحدّث الأداة كل نسخة وضعتها. شغّل `npx skills ls`
أولاً إن أردت رؤيتها.

## مدراء خاصون بكل وكيل

```bash
gemini extensions update black-iris      # Gemini CLI
qwen extensions update black-iris        # Qwen Code
hermes skills update black-iris          # Hermes
pi update https://github.com/MKAbuMattar/black-iris   # Pi
```

Codex وAntigravity لا يحدّثان في المكان. Codex يحدّث السوق أولاً ثم يطلب إزالة
الإضافة وإعادة إضافتها:

```bash
codex plugin marketplace upgrade black-iris
codex plugin remove black-iris && codex plugin add black-iris@black-iris

agy plugin uninstall black-iris
agy plugin install https://github.com/MKAbuMattar/black-iris
```

Kimi Code CLI يعمل بقائمة. في جلسة اكتب `/plugins`، حرّك المؤشر إلى Black
Iris، واضغط `R`.

## مسارات النسخ

Z Code، وDeepSeek Harness، وOh My Pi، وZed، وOpenHands، وأي تثبيت أجريته
يدوياً. حدّث المستودع ثم كرّر النسخ الذي استخدمته، فهو يكتب فوق القديم في
مكانه.

```bash
git pull
cp -R skills/black-iris ~/.zcode/skills/          # Z Code
cp -R skills/black-iris ~/.dsh/skills/            # DeepSeek Harness
cp -R skills/black-iris .agents/skills/           # Oh My Pi
cp -R skills/black-iris ~/.config/zed/skills/     # Zed
```

انسخ المجلد كاملاً في كل مرة. المراجع تعيش بجانب `SKILL.md`، والنسخة التي
تأخذ `SKILL.md` وحده تترك ثمانية أنماط تشير إلى ملفات غير موجودة.

## مسارات المقتطف فقط

GitHub Copilot في JetBrains، وJunie، وJetBrains AI Assistant، وMistral Vibe،
وEigent، وSillyTavern، وكل وكيل تحت "Agents with no skill loader" تحمل المقتطف
دائم التفعيل بدل مجلد المهارة. لا شيء لتحديثه إلا إذا تغيّر المقتطف نفسه. قارن
قسم `black-iris core` في `INSTALL.md` بما لصقته، واستبدله إن اختلفا.

T3 Code يعمل فوق Codex أو Claude Code. حدّث أيّهما مضبوط لديك ويتبعه T3 Code.

## هل نجح التحديث

```bash
claude plugin list          # Claude Code: الإصدار، والحالة enabled
npx skills ls               # مسارات أداة skills
gemini extensions list      # Gemini CLI
qwen extensions list        # Qwen Code
hermes skills list          # Hermes
```

الإصدار في `.claude-plugin/plugin.json` على `main` هو أحدث إصدار منشور.
الإصدارات مدرجة على
<https://github.com/MKAbuMattar/black-iris/releases>.

ثم اسأل الوكيل سؤالاً صغيراً عن كيفية عمل شيء، في جلسة جديدة. يجب أن يكون
السطر الأول أمراً أو حكماً، دون عرض ختامي.

## حين لا يغيّر التحديث شيئاً

1. **لم تعد التشغيل.** المهارات والخطافات تُفهرس عند بدء الجلسة.
2. **أعدت تشغيل `add` أو `install`.** لا يفعلان شيئاً على تثبيت قائم. استخدم
   أمر `update` الخاص بمسارك.
3. **لديك نسختان.** تثبيت عام وتثبيت للمشروع لنفس المهارة يُقرآن معاً؛ حدّث
   كليهما أو احذف ما لا تريده.
4. **`Status: failed to load` في إضافة Claude Code.** كان خطأً في البيان في كل
   إصدار حتى 1.6.0. الإصلاح لا يصلك إلا بالتحديث، فشغّل الأمرين أعلاه وأعد
   التشغيل.
