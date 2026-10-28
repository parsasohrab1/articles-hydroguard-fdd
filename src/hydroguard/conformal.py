"""Split-conformal prediction sets (LAC score = 1 - p_true) with a finite-sample quantile."""
import numpy as np


def threshold(p_cal, y_cal, alpha):
    s = 1.0 - p_cal[np.arange(len(y_cal)), y_cal]
    n = len(s)
    k = min(int(np.ceil((n + 1) * (1 - alpha))), n)
    return np.sort(s)[k - 1]


def sets(p, q):
    return (1.0 - p) <= q          # boolean matrix: class kept in the set


def evaluate(S, y):
    n = len(y)
    cov = S[np.arange(n), y].mean()
    size = S.sum(1)
    per_class = {int(c): float(S[y == c, c].mean()) for c in np.unique(y)}
    return dict(coverage=float(cov), mean_size=float(size.mean()), singleton=float((size == 1).mean()),
                empty=float((size == 0).mean()), min_class_coverage=min(per_class.values()))
