import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange

# -----------------------------
# parameters
# -----------------------------

sigma1=1.0
kappa=3.0
sigma2=kappa*sigma1

A=1.0
beta=0.2
B=beta*A

T=150000
window=5000

# -----------------------------
# kernel gradient
# -----------------------------

@njit
def grad_kernel(dx):

    r2=np.dot(dx,dx)

    g1=np.exp(-r2/(2*sigma1**2))
    g2=np.exp(-r2/(2*sigma2**2))

    pref=(-A/sigma1**2)*g1 + (B/sigma2**2)*g2

    return pref*dx

# -----------------------------
# two-body simulation
# -----------------------------

@njit
def run_two_body(d,eps,eta,a):

    x1=np.random.randn(d)
    x2=-x1

    rmean=0.0
    rvar=0.0
    count=0

    for t in range(T):

        dx=x1-x2
        r2=np.dot(dx,dx)

        g1=np.exp(-r2/(2*sigma1**2))
        g2=np.exp(-r2/(2*sigma2**2))

        pref=(-A/sigma1**2)*g1 + (B/sigma2**2)*g2

        f = pref*dx

        for i in range(d):

            noise1=eps*np.random.randn()
            noise2=eps*np.random.randn()

            x1[i]+=noise1-eta*f[i]
            x2[i]+=noise2+eta*f[i]

        r=np.sqrt(np.dot(x1-x2,x1-x2))

        if t>=T-window:

            rmean+=r
            rvar+=r*r
            count+=1

    rmean/=count
    rstd=np.sqrt(rvar/count-rmean*rmean)

    return rmean,rstd

Xi_vals=np.linspace(5,50,30)
alpha_vals=np.linspace(0.001,0.05,30)

d=3
eta=0.05

phase=np.zeros((len(alpha_vals),len(Xi_vals)))

for i,a in enumerate(alpha_vals):
    for j,Xi in enumerate(Xi_vals):

        eps=np.sqrt(2*eta/Xi)

        rmean,rstd=run_two_body(d,eps,eta,a)

        phase[i,j]=rstd/rmean

plt.imshow(phase,
           extent=[Xi_vals[0],Xi_vals[-1],
                   alpha_vals[0],alpha_vals[-1]],
           origin="lower",
           aspect="auto")

plt.xlabel("Xi")
plt.ylabel("alpha")
plt.colorbar(label="relative radius fluctuation")
plt.show()