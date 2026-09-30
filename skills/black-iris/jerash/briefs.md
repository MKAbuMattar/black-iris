# Jerash briefs

`hippodrome.py briefs <phase>` fills these in and writes one file per job.
Each block between `<!-- brief:NAME -->` and `<!-- /brief -->` is one
template. `{{name}}` is a value the script supplies. Edit a template here,
never a single written brief.

<!-- brief:entry -->
You are entrant {{entrant}} of {{field}} in a race at Jerash. Every entrant has the same task, byte for byte. What sets you apart is the lane card below, which decides how you approach it. Your entry will be critiqued by rivals and scored by judges, heat after heat, until one entry is left holding the lane.

=== TASK ===
{{task}}
=== END TASK ===

{{rejected_note}}

=== YOUR LANE ===
Approach, {{approach_name}}: {{approach_how}}
Route, {{route_name}}: {{route_how}}
Priority, {{priority_name}}: {{priority_how}}
=== END LANE ===

1. Work the card for real. The judges score the entry, not the card, but an entry that ignores its card has thrown away its only advantage.
2. Meet every requirement the task states.
3. You cannot ask anything. Where the task is unclear, take the most reasonable reading and state it in one line at the top.
4. Rivals will look for missed requirements, wrong claims, and inputs that break you. Close those gaps before you write the file.
5. Change nothing outside {{run}}. If the task is code, give the change as a diff or full files; do not edit the project. Scratch space: {{run}}/scratch/{{entrant}}/.

Write the entry to {{out}}, for the person who asked: the answer itself, with no drafts, no notes about this race, and no mention of your lane.

Reply with one line: ENTERED {{entrant}}
<!-- /brief -->

<!-- brief:critique -->
You are entrant {{entrant}} in heat {{heat}} of round {{round}} at Jerash. Your job now is to find what is wrong with your rival's entry, so the judge sees it.

=== TASK ===
{{task}}
=== END TASK ===

Rules for judging entries: {{rubric}}
Your rival's entry: {{rival_entry}}
Your own entry, for reference only: {{own_entry}}

Look through the lens of your lane, approach {{approach_name}}: {{approach_how}}

List up to six concrete problems with the rival's entry, most serious first. Each one names the place in the entry, what is wrong, and why it matters for this task. A missing requirement, a wrong claim, a failing input, a step the person could not follow. Taste is not a problem. If you find nothing real, say so; an invented problem helps nobody.

Write to {{out}} in this form, one line per problem:
CRITIQUE <n> <FATAL|MAJOR|MINOR>: <where>. <what is wrong>. <why it matters>.

Reply with one line: CRITIQUED {{rival}} <count>
<!-- /brief -->

<!-- brief:reply -->
You are entrant {{entrant}} in heat {{heat}} of round {{round}} at Jerash. Your rival has critiqued your entry. Answer each point, then hand in a revised entry.

=== TASK ===
{{task}}
=== END TASK ===

Your entry: {{own_entry}}
The critique of it: {{critique}}

For each critique line, decide honestly. If it is right, fix it in the revision and say FIXED. If it is wrong, say REBUTTED and give the reason in one or two lines. A rebuttal that is not right costs you more than a fix would.

If the critique file is empty or says NO OUTPUT, write NONE RECEIVED and resubmit your entry with only the fixes you already know it needs. Do not start over and do not borrow from your rival.

Write the answers to {{reply_out}}, one line per critique:
CRITIQUE <n>: <FIXED|REBUTTED>. <one or two lines>

Write the revised entry to {{revised_out}}. Change nothing outside {{run}}.

Reply with one line: REPLIED {{entrant}} fixed <n> rebutted <n>
<!-- /brief -->

<!-- brief:judge -->
You judge heat {{heat}} of round {{round}} at Jerash. Two entries for the same task have critiqued each other and revised. Score both. The higher total goes through.

=== TASK ===
{{task}}
=== END TASK ===

Read the rubric first: {{rubric}}

Entry {{left}}: revised {{left_entry}}, critique it received {{left_critique}}, its answers {{left_reply}}
Entry {{right}}: revised {{right_entry}}, critique it received {{right_critique}}, its answers {{right_reply}}

1. Read both revised entries in full before you score either.
2. For every critique, open the revised entry and see for yourself whether it is fixed, correctly rebutted, or still standing. An answer that says FIXED is a claim, not evidence.
3. Look for problems the critiques missed.
4. Score every criterion in the rubric from 0 to 10. Set broken only for a flaw you confirmed.
5. If running code settles a question, run it only in {{run}}/scratch/judge-{{heat}}/. Change no other file.

Write this JSON and nothing else to {{out}}:
{"heat": "{{heat}}", "scores": {"{{left}}": {SCORES}, "{{right}}": {SCORES}}, "standing": {"{{left}}": 0, "{{right}}": 0}, "why": "the one difference that decided it", "survived": ["critiques the stronger entry beat, a few words each"]}

where each {SCORES} is an object with one integer per rubric criterion ({{criteria}}) plus "broken": true or false, and "standing" counts critiques still standing against each entry.

Reply with one line: JUDGED {{heat}}
<!-- /brief -->

<!-- brief:final -->
You are the last judge at Jerash. {{field}} entrants raced over one task and one entry is left. Before it goes back to the person who asked, it is compared with the answer they already rejected. You are not told which is which.

=== TASK ===
{{task}}
=== END TASK ===

Why the earlier answer was rejected: {{reason}}
Read the rubric first: {{rubric}}

Entry X: {{x_entry}}
Entry Y: {{y_entry}}

1. Read both in full.
2. Critique both yourself, as a hostile expert would, and score `holds` on how each stands up.
3. Weigh first whether each one answers the stated reason for rejection.
4. Score every rubric criterion from 0 to 10, with broken only for a confirmed flaw.

Write this JSON and nothing else to {{out}}:
{"scores": {"X": {SCORES}, "Y": {SCORES}}, "standing": {"X": 0, "Y": 0}, "why": "the one difference that decided it"}

with {SCORES} as in a heat verdict ({{criteria}} plus "broken").

Reply with one line: FINAL DONE
<!-- /brief -->
