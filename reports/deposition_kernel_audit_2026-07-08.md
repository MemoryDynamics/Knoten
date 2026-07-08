# Deposition Kernel Audit

Date: 2026-07-08.

## Result

The canonical simulation backend already uses delta deposition.

In code, the retained memory is a weighted list of past points
`x[n-k]`. The force is evaluated as a direct weighted sum of Gaussian kernel
gradients over those point deposits:

```text
grad Phi(x_n) = sum_k w_k grad K(x_n - x[n-k])
```

This is the discrete representation of

```text
rho_n = sum_k w_k delta(. - x[n-k])
```

and therefore corresponds to `G = delta` in the paper notation. The parameters
`sigma_rep` and `sigma_att` are interaction/effective-kernel lengths in `K`, not
a separate deposition smoothing width.

## Consequence

The existing baseline, single-scale, eta-zero, M0-zero, and alpha-one long-run
families should be read as delta-deposition runs. A new `delta_deposition`
condition would only duplicate `baseline` for the same seed and parameters.

This matters for the two-scale question: the lack of separation between
`baseline` and `single_scale` in the current 100M score comparison cannot be
explained by a broad Gaussian deposition kernel washing out the short scale.
The current implementation already preserves point deposits.

## Next useful control

The meaningful additional control is the opposite direction: implement an
explicit finite-width deposition kernel. For Gaussian `K` and Gaussian `G`, this
can first be approximated analytically by replacing each interaction length with
an effective convolved length

```text
sigma_eff = sqrt(sigma_K^2 + sigma_G^2)
```

and then checking whether increasing `sigma_G` suppresses the two-scale
signature. That would directly test the smoothing/washout hypothesis.

## Implementation status

Original audit result: `SimulationConfig` recorded `deposition_kernel="delta"`
to make the point-memory convention explicit.

Follow-up implementation on 2026-07-08: finite Gaussian deposition is now
implemented through effective convolution parameters. Supported modes are
`delta`, `gaussian`, and `matched_gaussian`; long-run payloads include the
resulting `effective_kernel`. The first matched-deposition pilot is reported in
`reports/matched_deposition_kernel_pilot_2026-07-08.md`.
