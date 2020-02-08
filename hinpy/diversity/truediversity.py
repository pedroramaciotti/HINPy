import numpy as np
from .utils import *

def TrueDiversity(P,alpha,renormalize=False):
    # Convert, check, trim, and renormalize
    P=np.array(P)
    CheckDistribution(P)
    # P=TrimDistribution(P)
    if renormalize:
        P=RenormalizeDistribution(P)
    # Computing the True Diversity
    if alpha==0:
        return P.size
    elif alpha==1:
        return 1.0/np.power(P,P).prod()
    elif alpha>1e3:
        return 1.0/P.max()
    else:
        return np.power(np.power(P,alpha).sum(),1/(1-alpha))
