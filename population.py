from individual import Individual
import random


class Population:
    """
        A class that describes a population of virtual individuals
    """

    def __init__(self, graph, pop_size, mutation_rate, max_generation):
        self.population = []
        self.generations = 0
        self.graph = graph
        self.mutation_rate = mutation_rate
        self.best_ind = None
        self.finished = False
        self.best_fitness = 0.0
        self.average_fitness = 0.0
        self.mating_pool = []
        self.max_generation = max_generation

        # generate Individual
        for i in range(pop_size): 
            ind = Individual(len(graph))
            ind.calc_fitness(graph)

            if ind.fitness > self.best_fitness:
                self.best_fitness = ind.fitness
                self.best_ind = ind

            self.average_fitness += ind.fitness
            self.population.append(ind)

        self.average_fitness /= pop_size

    def print_population_status(self):
        print("\nGeneration " + str(self.generations))
        print("Average fitness: " + str(self.average_fitness))
        print(f"Best fitness: {self.best_fitness}"  )
        print(f"Best individual: {self.best_ind.genes}"  )
        

    def natural_selection(self):
        # Implementation suggestion based on Lab 3:
        # Based on fitness, each member will get added to the mating pool a certain number of times
        # a higher fitness = more entries to mating pool = more likely to be picked as a parent
        # a lower fitness = fewer entries to mating pool = less likely to be picked as a parent
        self.mating_pool = []

        # create the pool with all the individuals according to their probability (fitness)
        for index, ind in enumerate(self.population):
            prob = int(round(ind.fitness * 100))
            self.mating_pool.extend([index for i in range(prob)])

    def generate_new_population(self):
        population_len = len(self.population)
        mating_pool_len = len(self.mating_pool)

        new_population = []
        self.average_fitness = 0.0

        for i in range(population_len):
            i_partner_a = random.randint(0, mating_pool_len - 1)
            i_partner_b = random.randint(0, mating_pool_len - 1)

            i_partner_a = self.mating_pool[i_partner_a]
            i_partner_b = self.mating_pool[i_partner_b]

            partner_a = self.population[i_partner_a]
            partner_b = self.population[i_partner_b]

            child = partner_a.crossover(partner_b)
            child.mutate(self.mutation_rate, len(self.graph))
            child.calc_fitness(self.graph)

            self.average_fitness += child.fitness
            new_population.append(child)

        self.population = new_population
        self.generations += 1
        self.average_fitness /= len(new_population)


    def evaluate(self):
        for ind in self.population:
            if ind.fitness > self.best_fitness:
                self.best_fitness = ind.fitness
                self.best_ind = ind

        if self.max_generation <= self.generations:
            self.finished = True