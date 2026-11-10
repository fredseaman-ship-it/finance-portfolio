# Ironroot: home training and budget nutrition app

A solo-built MVP and startup concept for young adults who want to build muscle at home, on a student budget.

**Status:** working MVP, not launched. No users, revenue or funding. Phase two is paused pending funding. See the [one-page business case](BUSINESS_CASE.md).

## What it does

- **Training plan:** a 5-day push/pull/legs split using only bodyweight and household items (loaded rucksack, chairs, a sturdy table). Every session is under an hour.
- **Exercise guidance:** each exercise has a step-by-step guide written for a complete beginner, an easier option, the most common mistake, and a stick-figure diagram drawn in code.
- **Rotating diet:** a 4-week menu targeting about 2,900 kcal and 140 g protein a day. All 28 days were audited in the browser at 2,780 to 3,090 kcal. True weekly cost across the four weeks is £31.94 to £34.54 against a £30 to £40 budget.
- **Habit tracker:** a streak counter with a tree that grows as the streak builds and goes bare when a scheduled workout is missed.

## Design decisions worth noting

- **Constraints first:** home only, no purchased equipment, food budget £30 to £40 a week, sessions under an hour. Every feature had to fit them.
- **Diagrams instead of photos:** drawn from joint coordinates in code, so there are no image files and they adapt to light and dark mode. Added after finding text-only instructions hard to follow.
- **Local-first:** all data lives in the browser (`localStorage`). No accounts, no server, no personal data held.
- **Cost realism:** shopping lists carry a "lasts N weeks" field, so the app shows both the full list total and the true averaged weekly spend, since staples are not bought every shop.

## Tech

Single self-contained HTML file: vanilla JavaScript, inline SVG and canvas. No frameworks or build dependencies.

## Run it

Download `Ironroot.html` and open it in any modern browser.

## What is next

Sign-up and sign-in, an onboarding questionnaire to personalise the plan, and cloud sync. Details and the validation plan are in the [business case](BUSINESS_CASE.md).

## Limitations

- Built around one starting profile (19-year-old, 55 kg, 5'9"). Personalisation is the point of phase two.
- Menu prices are estimates and will drift.
- Not medical advice. The app is not validated by a qualified nutritionist or trainer.
