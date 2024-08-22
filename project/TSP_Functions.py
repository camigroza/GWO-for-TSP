import numpy as np


# calculate euclidian distance between two points
def calc_dist(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# generate the distance matrix based on cities coordinates
def make_dist_matrix(x_coord, y_coord):
    num_cities = len(x_coord)
    dist_matrix = np.zeros((num_cities, num_cities))

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                dist_matrix[i, j] = calc_dist(x_coord[i], y_coord[i], x_coord[j], y_coord[j])

    return dist_matrix


# Calculate the total distance of a tour
def calc_total_dist(tour, dist_matrix):
    total_dist = 0

    for i in range(len(tour) - 1):
        total_dist += dist_matrix[tour[i], tour[i + 1]]

    total_dist += dist_matrix[tour[-1], tour[0]]

    return total_dist


# Function to repair an invalid permutation
def repair_permutation(wolf):
    # what the elements are and how many times they appear
    unique_elements, counts = np.unique(wolf, return_counts=True)

    # what elements appear more than one time
    duplicate_elements = unique_elements[counts > 1]

    for element in duplicate_elements:
        indices = np.where(wolf == element)[0]

        for index in indices[1:]:
            # replace duplicate element with a randomly selected unused city
            unused_cities = np.setdiff1d(range(len(wolf)), wolf)
            replacement = np.random.choice(unused_cities)
            wolf[index] = replacement

    return wolf


# partially mapped crossover
def crossover(parent1, parent2, break_point):
    for i in range(break_point):
        index = list(parent1).index(parent2[i])
        parent1[i], parent1[index] = parent1[index], parent1[i]

    return parent1


# neighborhood seach
def neighborhood_search(solution, dist_matrix):
    # two-swap mutation
    new_solution_1 = solution.copy()
    index1, index2 = np.random.choice(len(solution), 2, replace=False)
    new_solution_1[index1], new_solution_1[index2] = new_solution_1[index2], new_solution_1[index1]

    # two-opt
    new_solution_2 = solution.copy()
    index1, index2 = np.random.choice(len(solution), 2, replace=False)
    new_solution_2[index1:index2 + 1] = new_solution_2[index1:index2 + 1][::-1]

    fitness1 = calc_total_dist(new_solution_1, dist_matrix)
    fitness2 = calc_total_dist(new_solution_2, dist_matrix)

    if fitness1 < fitness2:
        return new_solution_1
    return new_solution_2


# adaptive crossover
def adaptive_crossover(alpha, beta, delta, omega, break_point, dist_matrix):
    solution1 = crossover(alpha, omega, break_point)
    solution2 = crossover(beta, omega, break_point)
    solution3 = crossover(delta, omega, break_point)

    solutions = [omega, solution1,solution2, solution3]

    fitness_values = [calc_total_dist(solution, dist_matrix) for solution in solutions]
    best_solution_index = np.argmin(fitness_values)
    best_solution = solutions[best_solution_index]

    return best_solution
