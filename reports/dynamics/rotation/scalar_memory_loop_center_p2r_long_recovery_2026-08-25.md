# P2-R sign-sensitive L3 long recovery

Date: 2026-08-25.

Decision: **`p2r-sign-sensitive-long-recovery-pass`**.

This is an outcome-informed reconciliation of the immutable P2 tail
failure. It does not rename the historical P2 decision.

## Replay controls

| control | observed | pass |
| --- | ---: | :---: |
| complete old-P2 scalar metrics | 120 metrics, max error/tolerance 0 | True |
| long-run 2400 checkpoint replay | all eight response rows | True |
| extended probe off | 1.89392e-14 | True |

## Sign-sensitive recovery

Each range below is over the three frozen late windows.

| waveform | direction | amplitude | branch | signed slope range | log-rate range | max sampled increase | final/peak | signal min | pass |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| sine_cycle | radial | 1e-05 | plus | -0.000117145 .. -5.71106e-06 | 0.65287 .. 0.774868 | -0.0246873 | 4.41019e-06 | 4.41019e-06 | True |
| sine_cycle | radial | 1e-05 | minus | -0.000117144 .. -5.71106e-06 | 0.652877 .. 0.774872 | -0.0246872 | 4.41011e-06 | 4.41011e-06 | True |
| sine_cycle | radial | 3e-05 | plus | -0.000117146 .. -5.7111e-06 | 0.652874 .. 0.774866 | -0.0246872 | 4.41018e-06 | 4.41018e-06 | True |
| sine_cycle | radial | 3e-05 | minus | -0.000117144 .. -5.711e-06 | 0.652871 .. 0.774875 | -0.0246874 | 4.41012e-06 | 4.41012e-06 | True |
| sine_cycle | radial | 0.0001 | plus | -0.000117148 .. -5.71125e-06 | 0.65288 .. 0.774857 | -0.0246871 | 4.41024e-06 | 4.41024e-06 | True |
| sine_cycle | radial | 0.0001 | minus | -0.000117142 .. -5.71085e-06 | 0.652866 .. 0.774885 | -0.0246874 | 4.41006e-06 | 4.41006e-06 | True |
| hann_doublet | radial | 3e-05 | plus | -0.000113973 .. -5.6313e-06 | 0.657293 .. 0.77347 | -0.0248492 | 4.31006e-06 | 4.31006e-06 | True |
| hann_doublet | radial | 3e-05 | minus | -0.000113972 .. -5.63121e-06 | 0.657291 .. 0.773477 | -0.0248491 | 4.31e-06 | 4.31e-06 | True |
| sine_cycle | tangential | 1e-05 | plus | -8.16962e-05 .. -4.72165e-06 | 0.635767 .. 0.777081 | -0.0247678 | 3.54986e-06 | 3.54986e-06 | True |
| sine_cycle | tangential | 1e-05 | minus | -8.16961e-05 .. -4.72164e-06 | 0.635768 .. 0.777082 | -0.0247693 | 3.54983e-06 | 3.54983e-06 | True |
| sine_cycle | tangential | 3e-05 | plus | -8.16963e-05 .. -4.72166e-06 | 0.635767 .. 0.777082 | -0.0247684 | 3.54986e-06 | 3.54986e-06 | True |
| sine_cycle | tangential | 3e-05 | minus | -8.16959e-05 .. -4.72163e-06 | 0.635767 .. 0.777082 | -0.0247688 | 3.54983e-06 | 3.54983e-06 | True |
| sine_cycle | tangential | 0.0001 | plus | -8.16968e-05 .. -4.7217e-06 | 0.635767 .. 0.777082 | -0.0247685 | 3.54989e-06 | 3.54989e-06 | True |
| sine_cycle | tangential | 0.0001 | minus | -8.16954e-05 .. -4.72159e-06 | 0.635768 .. 0.777081 | -0.0247685 | 3.54981e-06 | 3.54981e-06 | True |
| hann_doublet | tangential | 3e-05 | plus | -8.11687e-05 .. -4.71296e-06 | 0.638233 .. 0.775959 | -0.0249189 | 3.52874e-06 | 3.52874e-06 | True |
| hann_doublet | tangential | 3e-05 | minus | -8.11682e-05 .. -4.71292e-06 | 0.638234 .. 0.775959 | -0.0249191 | 3.5287e-06 | 3.5287e-06 | True |

## Decision and limits

Gate components: `{"checkpoint_replay": true, "complete_traces": true, "full_p2_replay": true, "probe_off": true, "recovery": true, "signals_above_floor": true}`.

The historical P2 decision remains **`loop-center-matrix-local-fail`**.
P2-R changes only the observation horizon and the prospectively
declared sign-sensitive recovery question. A pass supports local
recovery of one prepared loop; it is neither an independent
replication nor evidence for formation, a scalar Center mass, a
microscopic actuator, work or physical mass.

## Provenance

- freeze revision: `76145d7bd8ede06d5ae4f3a4166a452794a9e3ae`;
- execution revision: `d5bedacd99f63fbe977943a16df92d8ff1f6f919`;
- source P2 SHA-256: `697b9e9782fa5ba8cf694f8a84c6a931171cdec8a53b42605cb6b7971bc20656`;
- P2-R JSON SHA-256: `484d0c614471980f81a242e3656ccea7793bd4c832f6138621cee575c36c1423`;
- elapsed seconds: `260.011`;
- Python / NumPy / SciPy: `3.12.13` / `2.3.5` / `1.17.1`.
