# Kernel Shape Probe

Date: 2026-07-01T21:07:36Z.

## Scope

This is a targeted visual probe for smoother or rounder 3D trajectories.
It varies only kernel widths/amplitudes across a few motivated cases.
It is not a broad parameter sweep and not Paper-I evidence by itself.

Important sign convention: in the current Euler update, the kernel
contributes a deterministic drift term. It does not impose a hard
minimum step length; without inertia or correlated noise the path can
remain jagged even when it is spatially confined.

## Figure

![Kernel shape probe](../figures/draft/kernel_shape_probe_2026-07-01.svg)

## Results

| case | sigma_rep | sigma_att | A_rep | A_att | mean radius | median step | turn mean | path/chord | PCA energy first 3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `1` | `3` | `1` | `0.35` | `0.233` | `0.1099` | `-0.342` | `1202.3` | `0.60, 0.24, 0.16` |
| `single_scale` | `1` | `3` | `1` | `0` | `0.225` | `0.1090` | `-0.348` | `1238.7` | `0.59, 0.24, 0.16` |
| `strong_local` | `1` | `3` | `4` | `0.35` | `0.075` | `0.0707` | `-0.430` | `2746.5` | `0.49, 0.28, 0.23` |
| `wide_strong` | `2` | `6` | `16` | `1.4` | `0.075` | `0.0707` | `-0.430` | `2752.4` | `0.49, 0.28, 0.23` |

## Reading

- Increasing local kernel strength changes confinement scale, but it
  does not automatically create directionally persistent, round paths.
- Co-scaling amplitudes with kernel width can leave the local
  stiffness scale A/sigma^2 almost unchanged in compact regimes.
- If the scientific target is visibly smooth curves rather than compact
  residence, the model likely needs an additional mechanism such as
  persistent noise, an inertial/velocity variable, or a smoother
  coarse-grained trajectory observable.
