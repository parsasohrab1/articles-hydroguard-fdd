# HydroGuard – certified fault diagnosis for hydraulic systems

Condition monitoring of hydraulic equipment (pumps, valves, coolers, accumulators – typical of offshore and process plants).
For each component the tool returns a **set of possible condition grades with a stated confidence (95 %)** instead of a single guess,
and treats an **empty set as an alarm** ("the cycle does not look like anything seen in calibration – inspect, do not trust").

Data: public UCI data set *Condition monitoring of hydraulic systems* (ZeMA gGmbH, 2205 load cycles, 17 sensors, 4 components).
No data is committed; `scripts/run_experiment.py` downloads it and reproduces `outputs/results.json`.

```
pip install -r requirements.txt
PYTHONPATH=src pytest -q
python scripts/run_experiment.py
```

## Measured results (see `outputs/results.json`)
| component | 5-fold accuracy | coverage (target 0.95) | mean set size | empty sets, random split | empty sets, unstable cycles |
|---|---|---|---|---|---|
| cooler | 0.998 | 0.969 | 0.97 | 3 % | 40 % |
| valve | 0.985 | 0.958 | 0.98 | 3 % | 53 % |
| pump leakage | 0.997 | 0.948 | 0.95 | 5 % | 73 % |
| accumulator | 0.990 | 0.948 | 0.95 | 5 % | 11 % |

Limits (read before using): one test rig; cycles of the same rig are split at random, so the 0.95 coverage holds for that rig only.
When calibration is done on stable cycles and testing on the 756 cycles the data set flags as "conditions not yet stable", coverage
falls to 0.20–0.60: the guarantee does **not** survive that shift, but the empty-set rate rises sharply and works as an alarm.
No field data from an operating platform was used. Nothing here is a plant-ready result.

See `docs/SRS.md` and `docs/ARCHITECTURE.md`.
