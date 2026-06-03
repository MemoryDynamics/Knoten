import os
import time

import numpy as np

src = "progress.npy"


def wait_until_stable(path, delay=0.5):
    size1 = os.path.getsize(path)
    time.sleep(delay)
    size2 = os.path.getsize(path)
    return size1 == size2


# Warten, bis die Datei nicht mehr wächst
while not wait_until_stable(src):
    time.sleep(0.2)

print("Loading…")
D_spec, D_cov, R2_map = np.load(src, allow_pickle=True)

print("Loaded types:", type(D_spec), type(D_cov), type(R2_map))
print("Shapes:", D_spec.shape, D_cov.shape, R2_map.shape)
print("NaNs:", np.isnan(D_spec).sum(), np.isnan(D_cov).sum(), np.isnan(R2_map).sum())
