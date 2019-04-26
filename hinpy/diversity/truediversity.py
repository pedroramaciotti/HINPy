import numpy as np

def TrueDiversity(P,alpha):
    # Convert to array in case it was called on a list
    P=np.array(P)
    # Check that it is a probability distribution
    if np.abs(P.sum()-1)>1e-10:
        raise ValueError('P does not sume 1 (sum=%f)'%P.sum())
    if P[0>P].size!=0:
        raise ValueError('Some elements of P are negative.')
    # Keep only positive parts
    P=P[P>1e-20]
    if alpha==0:
        return P.size
    elif alpha==1:
        return 1.0/np.power(P,P).prod()
    elif alpha>1e20:
        return 1.0/P.max()
    else:
        return np.power(np.power(P,alpha).sum(),1/(1-alpha))
