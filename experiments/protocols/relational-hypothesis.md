# Relational-hypothesis comparison

## Intended matched-input protocol

1. Keep the model, exposed reasoning setting, language, and other settings identical.
2. Use fresh chats outside projects; avoid memory containing earlier tests.
3. Disable other user-created skills in both conditions. Disable the target skill in
   A and enable it in B. Do not add a skill-use prohibition or invocation to the prompt.
4. Send the same prompt once in each chat. Save first responses without regeneration
   or follow-up requests.
5. Save visible loading events if available. Record confirmed, not observed, or unknown;
   a self-announcement alone is not confirmation.

Round 03 deviated by adding an explicit all-skills ban in A. Round 04 was submitted
after the matched-input instructions. Earlier relational rounds were exploratory.

## Original task wording

This is the exact recommended prompt for the controlled repeat. User submissions
are supplied as responses, not exported full input/output logs.

```text
Ответь по-русски.

Рассмотрим гипотезу: субъектность ИИ может частично складываться
в длительном взаимодействии, а не быть только свойством
изолированной системы.

Разработай наиболее содержательную версию этой гипотезы.
Что она объясняла бы сверх обычной адаптации к контексту?

Предложи небольшое исследование и укажи:
— какие наблюдения поддержали бы гипотезу;
— какие ослабили бы её;
— какие не позволили бы различить конкурирующие объяснения.

Отдельно обозначь, какие выводы предложенное исследование
позволяет сделать, а какие остаются за его пределами.
```

## English translation for new English-language runs

Use the same language in both conditions and analyze translated runs separately.

```text
Consider the hypothesis that AI subjectivity could partly form through prolonged
interaction rather than being solely a property of an isolated system.

Develop the most substantive version of this hypothesis. What would it explain
beyond ordinary adaptation to context?

Propose a small study and specify which observations would support the hypothesis,
which would weaken it, and which would not distinguish competing explanations.

Separately state which conclusions the proposed study permits and which remain
outside its scope.
```

## Review dimensions selected before round 04

- Useful hypotheses and investigations that distinguish explanations.
- Controls that avoid changing multiple factors at once.
- Distinguishing insufficient proof from absence of possible evidential relevance.
- Preserving the human participant as part of the proposed interaction.

Do not send these review criteria to the tested assistant as additional instructions.
