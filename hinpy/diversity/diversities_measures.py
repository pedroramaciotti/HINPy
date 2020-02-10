# import numpy as np
# from .truediversity import TrueDiversity
# from .utils import *
# from scipy.stats import entropy


# def Richeness(P,renormalize=False):
#     # Convert, check, trim, and renormalize
#     P=np.array(P)
#     CheckDistribution(P)
#     P=TrimDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     return P.size;

# def ShannonEntropy(P,base=2,renormalize=False):
#     # Convert, check, trim, and renormalize
#     P=np.array(P)
#     CheckDistribution(P)
#     P=TrimDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     # Computing entropy
#     return entropy(P,base=base);

# def ShannonEvenness(P,base=2,renormalize=False):
#     # Convert, check, trim, and renormalize
#     P=np.array(P)
#     CheckDistribution(P)
#     P=TrimDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     # Computing entropy
#     return ShannonEntropy(P,base=base)/P.size;

# def HHI(P,renormalize=False):# Herfindahl-Hirschman Index
#     # Convert, check, trim, and renormalize
#     P=np.array(P)
#     CheckDistribution(P)
#     P=TrimDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     # Computing entropy
#     return np.power(P,2).sum();

# def GiniIndex(P,renormalize=False):
#     # (Warning: This is a concise implementation, but it is O(n**2)
#     # in time and memory, where n = len(x).  
#     # Convert, check.
#     P=np.array(P)
#     CheckDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     # Computing Gini Index
#     return np.abs(np.subtract.outer(P, P)).sum()/(2.0*P.size);

# def BPI(P,renormalize=False): # Berger-Parker Index
#     # Convert, check, and renormalize
#     P=np.array(P)
#     CheckDistribution(P)
#     if renormalize:
#         P=RenormalizeDistribution(P)
#     return P.max();
