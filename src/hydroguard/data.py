"""Loader for the public UCI 'Condition monitoring of hydraulic systems' data set (ZeMA gGmbH, 2205 cycles)."""
import io, os, urllib.request, zipfile
import numpy as np

URL = "https://archive.ics.uci.edu/static/public/447/condition+monitoring+of+hydraulic+systems.zip"
SENSORS = ["PS1", "PS2", "PS3", "PS4", "PS5", "PS6", "EPS1", "FS1", "FS2",
           "TS1", "TS2", "TS3", "TS4", "VS1", "CE", "CP", "SE"]
TARGETS = ["cooler", "valve", "pump", "accumulator"]


def download(dest="data"):
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, "hydraulic.zip")
    if not os.path.exists(path):
        urllib.request.urlretrieve(URL, path)
    return path


def load(path):
    """Return raw dict sensor -> (cycles x samples), profile (cycles x 5)."""
    z = zipfile.ZipFile(path)
    raw = {s: np.loadtxt(io.StringIO(z.read(s + ".txt").decode())) for s in SENSORS}
    prof = np.loadtxt(io.StringIO(z.read("profile.txt").decode()))
    return raw, prof
