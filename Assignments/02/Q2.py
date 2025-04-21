import random

popsize = 6
gens = 50

tasktimes = [5, 8, 4, 7, 6, 3, 9]
facilitycaps = [24, 30, 28]

costmatrix = [
    [10, 12, 9],
    [15, 14, 16],
    [8, 9, 7],
    [12, 10, 13],
    [14, 13, 12],
    [9, 8, 10],
    [11, 12, 13]
]

numtasks = len(tasktimes)
numfacilities = len(facilitycaps)

initialpopulation = [
    [1, 3, 1, 2, 3, 2, 1],
    [3, 2, 2, 1, 1, 3, 2],
    [3, 3, 2, 2, 1, 1, 3],
    [1, 1, 2, 3, 1, 2, 2],
    [1, 3, 3, 1, 1, 1, 2],
    [2, 2, 3, 2, 1, 1, 3]
]

def fitness(chrom):
    load = [0] * numfacilities
    cost = 0
    for i, fac in enumerate(chrom):
        f = fac - 1
        load[f] += tasktimes[i]
        cost += costmatrix[i][f] * tasktimes[i]
    penalty = sum((load[i] - facilitycaps[i]) * 100 for i in range(numfacilities) if load[i] > facilitycaps[i])
    return -(cost + penalty)

def rouletteselection(pop, fits):
    minfit = min(fits)
    adjusted = [f - minfit + 1 for f in fits]
    total = sum(adjusted)
    r = random.uniform(0, total)
    acc = 0
    for chrom, fit in zip(pop, adjusted):
        acc += fit
        if acc >= r:
            return chrom
    return pop[0]

def onepointcrossover(p1, p2):
    pt = random.randint(1, numtasks - 2)
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]

def mutate(chrom):
    i, j = random.sample(range(numtasks), 2)
    chrom[i], chrom[j] = chrom[j], chrom[i]
    return chrom

def geneticalgorithm():
    pop = initialpopulation[:]
    for g in range(1, gens + 1):
        fits = [fitness(c) for c in pop]
        newgen = []
        while len(newgen) < popsize:
            p1 = rouletteselection(pop, fits)
            p2 = rouletteselection(pop, fits)

            if random.random() < 0.8:
                c1, c2 = onepointcrossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            if random.random() < 0.2:
                mutate(c1)
            if random.random() < 0.2:
                mutate(c2)

            newgen += [c1, c2]

        pop = newgen[:popsize]

        if g % 5 == 0 or g == gens:
            best = max(pop, key=fitness)
            print(f"Gen {g} | Best Cost: {-fitness(best)}")

    best = max(pop, key=fitness)
    return best, -fitness(best)


bestsolution, mincost = geneticalgorithm()
print("\nBest Assignment:", bestsolution)
print("Total Cost:", mincost)
