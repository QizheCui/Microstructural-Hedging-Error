import numpy as np

class UctZone:
    def __init__(self, alpha, eta, T):
        self.alpha = alpha  # Tick size
        self.eta = eta  # Aversion of price change
        self.T = T

        self.x = None  # Efficient price
        self.p = None  # Observed price
    
        self.tau = None # Stopping times when x exits the uct zones
        self.obs_price = None # Observed price to consider
        
    def get_eff_price(self, sigma, n, x0=0):
        """
        Simulate geometric brownian motion under the scheme of Euler-Maruyama
        n: number of time steps 
        T: terminal time
        x0: initial value
        """
        dt = self.T/n
        t = np.linspace(0, self.T, n) # time grid
        x = np.zeros(n)
        x[0] = x0
        for i in range(1, n):
            x[i] = x[i-1] + sigma * x[i-1] * np.sqrt(dt) * np.random.normal()
        self.x = x
        return t, self.x
    
    
    def jump_size(self):
        """
        Generate jump size: potentially a more sophisticated model
        Currently fixed at 1
        """
        L = 1
        return L
    
    
    def get_exit_times(self):
        """
        Get exit times self.tau by efficient price self.x
        Get a list of observed price levels self.obs_price
        """
        if self.x is None:
            raise ValueError("Efficient price is not available")
        
        # First grid and grid price
        k = self.x[0] // self.alpha
        if k * self.alpha - self.x[0] < (k + 1) * self.alpha - self.x[0]:
            last_obs = k * self.alpha
        else:
            last_obs = (k + 1) * self.alpha
            k = k + 1

        tau = [0]  # stopping times when x exits the uct zones
        obs_price = [last_obs]

        i = 1
        while i < len(self.x):
            L = self.jump_size()
            while True:
                if self.x[i] > last_obs + self.alpha * (L - 0.5 + self.eta):  # ascend
                    tau.append(i)
                    last_obs += self.alpha * L
                    obs_price.append(last_obs)
                    break
                elif self.x[i] < last_obs - self.alpha * (L - 0.5 + self.eta):  # descend
                    tau.append(i)
                    last_obs -= self.alpha * L
                    obs_price.append(last_obs)
                    break
                i += 1
        
        self.tau = np.array(tau)
        self.obs_price = np.array(obs_price)

        return self.tau

    def get_obs_price(self):
        """
        Get observed price self.p by connecting the observed price levels self.obs_price
        Select the time to jump using a determined distribution
        """
        if self.x is None:
            raise ValueError("Efficient price is not available")
        if self.tau is None:
            raise ValueError("Exit times are not available")

        def select_time(a, b):
            # Use a beta distribution to pick a point between a, b
            # Parameters for beta distribution yet to be specified
            # currently set at 2, 5
            return np.random.beta(2, 5) * (b - a) + a

        p = None * len(self.x)
        p[0] = self.obs_price

        for j in range(len(self.tau) - 1):
            jump_time = select_time(self.tau[j], self.tau[j+1])
            p[jump_time] =self.obs_price[j]
        
        # Connect p
        for i in range(len(p)):
            if p[i] is None:
                p[i] = p[i-1]
        
        self.p = np.array(p)
        return self.p
    