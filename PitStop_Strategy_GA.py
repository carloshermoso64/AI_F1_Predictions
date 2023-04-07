import random

def fitness(chromosome, num_laps, lap_time, avg_loss_time, pitstop_time):
    # Count number of pitstops
    num_pitstops = sum(chromosome)
    # If there is no pitstop, make a penalty in time
    time = 0
    accumulate_lap_time = lap_time
    if num_pitstops == 0:
        time = 1000

    # Calculate total race time
    lap_times = []
    for i in range(num_laps):
        if chromosome[i] == 1:
            accumulate_lap_time = accumulate_lap_time + pitstop_time
            time += accumulate_lap_time
            lap_times.append(time)
            accumulate_lap_time=lap_time
        else:
            accumulate_lap_time = accumulate_lap_time + avg_loss_time
            time += accumulate_lap_time
            lap_times.append(time)
    race_time = -1 * lap_times[-1]
    # Return fitness as total race time
    return race_time


def iter_mylist(lista):
    for individual in range(len(lista)):
        father1 = lista[random.randint(0, len(lista) - 1)]
        father2 = lista[random.randint(0, len(lista) - 1)]
        father = list(sorted([father1, father2]))[-1][1]  # the best of 2
        mother1 = lista[random.randint(0, len(lista) - 1)]
        mother2 = lista[random.randint(0, len(lista) - 1)]
        mother = list(sorted([mother1, mother2]))[-1][1]  # the best of 2
        yield (father, mother)


def mutation(chromosome, prob):
    mutated = list(chromosome)
    if random.random() > prob:
        index = random.randint(0, len(chromosome) - 1)
        mutated[index] = random.randint(0, 1)
    return mutated


def crossover(parents, prob):
    father, mother = parents
    child = father
    if random.random() > prob:
        index1 = random.randint(1, len(father) - 2)
        index2 = random.randint(1, len(father) - 2)
        if index1 > index2:
            index1, index2 = index2, index1
        child = father[:index1] + mother[index1:index2] + father[index2:]
    return child


def nextgen(fits, pa, pb):
    newpopulation = []
    for parents in iter_mylist(fits):
        child = crossover(parents, pa)
        child = mutation(child, pb)
        newpopulation.append(child)
    return newpopulation


num_laps = 65
lap_time = 80 # seconds
avg_loss_time = 0.3 # seconds
avg_pitstop_time = 40 # seconds

limit = 2000
population_size = 100
prob_crossover = 0.5
prob_mutation = 0.2

counter = 0
actual_best = -1000000
population = [[random.randint(0, 1)
               for i in range(num_laps)]
              for j in range(population_size)]

while counter < limit:
    evaluation = [(fitness(chro, num_laps, lap_time, avg_loss_time, avg_pitstop_time), chro)
                  for chro in population]
    population = nextgen(evaluation, prob_crossover, prob_mutation)
    counter += 1

    solution = list(sorted(evaluation))[-1][1]
    best = list(sorted(evaluation))[-1][0]
    num_pitstops = sum(solution)
    if best > actual_best:
#       print('Total race time="{0}" number of pit stops:"{1}" iteration={2} '.format(best, num_pitstops, counter))
        actual_best = best

solution = list(sorted(evaluation))[-1][1]
best = list(sorted(evaluation))[-1][0]

pit_stops = []
for i, element in enumerate(solution):
    if element == 1:
        pit_stops.append(str(i))

if len(pit_stops) == 0:
    print("There were no pit stops")
else:
    sentence = "Pit stops in laps " + ", ".join(pit_stops)
    print(sentence)

#print('Final="{0}" valor"{1}" '.format(solution, best))



