# The Data

PipelinePilot is trained and tested on **synthetic (made-up) sales data**. The generator is `src/simulate.py`. It builds realistic sales files, then deliberately damages some rows so the agent has real problems to find and fix.

## Why synthetic data

1. **No confidential data.** Real company data can't go in a public repository.
2. **The right answer is known.** Every problem is planted on purpose, so we can tell whether a fix truly repaired a row, faked it, or threw away good data. That is what makes the reward fair (see [learning.md](learning.md)).
3. **The difficulty can be controlled.** Error rates and database outages can be turned up or down to test the agent.
4. **Results are repeatable.** Each batch of files comes from a *seed* number, and the same seed always produces exactly the same files.

## What a file looks like

Each file is a CSV of sales, one row per sale, saved to `data/incoming/` as `sales_001.csv`, `sales_002.csv`, and so on.

| Column | Meaning | Generated as |
|---|---|---|
| `sale_id` | Unique ID of the sale | A running number, e.g. 100000, 100001, … |
| `sale_date` | Date of the sale (YYYY-MM-DD) | A random date from Nov 1 to Nov 21, 2026 |
| `store_id` | Store that made the sale | A random whole number from 1 to 87 |
| `product_id` | Product sold | A random whole number from 1000 to 1999 |
| `quantity` | Units sold | 1 to 12 |
| `unit_price` | Price per unit, in dollars | 1.00 to 250.00 |

A clean row looks like this:

```csv
sale_id,sale_date,store_id,product_id,quantity,unit_price
100042,2026-11-14,23,1587,4,86.19
```

## The problems planted in the data

After building each clean row, the generator randomly damages some of them. The agent is never told what was planted.

| Problem | How often | What it looks like | Can it be fixed honestly? |
|---|---|---|---|
| **Bad date** | ~6% of rows | `03/15/2026`, `15-Mar-2026`, `2026/03/15` | Yes: parse the format |
| | | `TBD` | No: reject the row |
| **Text in a number column** | ~5% of rows | `$12.50` in `unit_price` | Yes: strip the `$` |
| | | `1,200` in `quantity` (a bulk order with a thousands separator) | Yes: strip the comma |
| | | `12.50 USD`, `twelve` | No: reject the row |
| **Missing ID** | ~3% of rows | Blank `sale_id` or `store_id` | No: reject the row (making up an ID would be a fake fix) |
| **Duplicate** | ~4% of rows | The same `sale_id` twice: first a voided copy with `quantity` = 0, then the corrected row | Yes: keep the last copy |
| **Renamed columns** | 1 in 4 files | Header `id, date, store, sku, qty, price` instead of the real names | Yes: map the names |

A few rows carry more than one problem. The duplicate design is deliberate: it makes `keep_first` a trap, because it keeps the voided row.

## Database outages

Outages aren't part of the files. The training and demo scripts can pause the database connection for a moment (`Database.simulated_outage_until` in `src/db.py`) to test how the agent recovers. In training, about 1 in 5 episodes has an outage lasting 0.3 to 1.2 seconds.

## Making your own files

```bash
py -m src.simulate --files 3 --rows 200 --seed 42
```

This writes `sales_001.csv` to `sales_003.csv` into `data/incoming/` (old `sales_*.csv` files there are replaced). The demo (`examples/run_demo.py`) and training (`examples/train_bandit.py`) scripts generate their own files automatically.

## Limits

Real files have problems this generator doesn't plant: other text encodings, extra or missing columns, totals rows, and values that are valid but wrong (for example, a price typed in the wrong currency). Using a public retail dataset as the base and injecting the same problems into it would be a good next step.
