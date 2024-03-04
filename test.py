from UctZone import UctZone

# Change this to test different parameters
A = UctZone(alpha=0.05, eta=0.2)  # for clearer plot set alpha=0.5
A.get_eff_price(n=10*8*3600, \
                sigma=0.3 /(252**0.5), r=0.05 / 360)  # Daily drift and volatility

A.get_exit_times()
# print(A.tau)
# print(A.obs_price)

A.get_obs_price(jump_mode="left")

A.plot(grid=True, exit_time=False, 
       save=True, filename="test-path.png")
