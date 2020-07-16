from abc import ABC

import numpy as np
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from optimizer import Optimizer
from solution_collector import VarArraySolutionCollector
from solution import Solution

class MinimumSupplierWithMinimumCostOptimizer(Optimizer, ABC):
    """Summary of class here.
    This optimizer will find a solution with minimum amount of supplier which has minimum cost.
    For example, we need at 10 suppliers to cover all the demand, and there are 50 combinations of the suppliers,
    this optimizer will select the combination which has the lowest total cost among all them.
    """

    def __init__(self, price_matrix, product_supply, product_demand):
        super().__init__(price_matrix, product_supply, product_demand)
        # minimum amount of supplier which can cover all the demand
        self.__minimum_amount_supplier = self._num_supplier
        self.__solution_set = []
        self.__solution_count = 0

    def find_minimum_supplier(self):
        # create a solver
        solver = pywraplp.Solver('find minimum amount of supplier',
                                 pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

        # Ci represents if supplier i is selected
        C = [solver.IntVar(0, 1, '') for i in self._supplier_list]

        # constraint: cover all demands
        for j in self._product_list:
            solver.Add(sum(C[i] * self.product_supply[i, j] for i in self._supplier_list) >= 1)

        # object function: minimize the number of suppliers
        solver.Minimize(sum(C[i] for i in self._supplier_list))

        rc = solver.Solve()

        if rc == pywraplp.Solver.OPTIMAL:
            self.__minimum_amount_supplier = int(solver.Objective().Value())
            return 0
        else:
            return -1

    def search_for_all_solutions(self):
        # creat a model
        model = cp_model.CpModel()

        # Ci represents if supplier i is selected
        C = [model.NewIntVar(0, 1, '') for i in self._supplier_list]

        # constraint: cover all demands
        for j in self._product_list:
            model.Add(sum(C[i] * self.product_supply[i, j] for i in self._supplier_list) >= 1)

        # amount of supplier must equals the minimum amount of supplier
        model.Add(sum(C[i] for i in self._supplier_list) == self.__minimum_amount_supplier)

        # create a solver and solve
        solver = cp_model.CpSolver()
        solution_collector = VarArraySolutionCollector([C[i] for i in self._supplier_list])
        status = solver.SearchForAllSolutions(model, solution_collector)

        if status == cp_model.OPTIMAL:
            self.__solution_count = solution_collector.get_solution_count()
            self.__solution_set = solution_collector.get_solutions()
            return 0
        else:
            return -1

    def base_solver(self, supplier_list):
        # calculate price for each product
        price_for_each_product = self.price_matrix[supplier_list].min(axis=0)

        # find supplier for each product
        supplier_for_each_product = [supplier_list[i] for i in self.price_matrix[supplier_list].argmin(axis=0)]

        # selected suppliers
        selected_suppliers = set(supplier_for_each_product)

        # calculate total cost
        cost = np.dot(price_for_each_product, self.product_demand)

        return Solution(supplier_for_each_product, selected_suppliers, cost)

    def solver(self):
        # find minimum amount of supplier
        print("calculating the minimum amount of supplier")
        rcfm = self.find_minimum_supplier()

        if rcfm == -1:
            return -1
        else:
            print("minimum amount of supplier: %d" % self.__minimum_amount_supplier)

        # search all possible solutions
        print("searching for all possible soutions")
        rcsf = self.search_for_all_solutions()

        if rcsf == -1:
            return -1
        else:
            print("found %d possible solutions" % self.__solution_count)

        # loop through all solutions to find the solution with lowest cost
        print("calculating the best solution")
        best_solution = Solution()

        for solution in self.__solution_set:
            temp_solution = self.base_solver(solution)

            # check if cost is lower
            if temp_solution.cost < best_solution.cost:
                best_solution = temp_solution

        self._solution = best_solution

        return 0






