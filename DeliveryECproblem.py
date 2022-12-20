import random
from random import choices

from matplotlib import pyplot as plt


class DeliveryProblem:
    def __init__(self, number_objects, boxes, quota, capacity):
        self.population_size = number_objects * 10
        self.boxes = boxes
        self.quota = quota
        self.capacity = capacity
        self.MUTATION_RATE = 0.1
        self.GENERATION_LIMIT = 200

    def generate_chromosome(self):
        return random.choices((0, 1), k=len(self.boxes))

    def generate_population(self):
        return (self.generate_chromosome() for _ in range(self.population_size))

    def fitness_score(self, chromosome):
        capacity = 0
        quota = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                capacity += int(self.boxes[i][1])
                quota += int(self.boxes[i][2])
                if capacity > self.capacity:
                    return 0
        if quota < self.quota:
            return 0
        return quota

    def selection(self, population):
        return choices(population=population, weights=[self.fitness_score(chromosome) for chromosome in population],
                       k=2)

    def crossover(self, chromosome1, chromosome2):
        if len(self.boxes) < 2:
            return chromosome1, chromosome2
        crossPoint = random.randint(1, len(self.boxes) - 1)
        return chromosome1[0:crossPoint] + chromosome2[crossPoint:], chromosome2[0:crossPoint] + chromosome1[
                                                                                                 crossPoint:]

    def mutation(self, chromosome):
        for row in range(len(chromosome)):
            if random.random() < self.MUTATION_RATE:
                chromosome[row] = random.randrange(0, 2)
        return chromosome

    def run_evolution(self, population):
        most_fit = [0, 0, 0]
        gen_no = 0
        cont_gen = 1
        fitness = []
        num_gen =[]
        terminate = 0
        while terminate < 50 and cont_gen < self.GENERATION_LIMIT:
            population = sorted(population, key=lambda chromosome: self.fitness_score(chromosome), reverse=True)
            if self.fitness_score(population[0]) > self.fitness_score(most_fit):
                most_fit = population[0]
                gen_no = cont_gen
                terminate = 0
            else:
                terminate += 1
            next_gen = population[:2]
            for i in range(int(len(population) / 2 - 1)):
                parents = self.selection(population)
                offspring1, offspring2 = self.crossover(list(parents[0]), list(parents[1]))
                offspring1 = self.mutation(offspring1)
                offspring2 = self.mutation(offspring2)
                next_gen += [offspring1, offspring2]
            population = next_gen
            cont_gen += 1
            fitness.append(self.fitness_score(population[0]))
            num_gen.append(gen_no)
        fig, ax1 = plt.subplots()
        print(fitness)
        print(num_gen)
        line1 = ax1.plot(num_gen, fitness, "b-", label="Fitness")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness")
        plt.xlim(0, 50)
        plt.show()
        return [most_fit, gen_no]

