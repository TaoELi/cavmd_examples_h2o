import numpy as np
import sys

filename = sys.argv[-1]

data = np.loadtxt(filename)

mu = np.mean(data, axis=0)
print("%.6f %.6f %.6f" %(mu[0], mu[1], mu[2]))
