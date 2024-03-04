import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class UctZone:
    def __init__(self, alpha, eta, T=1):
        self.alpha = alpha  # Tick size
        self.eta = eta  # Aversion of price change
        self.T = T  # Total time, default to 1
        self.t = None  # Time grid

        self.x = None  # Theoretical price
        self.p = None  # Observed price

        self.tau = None # Stopping times when x exits the uct zones
        self.obs_price = None # Observed price levels

    def get_eff_price(self, sigma, n, r=0, x0=100):
        """
        Simulate geometric brownian motion under the scheme of Euler-Maruyama
        sigma: volatility
        n: number of time steps 
        r: drift; default to 0
        x0: initial value, default to 100
        """
        dt = self.T/n
        t = np.linspace(0, self.T, n) # time grid
        x = np.zeros(n)
        x[0] = x0
        for i in range(1, n):
            x[i] = x[i-1] + r * x[i-1] * dt + \
                   sigma * x[i-1] * np.sqrt(dt) * np.random.normal()
        self.x = x
        self.t = t
        return self.t, self.x
    
    
    def jump_size(self):
        """
        Generate jump size: potentially a more sophisticated model
        Currently fixed at 1
        """
        L = 1
        return L
    
    
    def get_exit_times(self):
        """
        Get exit times self.tau by theoretical price self.x
        Get a list of observed price levels self.obs_price
        """
        if self.x is None:
            raise ValueError("Theoretical price is not available")
        
        # First observed price k * alpha
        k = self.x[0] // self.alpha
        if abs(k * self.alpha - self.x[0]) < abs((k + 1) * self.alpha - self.x[0]):
            last_obs = k * self.alpha
        else:
            last_obs = (k + 1) * self.alpha
            k = k + 1

        tau = [0]  # stopping times when x exits the uct zones
        obs_price = [last_obs]

        i = 1
        L = self.jump_size()  # Initial jump size
        while i < len(self.x):
            if self.x[i] > last_obs + self.alpha * (L - 0.5 + self.eta):  # ascend
                tau.append(i)
                last_obs += self.alpha * L
                obs_price.append(last_obs)
                L = self.jump_size()  # Draw the jump size again
            elif self.x[i] < last_obs - self.alpha * (L - 0.5 + self.eta):  # descend
                tau.append(i)
                last_obs -= self.alpha * L
                obs_price.append(last_obs)
                L = self.jump_size()  # Draw the jump size again
            i += 1
        
        self.tau = np.array(tau)
        self.obs_price = np.array(obs_price)

        return self.tau

    def select_time(self, a, b):
        """
        Use a beta distribution to pick a point between a, b
        Parameters for beta distribution yet to be specified
        currently set at 2, 5
        """
        return np.random.beta(2, 5) * (b - a) + a

    def get_obs_price(self, jump_mode='beta'):
        """
        Get observed price self.p by connecting the observed price levels self.obs_price
        Select the time to jump using a determined distribution
        
        select_time: default to 'beta', can also be 'left' or 'right'(naive)
        """
        if self.x is None:
            raise ValueError("Theoretical price is not available")
        if self.tau is None:
            raise ValueError("Exit times are not available")

        p = [None] * len(self.x)
        p[0] = self.obs_price[0]

        for j in range(len(self.tau) - 1):
            if jump_mode=='beta':
                jump_time = self.select_time(self.tau[j], self.tau[j+1])
                jump_index = np.round(jump_time, 0).astype(int)
            elif jump_mode=='left':
                jump_index = self.tau[j]
            elif jump_mode=='right':
                jump_index = self.tau[j+1]
            p[jump_index] =self.obs_price[j]
        
        # Connect p
        for i in range(len(p)):
            if p[i] is None:
                p[i] = p[i-1]
        
        self.p = np.round(p, 2)
        return self.p
    
    def plot(self, grid=False, exit_time=False, save=False, filename=None):
        """
        Plot the theoretical price and observed price
        grid: whether to add grids as k * alpha, default to False
        exit_time: whether to mark the exit times, default to False
        save, filename: whether to save the plot and the filename, default to False and None
        """
        if self.x is None:
            raise ValueError("Theoretical price is not available")
        if self.p is None:
            raise ValueError("Observed price is not available")
        
        fig, ax = plt.subplots(figsize=(12, 5))
        pd.Series(index=self.t, data=self.x).plot(
            lw=0.7, color='teal', ax=ax, label="Theoreteical Price")  # Theoretical price
        ax.step(self.t, self.p, '--',where='post', 
                color='coral', lw=0.7, label="Observed Price")  # Observed price
        
        # Add grids: k * alpha
        if grid:
            ax.set_yticks(np.arange(self.p.min(), self.p.max() + self.alpha, self.alpha))
            ax.grid(True, linestyle='-', linewidth=0.3, color='gray', alpha=0.3)
            # Keep 1/5 label
            y_ticks = ax.get_yticks()
            new_y_tick_labels = ['' for _ in y_ticks]
            for i, tick in enumerate(y_ticks):
                if i % 5 == 0:  # Keep every tenth label
                    new_y_tick_labels[i] = f'{tick:.2f}'
            ax.set_yticklabels(new_y_tick_labels)

        # Mark the exit times
        if exit_time:
            ax.plot([self.t[i] for i in self.tau],
                    [self.x[i] for i in self.tau], 'x', color='coral', markersize=4, label="Exit times")

        # Output the file
        if save:
            if filename is None:
                raise ValueError("Please specify the filename")
            plt.savefig(filename, dpi=200)

        # Show the plot
        ax.legend()
        plt.tight_layout()
        plt.show()
