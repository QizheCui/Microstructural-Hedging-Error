from UctZone import UctZone
import pandas as pd
import matplotlib.pyplot as plt

A = UctZone(0.2, 0.2, 1)
A.get_eff_price(0.01, 100)

A.get_exit_times()
# print(A.tau)
# print(A.obs_price)

A.get_obs_price()

pd.Series(index=A.t, data=A.x).plot(lw=0.5, color='black')
pd.Series(index=A.t, data=A.p).plot(lw=0.5, color='blue')
plt.show()



