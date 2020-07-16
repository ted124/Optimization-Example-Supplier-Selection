from ortools.sat.python import cp_model
import numpy as np


class VarArraySolutionCollector(cp_model.CpSolverSolutionCallback):
    """Summary of class here.
    This class defines a collector to collect result from the solver
    """

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solutions = []

    def on_solution_callback(self):
        self.__solution_count += 1
        C = [self.Value(v) for v in self.__variables]
        solution = np.where(np.array(C) == 1)[0].tolist()
        self.__solutions.append(solution)

    def get_solution_count(self):
        return self.__solution_count

    def get_solutions(self):
        return self.__solutions