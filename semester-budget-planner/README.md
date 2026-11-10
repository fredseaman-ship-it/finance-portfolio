# Semester Budget Planner

A budgeting framework that turns a student's income, costs and savings into one number: **how many hours a week do I need to work?**

<!-- Add 2 or 3 screenshots of your planner into the screenshots/ folder, then uncomment:
![Planner overview](screenshots/planner-overview.png)
![Month-by-month balance](screenshots/month-by-month.png)
-->

## The problem

Most student budgets are written once in September and abandoned by November. They also use annual averages, which hide the real risk: student finance lands in three lumps while rent leaves every month, so a plan that balances over the year can still hit zero part-way through it.

## How it works

### Two clocks, not one
| Window | Dates | Payments |
|---|---|---|
| Rent | 1 Sep to 29 Apr | 8 |
| Bills | 1 Sep to 1 Jun | 9 |
| Everything else | Sep to Jun | 10 months |

Getting these windows right is the foundation. Every downstream number depends on them.

### Five layers
1. **The frame:** hourly rate after tax, realistic working weeks (about 39 from September to June), opening savings, and an honest cap on term-time hours.
2. **Money that arrives anyway:** student finance instalments, family support and bursaries, each tagged with *when* it lands, not just how much.
3. **Money going out, in three tiers:**
   - **Tier A, Locked:** rent, utilities, phone, insurance, course costs.
   - **Tier B, Living:** food, household, transport, laundry.
   - **Tier C, Life:** going out, subscriptions, clothes, gifts.

   The tiers matter more than the categories because they set the order to cut in when the answer comes back too high.
4. **The gap:** total outgoings minus non-work income minus opening savings. Gap ÷ hourly rate = total hours. Total hours ÷ working weeks = **hours per week**.
5. **Month by month:** a running balance from September to June. Wherever it dips negative, earnings need to be *front-loaded* rather than earned in the moment.

## What it found

Two pressure points sit on the calendar:
- **December to January:** the longest gap between finance instalments, on top of Christmas and travel home.
- **May:** rent has stopped but bills haven't, and exams limit working hours. Earn ahead of it.

## Routine built in

On the last day of each month, 20 minutes: update actual spend and earnings and let the hours-per-week figure reset. A budget written once is fiction by November.

## How it connects to the rest of this portfolio

This planner is a **deterministic plan**: one set of inputs, one answer. The [Cashflow Stress-Tester](../cashflow-stress-tester/) takes the same structure and adds **uncertainty**, asking how likely the plan is to fail.

## Limitations

- Built for one student's circumstances. Inputs such as rent, hourly rate and instalment sizes need replacing for anyone else.
- Assumes spending and earnings go roughly to plan. See the stress-tester for what happens when they don't.

## Live version

[Open the planner](https://claude.ai/code/artifact/7059eed1-e845-4117-89d9-313d23dd7902)
