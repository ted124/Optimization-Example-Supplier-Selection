import numpy as np
from abc import ABC, abstractmethod
from solution import Solution


class Optimizer(ABC):
    """Summary of class here.
    This is an abstract class, all optimizers should inherit this class and implement the abstract method(solver), in
    which you can define how this problem to be solved.

    Attributes:
        price_matrix: A matrix contains the price of all products from all suppliers.
        product_supply: A matrix contains information about what products can each supplier supply.
        product_demand: A vector contrains information about the product demand.
    Notice:
        All three Attributes should be numpy array.
    """

    def __init__(self, price_matrix, product_supply, product_demand):
        self.price_matrix = price_matrix
        self.product_supply = product_supply
        self.product_demand = product_demand
        # number of suppliers
        self._num_supplier = self.product_supply.shape[0]
        # number of product
        self._num_product = self.product_supply.shape[1]
        # supplier list
        self._supplier_list = [supplier for supplier in range(self._num_supplier)]
        # product list
        self._product_list = [product for product in range(self._num_product)]
        self._solution = Solution()

    def is_solvable(self):
        if self._num_supplier == 1:
            return np.all(self.product_supply)
        else:
            return np.all(np.any(self.product_supply, axis=0))

    def get_solution(self):
        return self._solution

    @abstractmethod
    def solver(self):
        """
        define your algorithm here
        """
    def solve(self):
        # check if solvable
        if not self.is_solvable():
            return -1

        # solve
        rc = self.solver()

        return rc

