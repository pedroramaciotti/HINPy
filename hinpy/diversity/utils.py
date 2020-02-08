import numpy as np

def CheckDistribution(P):
    if np.abs(np.sum(P)-1)>1e-6:
        raise ValueError('P does not sume 1 (sum=%f)'%P.sum())
    if P[0>P].size!=0:
        raise ValueError('Some elements of P are negative.')
    return;

def TrimDistribution(P,tol=1e-8):
    P=np.array(P)
    P=P[P>tol]
    if np.abs(P.sum()-1)>tol:
        raise ValueError('Trimming the probability distribution resulted in it not summing up to zero.')
    return P;

def RenormalizeDistribution(P):
    P=np.array(P)
    P=P[:-1]
    if not np.abs(P.sum())>1e-8:
        raise ValueError('Cannot renormalize: all the mas was int he sink node.')
    return P/P.sum();
