from data_simulator import DataSimulator
from minimum_supplier_with_minimum_cost import MinimumSupplierWithMinimumCostOptimizer

def main():
    # create a data simulator
    data_simulator = DataSimulator(num_supplier=50, num_product=2000, probability=0.95, price_lb=1, price_ub=100,
                                   demand_lb=10, demand_up=100)

    # simulate data
    price_matrix = data_simulator.get_price_matrix()
    product_supply = data_simulator.get_product_supply()
    product_demand = data_simulator.get_product_demand()

    # create a optimizer
    optimizer = MinimumSupplierWithMinimumCostOptimizer(price_matrix, product_supply, product_demand)

    # solve
    rc = optimizer.solve()

    if rc == 0:
        print("found solution")
        solution = optimizer.get_solution()
        print("selected suppliers: %s" % solution.selected_suppliers)
        print("total cost: %d" % solution.cost)


if __name__ == '__main__':
    main()