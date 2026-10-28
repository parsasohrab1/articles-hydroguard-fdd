# Architecture
sensor cycle -> `features.cycle_features` -> random-forest probabilities (per component) -> `conformal.threshold` (calibration cycles) -> `conformal.sets` -> diagnosis set or **out-of-envelope alarm** -> maintenance work order / dashboard.

- `src/hydroguard/data.py` public data loader; `features.py` statistics; `conformal.py` split-conformal sets and audit metrics.
- `scripts/run_experiment.py` end-to-end evaluation; `outputs/results.json` measured numbers; `tests/` unit test of the coverage guarantee.
- Deployment: stateless Python service next to the historian; calibration set refreshed after overhauls.
