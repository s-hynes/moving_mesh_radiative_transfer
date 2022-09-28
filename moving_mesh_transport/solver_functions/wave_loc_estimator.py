import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline, CubicSpline

from ..solver_classes.make_phi import make_output
from ..solver_classes.functions import find_nodes



class find_wave:
    """
    This class takes solutions at an array of times, creates interpolated solutions and derivatives, 
    and estimates the wave location at those times
    """
    def __init__(self, N_ang, N_space, ws, M, uncollided, mesh, uncollided_sol, thermal_couple, tfinal, x0, times, find_edges_tol, source_type):
        self.N_ang = N_ang
        self.N_space = N_space
        self.ws = ws
        self.M = M
        self.uncollided = uncollided
        self.mesh = mesh
        self.uncollided_sol = uncollided_sol
        self.thermal_couple = thermal_couple
        self.tfinal = tfinal
        self.x0 = x0
        self.times = times
        self.dx = 1e-3 # step for searching for the wave 
        self.find_edges_tol = find_edges_tol
        self.source_type = source_type

    def find_wave(self, sol):
        self.make_sol(sol)
        left_edge_list = np.zeros(sol.t.size)
        right_edge_list = np.zeros(sol.t.size)
        for it in range(sol.t.size):
        # it = sol.t.size-1
  
            self.interpolated_sol = CubicSpline(self.xs_list[it], self.solutions[it, :])
            self.e_interpolated_sol = CubicSpline(self.xs_list[it], self.e_solutions[it, :])

            xs_range = [0, self.xs_list[it,-1]]
            x_left, x_right = self.find_wave_bounds(xs_range)

            left_edge_list[it] = x_left
            right_edge_list[it] = x_right
            xs_test = np.linspace(self.xs_list[it,0], self.xs_list[it,-1], 1000)
            if it == sol.t.size-1:
                plt.figure(22)
                plt.plot(xs_test, self.interpolated_sol(xs_test,1), '-', label = f'first deriv t={sol.t[it]}')
                plt.xlim(250, self.xs_list[it,-1])
                plt.legend()
                plt.figure(23)
                plt.plot(xs_test, self.interpolated_sol(xs_test,2), '--', label = f'second deriv t={sol.t[it]}')
                plt.legend()
                plt.xlim(350, self.xs_list[it,-1])
                plt.figure(1)
                plt.plot(xs_test, self.interpolated_sol(xs_test,0), '-s', mfc ='none',label = f't={sol.t[it]}')
                plt.xlim(350, self.xs_list[it,-1])
                # print(self.interpolated_sol(xs_test,1))
                plt.legend()
                plt.show()

        return left_edge_list, right_edge_list


    def make_sol(self, sol):
        self.mesh.move(sol.t[-1])
        self.edges = self.mesh.edges
        xs = find_nodes(self.edges, self.M)
        self.solutions = np.zeros((sol.t.size, xs.size))
        self.e_solutions = np.zeros((sol.t.size, xs.size))
        self.xs_list = np.zeros((sol.t.size, xs.size))
        for it in range(sol.t.size):
            self.mesh.move(sol.t[it])
            self.edges = self.mesh.edges
            xs = find_nodes(self.edges, self.M)
            self.xs_list[it,:] = xs
            t = sol.t[it]
            self.mesh.move(t)
            if self.thermal_couple == 0:
                sol_reshape = sol.y[:,it].reshape((self.N_ang,self.N_space,self.M+1))
            elif self.thermal_couple == 1:
                sol_reshape = sol.y[:,it].reshape((self.N_ang+1,self.N_space,self.M+1))

            output = make_output(t, self.N_ang, self.ws, xs, sol_reshape, self.M, self.edges, self.uncollided)
            phi = output.make_phi(self.uncollided_sol)
            e = output.make_e()

            self.solutions[it, :] = phi
            self.e_solutions[it,:] = e

    def find_wave_bounds(self, xs_range):
        left_found = False
        right_found = False


        if self.source_type[1] == 1 or self.source_type[2] == 1:
            x_left = self.x0
            x_right = self.x0
        elif self.source_type[3] == 1 or self.source_type[5] ==1:
            x_left = 0
            x_right = 0
            left_found = True

        mean_free = 1
        edge = xs_range[-1]

        inflection_found = False
        xs_test = np.linspace(0, self.tfinal + self.x0, 100000)
        test_deriv = np.abs(self.interpolated_sol(xs_test,1))

        # tol = np.abs(np.mean(test_deriv) - 8*np.std(test_deriv))
        # tol = 1.05 * np.min(test_deriv)

        tol = np.max(test_deriv)/self.find_edges_tol
        tol_left = tol*1
        tol_right = tol*1
        print(tol, 'tol')

        while left_found == False:
            x_left -= self.dx
            if x_left <= xs_range[0]:
                tol_left = tol_left*1.1
                x_left = self.x0
                print(tol_left, 'new tol left')
                # left_found = True
            elif abs(self.interpolated_sol(x_left,1)) <= tol_left and abs(self.e_interpolated_sol(x_left,1)) <= tol_left:
                left_found = True
                print(x_left, 'left edge')
        while right_found == False:
            x_right += self.dx
            if x_right >= xs_range[-1]:
                tol_right = tol_right*1.05
                x_right = self.x0
                print(tol_right, 'new tol right')
                # right_found = True
            elif abs(self.interpolated_sol(x_right,1)) <= tol_right and abs(self.e_interpolated_sol(x_right,1)) <= tol_right:
                print(x_right, 'right edge')
                right_found = True

        # while inflection_found == False:
        #     second_old = self.second_deriv(edge)
        #     edge -= self.dx
        #     if np.sign(second_old) != np.sign(self.second_deriv(edge)):
        #         inflection_found = True
        #         # print(edge)
        #     elif edge <= 0:
        #         inflection_found = True

        if abs(x_left) < mean_free:
            x_left = mean_free
            print('x_left', x_left)


        return x_left, x_right


