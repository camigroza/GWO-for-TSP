import statistics
import time
from Grey_Wolf_Optimization import *


def main():
    nume_fisier = input("Dati numele fisierului de configurare: ")

    x_coord = []
    y_coord = []

    with open(nume_fisier, 'r') as fisier:
        for linie in fisier:
            linie = linie.strip().split()
            x_coord.append(int(linie[1]))
            y_coord.append(int(linie[2]))

    dist_matrix = make_dist_matrix(x_coord, y_coord)

    num_wolves = int(input("Dati numarul de lupi din haita: "))
    max_iterations = int(input("Dati numarul maxim de iteratii: "))

    with open("results_GWO.txt", 'a') as fisier:
        fisier.write("Grey Wolf Optimization -> " + nume_fisier +
                     " -> wolves = " + str(num_wolves) + " -> iterations = " + str(max_iterations) + " -> 10 rulari\n\n")

    # with open("results_AGWO.txt", 'a') as fisier:
    #     fisier.write("Adaptive Grey Wolf Optimization -> " + nume_fisier +
    #                  " -> wolves = " + str(num_wolves) + " -> iterations = " + str(max_iterations) + " -> 10 rulari\n\n")

    all_values = []
    all_times = []

    for i in range(10):
        timp_inceput = time.time()
        rezultat = GWO(dist_matrix, num_wolves, max_iterations)
        # rezultat = AGWO(dist_matrix, num_wolves, max_iterations)
        timp_sfarsit = time.time()

        best_value = rezultat[1]

        all_times.append(timp_sfarsit - timp_inceput)
        all_values.append(best_value)

        with open("results_GWO.txt", 'a') as fisier:
            fisier.write(str(best_value) + " " + str(timp_sfarsit - timp_inceput) + "\n")

        # with open("results_AGWO.txt", 'a') as fisier:
        #     fisier.write(str(best_value) + " " + str(timp_sfarsit - timp_inceput) + "\n")

    with open("results_GWO.txt", 'a') as fisier:
        fisier.write("\n")
        fisier.write(
            "Calitatea solutiei: avg = " + str(statistics.mean(all_values)) + "; best = " + str(min(all_values)))
        fisier.write("\nTimpul mediu de executie: " + str(statistics.mean(all_times)))
        fisier.write("\n\n----------------------------------------------------------------------------------\n\n")

    # with open("results_AGWO.txt", 'a') as fisier:
    #     fisier.write("\n")
    #     fisier.write(
    #         "Calitatea solutiei: avg = " + str(statistics.mean(all_values)) + "; best = " + str(min(all_values)))
    #     fisier.write("\nTimpul mediu de executie: " + str(statistics.mean(all_times)))
    #     fisier.write("\n\n----------------------------------------------------------------------------------\n\n")


if __name__ == '__main__':
    main()
