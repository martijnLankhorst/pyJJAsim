from pyjjasim import *

import matplotlib.pyplot as plt

"""
EXAMPLE 4: Parameter optimization

Compute maximal frustration bounds and maximal current 
"""

if __name__ == "__main__":
    # define arrays
    array = SquareArray(12, 12)
    Ih, Iv = 1.0 * array.horizontal_junctions(), 1.0 * array.vertical_junctions()

    # compute frustration bounds for zero vortex state
    prob = StaticProblem(array, current_sources=0)
    (smallest_f, largest_f), (s_config, l_config), _ = prob.compute_frustration_bounds()
    print(f"smallest and largest frustration for which the zero-vortex state exists: {smallest_f}, {largest_f}")
    s_config.plot(title=f"minimal frustration in zero vortex state (f={np.round(smallest_f, 4)})")

    # compute maximal current
    prob = StaticProblem(array, frustration=0, current_sources=Iv)
    I_factor, net_I, max_I_config, info = prob.compute_maximal_current()
    np.set_printoptions(linewidth=10000000)
    print(f"largest current factor {I_factor} (corresponding to net current of  {net_I}) at which the zero-vortex state exists at zero frustration")
    max_I_config.plot(title=f"maximal current in zero vortex state (net_I={np.round(net_I, 4)})")

    # compute extermum in Is-f space using compute_stable_region()
    prob = StaticProblem(array, frustration=0, current_sources=Iv)
    f, net_I, _, _ = prob.compute_stable_region()
    plt.subplots()
    plt.plot(f, net_I)
    plt.xlabel("frustration")
    plt.ylabel("net I")
    plt.title("Region in f-I parameter space where the zero-vortex state is stable")

    # compute direction dependent maximal current using compute_maximal_parameter()
    prob = StaticProblem(array)
    angles = np.linspace(0, 2*np.pi, 33)
    I_factor = np.zeros(len(angles))
    for i, angle in enumerate(angles):
        prob_func = lambda x: prob.new_problem(current_sources=x * (np.cos(angle) * Ih + np.sin(angle) * Iv))
        I_factor[i], _, _, _ = compute_maximal_parameter(prob_func)
    plt.subplots()
    plt.plot(np.cos(angles) * I_factor, np.sin(angles) * I_factor, marker="o")
    plt.xlabel("horizontal current")
    plt.ylabel("vertical current")
    plt.title("angle dependent maximal current for zero-vortex state")
    plt.show()
