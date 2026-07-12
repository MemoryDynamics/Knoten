# Initial Vector-Memory Pilot

Date: 2026-07-10T04:14:27Z.

## Scope

This pilot tests the first oriented-memory implementation. It is a
mode diagnostic, not a photon, neutrino, boson, or Standard-Model claim.

Burn-in is kept as an analysis cut, not a model assumption. The default
pilot uses `burn_in=0` to preserve formation histories.

## Parameters

- `amplitude_att`: `[0.35, 8.0, 20.0]`
- `eta_s`: `0.15`
- `eta_vector`: `[0.0, 0.01, 0.03]`
- `force_mode`: `alignment`
- `alpha=lambda_s`: `0.01`
- `lambda_vector`: `0.01` (`None` means `alpha`)
- `memory_mass=M0_s`: `1.0`
- `vector_mass=M0_v`: `1.0`
- `steps`: `5000`, `seeds`: `[1, 2, 3]`

## AR Summary

| A_att | eta_v | radius med | lag | class | leading abs | leading imag | residual | top eigenvalues |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| `0.35` | `0` | `26.97` | `1` | `complex` | `0.9924` | `-0.05848` | `0.4816` | `0.9906-0.0585i ; 0.9906+0.0585i ; 0.9805-0.0169i` |
| `0.35` | `0` | `26.97` | `2` | `complex` | `0.9865` | `0` | `0.5963` | `0.9865 ; 0.9672-0.1076i ; 0.9672+0.1076i` |
| `0.35` | `0` | `26.97` | `5` | `complex` | `1.001` | `0` | `0.8296` | `1.0010 ; 0.8671-0.2337i ; 0.8671+0.2337i` |
| `0.35` | `0.01` | `28.19` | `1` | `complex` | `0.993` | `-0.06098` | `0.4743` | `0.9911-0.0610i ; 0.9911+0.0610i ; 0.9800-0.0123i` |
| `0.35` | `0.01` | `28.19` | `2` | `complex` | `0.9893` | `0` | `0.5895` | `0.9893 ; 0.9667-0.1138i ; 0.9667+0.1138i` |
| `0.35` | `0.01` | `28.19` | `5` | `complex` | `1.003` | `0` | `0.8152` | `1.0029 ; 0.8611-0.2445i ; 0.8611+0.2445i` |
| `0.35` | `0.03` | `30.62` | `1` | `complex` | `0.9931` | `-0.052` | `0.4696` | `0.9918-0.0520i ; 0.9918+0.0520i ; 0.9822-0.0144i` |
| `0.35` | `0.03` | `30.62` | `2` | `complex` | `0.9875` | `0` | `0.5898` | `0.9875 ; 0.9639-0.0932i ; 0.9639+0.0932i` |
| `0.35` | `0.03` | `30.62` | `5` | `complex` | `0.9969` | `0` | `0.8262` | `0.9969 ; 0.8371+0.1525i ; 0.8371-0.1525i` |
| `8` | `0` | `1.003` | `1` | `complex` | `0.9859` | `0.01321` | `1.068` | `0.9858+0.0132i ; 0.9858-0.0132i ; 0.5353+0.0180i` |
| `8` | `0` | `1.003` | `2` | `complex` | `0.981` | `0.02563` | `1.189` | `0.9807+0.0256i ; 0.9807-0.0256i ; 0.2497-0.0162i` |
| `8` | `0` | `1.003` | `5` | `complex` | `0.9636` | `0.06782` | `1.209` | `0.9612+0.0678i ; 0.9612-0.0678i ; 0.1480` |
| `8` | `0.01` | `1.126` | `1` | `complex` | `0.9867` | `0.01186` | `1.058` | `0.9866+0.0119i ; 0.9866-0.0119i ; 0.5560+0.0344i` |
| `8` | `0.01` | `1.126` | `2` | `complex` | `0.9829` | `0.02382` | `1.187` | `0.9826+0.0238i ; 0.9826-0.0238i ; 0.2561-0.0350i` |
| `8` | `0.01` | `1.126` | `5` | `complex` | `0.9703` | `0.06443` | `1.209` | `0.9682+0.0644i ; 0.9682-0.0644i ; 0.1327` |
| `8` | `0.03` | `1.306` | `1` | `complex` | `0.9858` | `0.01094` | `1.038` | `0.9858+0.0109i ; 0.9858-0.0109i ; 0.5815+0.0187i` |
| `8` | `0.03` | `1.306` | `2` | `complex` | `0.9825` | `0.02364` | `1.184` | `0.9822+0.0236i ; 0.9822-0.0236i ; 0.2736-0.0416i` |
| `8` | `0.03` | `1.306` | `5` | `complex` | `0.9737` | `0.06639` | `1.21` | `0.9715+0.0664i ; 0.9715-0.0664i ; 0.0944` |
| `20` | `0` | `0.09362` | `1` | `real` | `0.953` | `0` | `1.099` | `0.9530 ; 0.6157 ; 0.5063` |
| `20` | `0` | `0.09362` | `2` | `complex` | `0.9306` | `0` | `1.149` | `0.9306 ; 0.3796 ; 0.2935-0.0470i` |
| `20` | `0` | `0.09362` | `5` | `real` | `0.9159` | `0` | `1.174` | `0.9159 ; 0.1642+0.0401i ; 0.1642-0.0401i` |
| `20` | `0.01` | `0.09421` | `1` | `real` | `0.9553` | `0` | `1.091` | `0.9553 ; 0.6177 ; 0.6000` |
| `20` | `0.01` | `0.09421` | `2` | `real` | `0.9356` | `0` | `1.143` | `0.9356 ; 0.4265 ; 0.3779` |
| `20` | `0.01` | `0.09421` | `5` | `real` | `0.9226` | `0` | `1.17` | `0.9226 ; 0.2606 ; 0.2069` |
| `20` | `0.03` | `0.09586` | `1` | `real` | `0.9671` | `0` | `1.066` | `0.9671 ; 0.7972 ; 0.6169` |
| `20` | `0.03` | `0.09586` | `2` | `real` | `0.9557` | `0` | `1.121` | `0.9557 ; 0.6909 ; 0.3813` |
| `20` | `0.03` | `0.09586` | `5` | `real` | `0.9516` | `0` | `1.147` | `0.9516 ; 0.5830 ; 0.1812-0.0129i` |

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
