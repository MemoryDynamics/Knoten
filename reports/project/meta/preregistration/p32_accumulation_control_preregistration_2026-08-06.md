# P3.2 500k accumulation control: preregistration

Date: 2026-08-06.

## Question

Can the fixed, target-gradient-driven P3.2 Telegraph mechanism accumulate a
late reciprocal response or control-separated observable mode that was absent
at 50,000 and 150,000 updates?

This user-requested run is an additional falsification control. It does not
reopen or replace the negative P3.2 and P3.2c gates.

## Fixed simulation

- mature scalar `d=3`, `N=100,000,000`, formation-seed-1 checkpoint;
- future-noise seeds `{1,2}` from the registered seed offset;
- `500,000` updates = `5,000` memory times at `lambda=0.01`;
- store every 10th update; the hidden dynamics still advances every update;
- first 100 memory times excluded from mode fitting;
- initial distance `2.5 R`, cross gain `c=0.02`;
- correlation length `5 R`, relaxation time `10` memory times;
- grid spacing `0.25 R`, unchanged finite grid and exact DC normalization;
- channel-off, direct reciprocal, retarded one-way, and retarded reciprocal
  arms; no gain, lambda, noise, kernel, or geometry search.

## Registered analyses

The original four-segment observable `(x_-,m_-)` mode gate is retained with
frequency and damping scaled by the `0.1`-memory-time output cadence. With two
seeds, a candidate requires both reciprocal seeds and zero candidate seeds in
every control.

Accumulation is evaluated in fixed memory-time windows:

```text
[100,500], [500,1000], [1000,2500], [2500,5000].
```

For each seed and arm report:

- median and interquartile pair distance in `R`;
- linear pair-distance slope per 1,000 memory times;
- median absolute pair-distance difference from channel-off;
- early-to-late change of that control-subtracted difference;
- original mode, response, mediator, radius, and shape gates.

## Decision rule

- **control-separated mode:** both reciprocal seeds pass the original mode
  identity/shape/response gate and every control has zero candidate seeds;
- **late accumulation candidate:** both reciprocal seeds show a late-minus-
  early increase of at least `0.1 R` in absolute control-subtracted pair
  distance, while the one-way arm remains below `0.05 R` increase;
- **null:** neither condition holds and the shape gate remains valid;
- **inconclusive:** either reciprocal seed violates the shape envelope or the
  two seeds disagree in the sign of the late accumulation change.

The `0.1 R` threshold is deliberately effect-size based. Two paths from one
formation state do not justify uncertainty estimates or a general metastable
population claim.

## Outputs

- `reports/response/reciprocal/p32_accumulation_control_N500k_2026-08-06.md`;
- `reports/response/reciprocal/p32_accumulation_control_N500k_2026-08-06.json`;
- `figures/draft/response/p32_accumulation_control_N500k_2026-08-06.png`.

