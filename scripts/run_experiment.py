"""Reproduces every number in outputs/results.json from the public UCI hydraulic data set."""
import json, sys, os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from hydroguard import data, features, conformal

ALPHA, N_SPLITS = 0.05, 20
raw, prof = data.load(data.download(os.path.join(os.path.dirname(__file__), "..", "data")))
X, names = features.cycle_features(raw)
stable = prof[:, 4] == 0
res = {"n_cycles": int(len(X)), "n_features": int(X.shape[1]), "n_stable": int(stable.sum()), "alpha": ALPHA, "components": {}}


def rf(seed):
    return RandomForestClassifier(n_estimators=200, min_samples_leaf=1, n_jobs=-1, random_state=seed)


for j, comp in enumerate(data.TARGETS):
    raw_y = prof[:, j]
    classes = np.unique(raw_y); y = np.searchsorted(classes, raw_y)
    # 1) point accuracy, stratified 5-fold
    pred = np.empty(len(y), int)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
        pred[te] = rf(0).fit(X[tr], y[tr]).predict(X[te])
    out = {"classes": [float(c) for c in classes], "accuracy_cv5": float(accuracy_score(y, pred)),
           "macro_f1_cv5": float(f1_score(y, pred, average="macro"))}
    # 2) split-conformal, repeated random 60/20/20 splits
    runs = []
    for s in range(N_SPLITS):
        rng = np.random.default_rng(s); idx = rng.permutation(len(y)); a, b = int(.6 * len(y)), int(.8 * len(y))
        tr, ca, te = idx[:a], idx[a:b], idx[b:]
        m = rf(s).fit(X[tr], y[tr]); pc = m.predict_proba(X[ca]); pt = m.predict_proba(X[te])
        q = conformal.threshold(pc, y[ca], ALPHA); runs.append(conformal.evaluate(conformal.sets(pt, q), y[te]))
    out["conformal_random_split"] = {k: [float(np.mean([r[k] for r in runs])), float(np.std([r[k] for r in runs]))] for k in runs[0]}
    # 3) shift: calibrate on stable cycles, test on cycles flagged 'not yet stable'
    if (~stable).sum() > 50:
        rng = np.random.default_rng(0); si = rng.permutation(np.where(stable)[0]); a = int(.7 * len(si))
        tr, ca, te = si[:a], si[a:], np.where(~stable)[0]
        m = rf(0).fit(X[tr], y[tr]); q = conformal.threshold(m.predict_proba(X[ca]), y[ca], ALPHA)
        out["conformal_stable_to_unstable"] = {"n_test": int(len(te)), **conformal.evaluate(conformal.sets(m.predict_proba(X[te]), q), y[te]),
                                               "accuracy": float(accuracy_score(y[te], m.predict(X[te])))}
    res["components"][comp] = out
    print(comp, out["accuracy_cv5"], out["conformal_random_split"]["coverage"], flush=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "outputs"), exist_ok=True)
json.dump(res, open(os.path.join(os.path.dirname(__file__), "..", "outputs", "results.json"), "w"), indent=1)
