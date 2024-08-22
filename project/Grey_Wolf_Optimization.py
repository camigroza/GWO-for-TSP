from TSP_Functions import *


# Grey Wolf Optimization for TSP
def GWO(dist_matrix, num_wolves, max_iterations):
    num_cities = dist_matrix.shape[0]

    # initialize wolves
    wolves = [np.random.permutation(num_cities) for _ in range(num_wolves)]

    # get the best solution
    fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]
    best_wolf_index = np.argmin(fitness_values)
    best_solution_general = wolves[best_wolf_index]

    iteration_counter = 0

    while iteration_counter < max_iterations:
        fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]

        # determine alpha, beta and delta wolves
        sorted_indices = np.argsort(fitness_values)
        alpha = wolves[sorted_indices[0]]
        beta = wolves[sorted_indices[1]]
        delta = wolves[sorted_indices[2]]

        # update position of each wolf based on the positions of alpha, beta and delta wolves
        for i in range(num_wolves):
            for j in range(num_cities):
                r1, r2 = np.random.rand(2)

                # in [-1, 1]
                A1 = 2 * r1 - 1
                A2 = 2 * r2 - 1

                # in [0,2]
                C1 = 2 * r1
                C2 = 2 * r2

                # distances to alpha, beta and omega wolves
                D_alpha = abs(C1 * alpha[j] - wolves[i][j])
                D_beta = abs(C2 * beta[j] - wolves[i][j])
                D_delta = abs(C2 * delta[j] - wolves[i][j])

                wolves[i][j] = np.clip((alpha[j] - A1 * D_alpha + beta[j] - A2 * D_beta + delta[j] - A2 * D_delta) / 3, 0, num_cities - 1)

            # repair mechanism to ensure the new wolf remains a valid permutation
            wolves[i] = repair_permutation(wolves[i])

        # if the case, update the best solution
        fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]
        best_wolf_index = np.argmin(fitness_values)
        best_solution = wolves[best_wolf_index]
        if calc_total_dist(best_solution, dist_matrix) < calc_total_dist(best_solution_general, dist_matrix):
            best_solution_general = best_solution.copy()

        iteration_counter += 1

    # return the best solution found and it's fitness
    return [best_solution_general, calc_total_dist(best_solution_general, dist_matrix)]


# Adaptive Grey Wolf Optimization for TSP
def AGWO(dist_matrix, num_wolves, max_iterations):
    num_cities = dist_matrix.shape[0]

    # initialize wolves
    wolves = [np.random.permutation(num_cities) for _ in range(num_wolves)]

    # get the best solution
    fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]
    best_wolf_index = np.argmin(fitness_values)
    best_solution_general = wolves[best_wolf_index]

    break_point = num_cities
    iteration_counter = 0

    while iteration_counter < max_iterations:
        fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]

        # determine alpha, beta and delta wolves
        sorted_indices = np.argsort(fitness_values)
        alpha = wolves[sorted_indices[0]]
        beta = wolves[sorted_indices[1]]
        delta = wolves[sorted_indices[2]]

        # update positions
        for i in range(num_wolves):
            # update position of the wolf based on alpha, beta and delta wolves
            for j in range(num_cities):
                r1, r2 = np.random.rand(2)

                # in [-1, 1]
                A1 = 2 * r1 - 1
                A2 = 2 * r2 - 1

                # in [0,2]
                C1 = 2 * r1
                C2 = 2 * r2

                # distances to alpha, beta and omega wolves
                D_alpha = abs(C1 * alpha[j] - wolves[i][j])
                D_beta = abs(C2 * beta[j] - wolves[i][j])
                D_delta = abs(C2 * delta[j] - wolves[i][j])

                wolves[i][j] = np.clip((alpha[j] - A1 * D_alpha + beta[j] - A2 * D_beta + delta[j] - A2 * D_delta) / 3, 0, num_cities - 1)

            # repair mechanism to ensure the new wolf remains a valid permutation
            wolves[i] = repair_permutation(wolves[i])
            fitness = calc_total_dist(wolves[i], dist_matrix)

            # here comes the adaptive part
            new_wolf = adaptive_crossover(alpha, beta, delta, wolves[i], break_point, dist_matrix)
            new_fitness = calc_total_dist(new_wolf, dist_matrix)
            if new_fitness < fitness:
                wolves[i] = new_wolf.copy()

            new_wolf = neighborhood_search(wolves[i], dist_matrix)
            new_fitness = calc_total_dist(new_wolf, dist_matrix)
            if new_fitness < fitness:
                wolves[i] = new_wolf.copy()

        # compute breakpoint
        if break_point > 0:
            break_point -= 1

        # if the case, update the best solution
        fitness_values = [calc_total_dist(wolf, dist_matrix) for wolf in wolves]
        best_wolf_index = np.argmin(fitness_values)
        best_solution = wolves[best_wolf_index]
        if calc_total_dist(best_solution, dist_matrix) < calc_total_dist(best_solution_general, dist_matrix):
            best_solution_general = best_solution.copy()

        iteration_counter += 1

    # return the best solution found and it's fitness
    return [best_solution_general, calc_total_dist(best_solution_general, dist_matrix)]
