import numpy
import random



class Chromosone:

    def __init__(self, length, order = None):
        self.length = length
        if order is not None:
            self.genes = order
        else:
            self.genes = (2.4 * numpy.random.rand(length) - 1.2).tolist()


    def Mutation(self):

        mutated_gene_index = random.randint(0, self.length-1)
        self.genes[mutated_gene_index] += numpy.random.normal(scale=0.2)
    def BirthMutation(self, chance):

        if random.choices([True, False], [chance, 1-chance]):
            self.Mutation()

class Population:

    def __init__(self, size, chromosome_length):

        self.chromosomes = [Chromosone(chromosome_length) for i in range(size)]
        self.chromosomes_length = chromosome_length
        self.size = size

    def nextGenByRoulettWheel(self, fitness_scores):
        if fitness_scores is None:
            parent1 = random.choices(self.chromosomes,  k=1)[0]
            parent2 = random.choices(self.chromosomes,  k=1)[0]

        parent1 = random.choices(self.chromosomes, fitness_scores, k=1)[0]
        parent2 = random.choices(self.chromosomes, fitness_scores, k=1)[0]

        if parent2 == parent1:
            new_pop = [parent1]
        else:
            new_pop = [parent1, parent2]





        while len(new_pop) < self.size:
            off_springs = MergeChromosomes(parent1, parent2)
            off_springs[0].BirthMutation(0.1)
            off_springs[1].BirthMutation(0.1)
            new_pop.append(off_springs[0])
            new_pop.append(off_springs[1])

        if len(new_pop) > self.size:
            new_pop.pop(-1)
        self.chromosomes = new_pop
    def nextGenByBest(self, fitness):

        parents = TwoLargestElementIndexes(fitness)

        parent1 = self.chromosomes[parents[0]]

        parent2 = self.chromosomes[parents[1]]

        if parent2 == parent1:
            new_pop = [parent1]
        else:
            new_pop = [parent1, parent2]

        while len(new_pop) < self.size:
            off_springs = MergeChromosomes(parent1, parent2)
            off_springs[0].BirthMutation(0.10)
            off_springs[1].BirthMutation(0.10)
            new_pop.append(off_springs[0])
            new_pop.append(off_springs[1])

        if len(new_pop) > self.size:
            new_pop.pop(-1)
        self.chromosomes = new_pop
    def nextGenByMutation(self, fitness):

        a = TwoLargestElementIndexes(fitness)


        new_pop = [self.chromosomes[a[0]]]

        for i in range(self.size-1):
            new_crom = Chromosone(self.chromosomes_length, self.chromosomes[a[0]].genes)
            new_crom.Mutation()
            new_pop.append(new_crom)
        self.chromosomes = new_pop






def TwoLargestElementIndexes(lst):
    l1 = 0
    l2 = 0

    for i, val  in enumerate(lst):
        if val > lst[l1]:
            l2 = l1
            l1 = i
        elif val > lst[l2]:
            l2 = i
    return [l1, l2]








def MergeChromosomes(chromosome1, chromosome2):

    cross_point = random.randint(0, chromosome1.length-1)

    return [Chromosone(chromosome1.length, order =  chromosome1.genes[:cross_point] + chromosome2.genes[cross_point:]),
        Chromosone(chromosome1.length, order = chromosome2.genes[:cross_point] + chromosome1.genes[cross_point:])]