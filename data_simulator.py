import numpy as np

class DataSimulator(object):
    """Summary of class here.
    Data simulation for supplier selection optimization problem
    this simulator will return:
    1. A matrix contains the price of all products from all suppliers
    2. A matrix contains information about what products can each supplier supply
    3. A vector contrains information about the product demand

    Attributes:
        num_supplier: number of suppliers
        num_product: number of products
        probability: probability of each supplier has each product
        price_lb: lower bound of price for all products
        price_ub: upper bound of price for all products
        demand_lb: upper bound of demand for all products
        demand_up: upper bound of demand for all products
    """

    def __init__(self, num_supplier, num_product, probability, price_lb, price_ub, demand_lb, demand_up):
        self.num_supplier = num_supplier
        self.num_product = num_product
        self.__product_supply = np.random.choice(2, size=(self.num_supplier, self.num_product),
                                                 p=[1 - probability, probability])
        # if supplier i doesn't have product j => price_matrix[i, j] = 0
        self.__price_matrix = np.round(np.random.uniform(price_lb, price_ub, size=(self.num_supplier, self.num_product)),
                                       decimals=2) * self.__product_supply
        self.__product_demand = np.random.randint(demand_lb, demand_up, size=self.num_product)

    def get_product_supply(self):
        return self.__product_supply

    def get_price_matrix(self):
        return self.__price_matrix

    def get_product_demand(self):
        return self.__product_demand







