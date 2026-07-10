# Initial Vector-Memory Pilot

Date: 2026-07-10T04:13:31Z.

## Scope

This pilot tests the first oriented-memory implementation. It is a
mode diagnostic, not a photon, neutrino, boson, or Standard-Model claim.

Burn-in is kept as an analysis cut, not a model assumption. The default
pilot uses `burn_in=0` to preserve formation histories.

## Parameters

- `amplitude_att`: `[0.35]`
- `eta_s`: `0.0`
- `eta_vector`: `[0.0, 0.01, 0.03]`
- `force_mode`: `transverse_2d`
- `alpha=lambda_s`: `0.01`
- `lambda_vector`: `0.01` (`None` means `alpha`)
- `memory_mass=M0_s`: `1.0`
- `vector_mass=M0_v`: `1.0`
- `steps`: `5000`, `seeds`: `[1, 2, 3]`

## AR Summary

| A_att | eta_v | radius med | lag | class | leading abs | leading imag | residual | top eigenvalues |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| `0.35` | `0` | `0.9952` | `1` | `complex` | `0.9912` | `0.01361` | `0.987` | `0.9911+0.0136i ; 0.9911-0.0136i ; 0.6320+0.0231i` |
| `0.35` | `0` | `0.9952` | `2` | `complex` | `0.9866` | `0.02626` | `1.143` | `0.9862+0.0263i ; 0.9862-0.0263i ; 0.3621+0.0191i` |
| `0.35` | `0` | `0.9952` | `5` | `complex` | `0.9643` | `0.06501` | `1.196` | `0.9621+0.0650i ; 0.9621-0.0650i ; 0.1614+0.0800i` |
| `0.35` | `0.01` | `0.9981` | `1` | `complex` | `0.9936` | `-0.01321` | `0.9846` | `0.9935-0.0132i ; 0.9935+0.0132i ; 0.6134+0.0872i` |
| `0.35` | `0.01` | `0.9981` | `2` | `complex` | `0.9908` | `0.02573` | `1.14` | `0.9905+0.0257i ; 0.9905-0.0257i ; 0.3636+0.1052i` |
| `0.35` | `0.01` | `0.9981` | `5` | `complex` | `0.974` | `0.06169` | `1.196` | `0.9720+0.0617i ; 0.9720-0.0617i ; 0.1538+0.1101i` |
| `0.35` | `0.03` | `0.9191` | `1` | `complex` | `0.9979` | `-0.01068` | `0.9889` | `0.9978-0.0107i ; 0.9978+0.0107i ; 0.6161` |
| `0.35` | `0.03` | `0.9191` | `2` | `complex` | `0.9979` | `0.02032` | `1.144` | `0.9977+0.0203i ; 0.9977-0.0203i ; 0.2900+0.2172i` |
| `0.35` | `0.03` | `0.9191` | `5` | `complex` | `0.9897` | `0.04631` | `1.206` | `0.9886+0.0463i ; 0.9886-0.0463i ; 0.0766+0.1247i` |

## Immediate Reading

- Complex AR classifications in this pilot are not by themselves evidence
  for vector-induced oscillators, because `eta_vector=0` is included as
  a scalar fallback control and can already show complex projected modes.
- A vector effect requires a change relative to the `eta_vector=0` rows
  that is stable across lag, seed, and feature choices.
- The compact `A_att=20.0` reference should be read separately from the
  transition band `7.75..9.0`; it tests over-confinement/relaxation, not
  the boundary itself.

## Reading Rules

- `eta_vector=0` is the scalar fallback control.
- A complex classification matters only if it is slow and stable across lags.
- `A_att=0.35` is the weak-attraction historical reference; `7.75..9.0`
  covers the corrected transition; `20.0` is the first compactness
  reference inside the `9..35` window.
