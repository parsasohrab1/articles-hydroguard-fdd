import numpy as np
from hydroguard.conformal import threshold, sets, evaluate


def test_coverage_on_synthetic():
    rng = np.random.default_rng(0)
    def draw(n):
        y = rng.integers(0, 3, n); p = rng.dirichlet([1, 1, 1], n); p[np.arange(n), y] += 1.0; p /= p.sum(1, keepdims=True)
        return p, y
    pc, yc = draw(2000); pt, yt = draw(4000)
    q = threshold(pc, yc, 0.1)
    assert evaluate(sets(pt, q), yt)["coverage"] >= 0.88
