import numpy as np


class Solution(object):
    """Summary of class here.
    This class defines the solution.
    Each solution should contains four parts:
    1. supplier for each product
    2. selected supplier
    3. total cost
    """

    def __init__(self, supplier_for_each_product=[], selected_suppliers=None, cost=np.Inf):
        self.supplier_for_each_product = supplier_for_each_product
        if selected_suppliers is None:
            self.selected_suppliers = set()
        else:
            self.selected_suppliers = selected_suppliers
        self.cost = cost
