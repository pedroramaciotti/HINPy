import hinpy

import calendar
import numpy as np
# Load 
hin = hinpy.classes.HIN(name='m100k',filename='movielens100k_hin.csv')


hin.GetLinkGroupsNames()

# ['is_of_type',
#  'was_released',
#  'rates',
#  'has_occupation',
#  'has_age',
#  'has_gender',
#  'is_located']

hin.GetObjectGroupsNames()

# ['age',
#  'occupation',
#  'genre',
#  'zip_code',
#  'user',
#  'movie',
#  'gender',
#  'release']

months =  [(9,1997),(10,1997),(11,1997),(12,1997),(1,1998),(2,1998),(3,1998),(4,1998)]


N_genres = hin.GetObjectGroup('genre').size # there are 19 film genres

collective_diversity = [] 
mean_diversity = []
collective_pa = np.zeros((N_genres,len(months)))

for i,(month,year) in enumerate(months):
    first_day = '%d-%d-%d'%(year,month,1)
    last_day  = '%d-%d-%d'%(year,month,calendar.monthrange(year,month)[1])
    window = {'min':first_day,'max':last_day,}
    hin.CreateLinkGroup(linkgroup='rates',name='monthly_activity',datetimes=window)
    collective_diversity.append(hin.collective_diversity(['monthly_activity','is_of_type'],alpha=2.0))
    mean_diversity.append(hin.mean_diversity(['monthly_activity','is_of_type'],alpha=2.0))
    collective_pa[:,i] = hin.proportional_abundance(['monthly_activity','is_of_type'])
    hin.DeleteLinkGroup('monthly_activity')
    
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1)
axs[0].stackplot(np.arange(len(months)),collective_pa,baseline='zero')
axs[0].set_xticklabels(['%d-%d'%(y,m) for m,y in months],rotation = 45, ha="left")
axs[1].plot(np.arange(len(months)),collective_diversity)
axs[1].plot(np.arange(len(months)),mean_diversity)
axs[1].legend(['Collective diversity','Mean diversity'])
axs[1].set_xticklabels(['%d-%d'%(y,m) for y,m in months],rotation = 45, ha="left")
plt.tight_layout()
plt.savefig('temporal_series.pdf')
plt.clf()
plt.close()
