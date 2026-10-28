# HydroGuard – Software Requirements (SRS)
1. Purpose: give maintenance teams a diagnosis for hydraulic components with an explicit confidence statement and an alarm when the data is out of envelope.
2. Users: reliability engineers, offshore/process maintenance planners; client IT for integration.
3. Inputs: one load cycle per record from the 17 rig sensors (pressure, motor power, flow, temperature, vibration, derived efficiencies).
4. Functional requirements
   - FR1 Compute cycle features (mean, std, min, max, P10, P90 per sensor).
   - FR2 Classify cooler, valve, pump-leakage and accumulator grade.
   - FR3 Return a prediction set at confidence 1-alpha (default 95 %) calibrated on held-out cycles.
   - FR4 Raise "out of envelope" when the set is empty; recommend inspection.
   - FR5 Report per-class coverage and set size for audit.
5. Non-functional: reproducible from public data; no data leaves the site; model re-calibration without retraining (< 1 min).
6. Out of scope: remaining-useful-life prediction, control actions, safety-instrumented functions.
7. Acceptance: reproduce `outputs/results.json`; coverage within 0.03 of target on random splits of the reference data.
