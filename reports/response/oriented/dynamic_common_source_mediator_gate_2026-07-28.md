# Dynamic Common-Source Mediator Gate

Generated: `2026-07-28T18:56:53.538868+00:00`.

## Question

When the same autonomous source waveform drives the two already fixed local mediator laws under their pulse-calibrated couplings, do they produce measurable, odd, shape-bounded and dynamically distinct target responses across the inherited source-target holdouts?

## Preregistered design

- common settling interval `20.0000` and analysis interval `50.0000` memory times;
- six checksum-validated cyclic source-target pairs and the inherited distance ladder `2.5, 5, 10 R_pair`;
- mediator grids, laws, length scale and one pulse-calibrated coupling per law are inherited without retuning;
- persistent carrier and unit one-step source drive independent ambient components of the same one-dimensional relational mediator;
- active, global-sign-flip and exact channel-off target branches share one future-noise path;
- persistent RMS response must lie in `[1.000e-04, 0.1000] R_target`, odd residual at most `0.1000`, and target radius/shape changes at most `0.1`;
- far/near RMS response at most `0.5000` and relative cross-model response-trace separation at least `0.2500`;
- model and separation pass require at least `5/6` pairs.

The one-step arm is reported at the same coupling without amplitude matching. It is diagnostic and cannot rescue or invalidate the primary persistent arm by scale alone.

## Decision

Status: **dynamic_common_source_gate_fail**.

Both fixed mediator branches satisfy the response, oddness, source/target shape, and attenuation gates for all pairs. The preregistered cross-model separation criterion holds for only 4/6 pairs rather than the required 5/6. The present autonomous-source response therefore does not robustly distinguish the two inserted transport laws.

![Dynamic common-source gate](../../figures/draft/response/dynamic_common_source_mediator_gate_2026-07-28.png)

## Model summary

| model | passing pairs | response RMS range | max odd residual | max radius change | max shape change |
| --- | ---: | ---: | ---: | ---: | ---: |
| relaxation-diffusion | 6/6 | 0.0043..0.0552 | 1.008e-11 | 6.206e-04 | 0.0015 |
| telegraph | 6/6 | 0.0032..0.0454 | 1.375e-11 | 5.210e-04 | 0.0011 |

Both model rows pass the preregistered response, sign-flip, source/target shape and attenuation gates. Any overall failure therefore occurs at the separate cross-model discrimination gate.

## Separation by distance

| distance/R_pair | passing pairs | minimum | median | maximum |
| ---: | ---: | ---: | ---: | ---: |
| 2.5000 | 4/6 | 0.1874 | 0.2881 | 0.4640 |
| 5.0000 | 6/6 | 0.2700 | 0.4122 | 0.6558 |
| 10.0000 | 6/6 | 0.4413 | 0.6641 | 0.9455 |

## Pair results

| target<-source | source shape | diffusion | telegraph | min persistent separation | min one-step separation | overall |
| --- | --- | --- | --- | ---: | ---: | --- |
| 1<-2 | pass | pass | pass | 0.1874 | 0.1993 | fail |
| 2<-3 | pass | pass | pass | 0.2739 | 0.2838 | pass |
| 3<-4 | pass | pass | pass | 0.3023 | 0.3195 | pass |
| 4<-5 | pass | pass | pass | 0.2387 | 0.2530 | fail |
| 5<-6 | pass | pass | pass | 0.4640 | 0.4569 | pass |
| 6<-1 | pass | pass | pass | 0.3596 | 0.3178 | pass |

## Source-drive scale

| target<-source | persistent RMS | unit one-step RMS |
| --- | ---: | ---: |
| 1<-2 | 0.0279 | 1.0000 |
| 2<-3 | 0.0297 | 1.0000 |
| 3<-4 | 0.0296 | 1.0000 |
| 4<-5 | 0.0286 | 1.0000 |
| 5<-6 | 0.0311 | 1.0000 |
| 6<-1 | 0.0283 | 1.0000 |

## Distance-resolved persistent response

| target<-source | model | distance/R_pair | persistent RMS/R | one-step RMS/R | odd residual | radius change | shape change |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1<-2 | relaxation-diffusion | 2.5000 | 0.0449 | 0.0406 | 1.966e-12 | 6.206e-04 | 0.0015 |
| 1<-2 | relaxation-diffusion | 5.0000 | 0.0270 | 0.0244 | 1.396e-12 | 2.861e-04 | 7.229e-04 |
| 1<-2 | relaxation-diffusion | 10.0000 | 0.0095 | 0.0087 | 2.242e-12 | 8.625e-05 | 2.037e-04 |
| 1<-2 | telegraph | 2.5000 | 0.0433 | 0.0394 | 4.421e-12 | 4.431e-04 | 0.0010 |
| 1<-2 | telegraph | 5.0000 | 0.0250 | 0.0229 | 1.716e-12 | 2.152e-04 | 4.755e-04 |
| 1<-2 | telegraph | 10.0000 | 0.0079 | 0.0073 | 2.640e-12 | 9.645e-05 | 2.182e-04 |
| 2<-3 | relaxation-diffusion | 2.5000 | 0.0552 | 0.0537 | 4.443e-12 | 5.274e-04 | 0.0011 |
| 2<-3 | relaxation-diffusion | 5.0000 | 0.0313 | 0.0305 | 2.293e-12 | 2.794e-04 | 6.372e-04 |
| 2<-3 | relaxation-diffusion | 10.0000 | 0.0099 | 0.0097 | 2.282e-12 | 1.123e-04 | 2.400e-04 |
| 2<-3 | telegraph | 2.5000 | 0.0454 | 0.0444 | 2.585e-12 | 5.210e-04 | 0.0011 |
| 2<-3 | telegraph | 5.0000 | 0.0235 | 0.0231 | 1.531e-12 | 2.794e-04 | 6.317e-04 |
| 2<-3 | telegraph | 10.0000 | 0.0057 | 0.0058 | 3.942e-12 | 1.465e-04 | 3.029e-04 |
| 3<-4 | relaxation-diffusion | 2.5000 | 0.0417 | 0.0398 | 4.031e-12 | 4.544e-04 | 0.0010 |
| 3<-4 | relaxation-diffusion | 5.0000 | 0.0237 | 0.0226 | 2.395e-12 | 2.616e-04 | 5.636e-04 |
| 3<-4 | relaxation-diffusion | 10.0000 | 0.0075 | 0.0072 | 6.548e-12 | 7.444e-05 | 1.819e-04 |
| 3<-4 | telegraph | 2.5000 | 0.0342 | 0.0327 | 3.195e-12 | 3.797e-04 | 9.482e-04 |
| 3<-4 | telegraph | 5.0000 | 0.0179 | 0.0170 | 2.939e-12 | 2.031e-04 | 4.250e-04 |
| 3<-4 | telegraph | 10.0000 | 0.0047 | 0.0044 | 1.107e-11 | 6.971e-05 | 1.731e-04 |
| 4<-5 | relaxation-diffusion | 2.5000 | 0.0418 | 0.0403 | 3.091e-12 | 4.308e-04 | 8.576e-04 |
| 4<-5 | relaxation-diffusion | 5.0000 | 0.0240 | 0.0230 | 2.871e-12 | 2.244e-04 | 4.980e-04 |
| 4<-5 | relaxation-diffusion | 10.0000 | 0.0079 | 0.0076 | 5.976e-12 | 8.262e-05 | 1.678e-04 |
| 4<-5 | telegraph | 2.5000 | 0.0367 | 0.0351 | 3.816e-12 | 3.956e-04 | 8.049e-04 |
| 4<-5 | telegraph | 5.0000 | 0.0203 | 0.0193 | 3.185e-12 | 1.744e-04 | 3.684e-04 |
| 4<-5 | telegraph | 10.0000 | 0.0060 | 0.0057 | 7.711e-12 | 6.801e-05 | 1.810e-04 |
| 5<-6 | relaxation-diffusion | 2.5000 | 0.0233 | 0.0242 | 7.049e-12 | 6.189e-04 | 0.0014 |
| 5<-6 | relaxation-diffusion | 5.0000 | 0.0133 | 0.0138 | 3.951e-12 | 3.444e-04 | 7.376e-04 |
| 5<-6 | relaxation-diffusion | 10.0000 | 0.0043 | 0.0045 | 1.651e-12 | 8.491e-05 | 1.806e-04 |
| 5<-6 | telegraph | 2.5000 | 0.0198 | 0.0206 | 3.965e-12 | 4.824e-04 | 9.678e-04 |
| 5<-6 | telegraph | 5.0000 | 0.0107 | 0.0111 | 2.048e-12 | 3.137e-04 | 6.835e-04 |
| 5<-6 | telegraph | 10.0000 | 0.0032 | 0.0033 | 2.291e-12 | 5.877e-05 | 1.812e-04 |
| 6<-1 | relaxation-diffusion | 2.5000 | 0.0255 | 0.0299 | 3.622e-12 | 3.356e-04 | 8.164e-04 |
| 6<-1 | relaxation-diffusion | 5.0000 | 0.0146 | 0.0172 | 3.649e-12 | 1.920e-04 | 4.182e-04 |
| 6<-1 | relaxation-diffusion | 10.0000 | 0.0049 | 0.0057 | 1.008e-11 | 6.219e-05 | 1.335e-04 |
| 6<-1 | telegraph | 2.5000 | 0.0212 | 0.0250 | 3.391e-12 | 3.335e-04 | 6.819e-04 |
| 6<-1 | telegraph | 5.0000 | 0.0117 | 0.0137 | 4.422e-12 | 1.611e-04 | 4.126e-04 |
| 6<-1 | telegraph | 10.0000 | 0.0036 | 0.0041 | 1.375e-11 | 6.094e-05 | 1.390e-04 |

## Interpretation boundary

This gate can reject a mediator architecture if its inherited coupling produces no measurable response, violates oddness or the knot envelope, fails attenuation, or remains dynamically indistinguishable from the competing architecture. It still has no independent observed target trajectory. Therefore survival or failure is an architecture result, not discovery of a physical field law.

The mediator remains a one-dimensional relational axis carrying vectors in the supplied `d=3` ambient state. This neither selects three dimensions nor tests suppression of extra ambient directions. No reciprocity, conservation law, photon, spin, charge, QFT, Lorentz, or finite-signal-speed claim follows.

## Reproducibility

- identifiability summary: `reports/response/oriented/oriented_source_mediator_identifiability_2026-07-28.json`
- mediator summary: `reports/response/oriented/local_oriented_mediator_gate_2026-07-28.json`
- source reference: `reports/response/oriented/oriented_vector_fixed_pair_distance_gate_2026-07-26.json`
- analysis revision: `b5b754e95554ef8cdfc90c1971e1aedbc25e9bbb`
- worktree at start: `clean`
- runtime: `42.4103 s`
- command: `python experiments/current/memory/synchronization/mediation/dynamic_common_source_mediator_gate.py`
