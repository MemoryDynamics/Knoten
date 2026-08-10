# P3.2 500k accumulation control

Date: 2026-08-06T20:53:28+00:00.

## Design

Two future-noise paths continue the same mature formation checkpoint for `500,000` updates or `5000` memory times. Every `10`th update is stored; regression tests require this to be exact subsampling of the same hidden path and preserve fitted rates.

The mechanism, gain, kernel, grid, noise scale, and four P3.2 arms are unchanged. This is an accumulation falsification, not a reopening of the earlier mode or source-local gates.

## Result

Classification: **no control-separated P3.2 accumulation through 500k**.

- original long-horizon mode candidate: False;
- registered accumulation candidate: False;
- reciprocal shape-valid seeds: 2/2;
- reciprocal late-minus-early deltas: [19.144977869406894, 10.511831430564056];
- one-way late-minus-early deltas: [19.030578026737437, 10.307497806168222].

The large off-subtracted path differences are not reciprocal-specific: the one-way control accumulates nearly the same changes in both future-noise paths. Meanwhile, the actual late pair-distance medians remain bounded near one knot radius in both retarded arms. The supported reading is sensitive path divergence after a persistent perturbation, not a control-separated reciprocal accumulation law.

![P3.2 500k accumulation control](../../figures/draft/response/p32_accumulation_control_N500k_2026-08-06.png)

## Fixed-window diagnostics

| seed | arm | window | median distance/R | IQR/R | slope R/1000 memory times | median absolute delta from off/R |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1 | retarded_one_way | 100-500 | 1.075 | 0.775-1.407 | +0.1295 | 2.159 |
| 1 | retarded_one_way | 500-1000 | 1.109 | 0.7065-1.415 | +0.6206 | 8.172 |
| 1 | retarded_one_way | 1000-2500 | 1.065 | 0.7684-1.323 | -0.03372 | 12.01 |
| 1 | retarded_one_way | 2500-5000 | 1.02 | 0.7572-1.356 | -0.05428 | 21.19 |
| 1 | retarded_reciprocal | 100-500 | 1.02 | 0.7177-1.315 | +0.02147 | 2.068 |
| 1 | retarded_reciprocal | 500-1000 | 0.8483 | 0.5999-1.129 | +0.1252 | 8.403 |
| 1 | retarded_reciprocal | 1000-2500 | 0.9352 | 0.6652-1.245 | -0.05148 | 12.05 |
| 1 | retarded_reciprocal | 2500-5000 | 0.9369 | 0.6781-1.231 | -0.05161 | 21.21 |
| 2 | retarded_one_way | 100-500 | 1.098 | 0.8437-1.449 | -0.4953 | 5.557 |
| 2 | retarded_one_way | 500-1000 | 0.9145 | 0.7152-1.195 | -0.9485 | 6.393 |
| 2 | retarded_one_way | 1000-2500 | 1.019 | 0.6959-1.361 | -0.05496 | 9.394 |
| 2 | retarded_one_way | 2500-5000 | 1.07 | 0.8226-1.391 | -0.004577 | 15.86 |
| 2 | retarded_reciprocal | 100-500 | 1.125 | 0.8533-1.371 | -0.9685 | 5.466 |
| 2 | retarded_reciprocal | 500-1000 | 1.003 | 0.6967-1.293 | -0.7807 | 6.228 |
| 2 | retarded_reciprocal | 1000-2500 | 1.051 | 0.7814-1.346 | +0.009561 | 9.388 |
| 2 | retarded_reciprocal | 2500-5000 | 1.006 | 0.7451-1.332 | -0.009265 | 15.98 |

## Interpretation boundary

Both paths branch from one formation state. They can reveal a delayed numerical accumulation on this branch but cannot estimate basin prevalence. The source remains a target-specific cross-gradient, and the channel law remains inserted. No field, causal-speed, spin, charge, particle, dimension, or QFT claim follows.

## Reproducibility

- preregistration: `reports/project/meta/preregistration/p32_accumulation_control_preregistration_2026-08-06.md`;
- git revision: `72ae14528e7a807e9484093c1503e2ec9f3f72a9`;
- git status at start: `clean`;
- base runtime: `404.212 s`;
- command: `python experiments/current/memory/synchronization/reciprocity/p32_accumulation_control.py`;
- machine-readable summary: `reports/response/reciprocal/p32_accumulation_control_N500k_2026-08-06.json`.
