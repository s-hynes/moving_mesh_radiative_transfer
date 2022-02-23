"""Created on Thu Feb  3 15:12:33 2022@author: bennett"""import h5py import numpy as npimport mathfrom scipy.interpolate import interp1dimport scipy.integrate as integrate import matplotlib.pyplot as pltclass integrate_ganapol:    def __init__(self, npnts, x0):        self.t = 0        self.x_list = np.linspace(-1,1)        self.sol_list = self.x_list*0        self.x0 = x0        self.source_type = "empty"        self.npnts = npnts        ###########################################################################        def xi(self, u, eta):        q = (1+eta)/(1-eta)        zz = np.tan(u/2)        return (np.log(q) + complex(0, u))/(eta + complex(0, zz))        def ival(self, x, t):        eta = x/t        t1 = math.exp(-t)/2/t        t2 = (t/4/math.pi) * (1 - eta**2)        if abs(x) < t:            term =  t1 * (1 + t2 * self.integral_term(t, eta))        elif abs(x) == t:            term = math.exp(-t)/2/t        else:            term = 0        return term        def integrand(self, u, t, eta):        eval_xi = self.xi(u, eta)        # complex_term = (eval_xi**2 * math.exp(t * (1-eta**2) * eval_xi / 2))        complex_term = np.exp(t*((1 - eta**2)*eval_xi/2.))*eval_xi**2        return (1/np.cos(u/2))**2*complex_term.real            def integral_term(self, t, eta):        return integrate.quad(self.integrand, 0 , math.pi, args = (t, eta), epsabs = 1e-15, epsrel = 1e-13, limit = 1000)[0]        ###########################################################################    def source(self, s, t):        if self.source_type == "square":            return np.heaviside(self.x0 - np.abs(s), 1)        elif self.source_type =="gaussian":            return np.exp(-4*s*s)                        def greens_function_times_source(self, s, tau, x):        return self.ival(x-s, self.t - tau) * self.source(s, self.t)        def integrate_greens_function(self, x):        for i in range(self.x_list.size):            if self.source_type == "gaussian":                result = integrate.quad(self.greens_function_times_source, -np.inf, np.inf, args = (0, self.x_list[i]))[0]            else:                result = integrate.quad(self.greens_function_times_source, -self.x0, self.x0, args = (0, self.x_list[i]))[0]            self.sol_list[i] = result    def plane_source(self,t):        self.t = t        self.x_list = np.linspace(0, self.t , self.npnts)        self.sol_list = self.x_list*0        for i in range(self.x_list.size):            self.sol_list[i] = self.ival(self.x_list[i], self.t)                def square_IC(self, t):        self.t = t        self.source_type = "square"        self.x_list = np.linspace(0, self.t + self.x0, self.npnts)        self.sol_list = self.x_list*0        for i in range(self.x_list.size):            self.integrate_greens_function(self.x_list[i])                def gaussian_IC(self, t):        self.t = t         self.source_type = "gaussian"        self.x_list = np.linspace(0, self.t + self.x0, self.npnts)        self.sol_list = self.x_list*0        for i in range(self.x_list.size):            self.integrate_greens_function(self.x_list[i])                                        # xs = np.linspace(-1,1, 20)# t = 1# bench = integrate_ganapol(xs, t, 1/2)# # bench.plane_source()# # bench.square_IC()# bench.truncated_gaussian_IC()# sol = bench.sol_list# # print(sol)# plt.plot(xs, sol)