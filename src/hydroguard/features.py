"""Cycle-level statistics: mean, std, min, max, 10th and 90th percentile of every sensor."""
import numpy as np


def cycle_features(raw):
    cols, names = [], []
    for s, m in raw.items():
        for n, f in [("mean", lambda x: x.mean(1)), ("std", lambda x: x.std(1)), ("min", lambda x: x.min(1)),
                     ("max", lambda x: x.max(1)), ("p10", lambda x: np.percentile(x, 10, axis=1)),
                     ("p90", lambda x: np.percentile(x, 90, axis=1))]:
            cols.append(f(m)); names.append(f"{s}_{n}")
    return np.column_stack(cols), names
