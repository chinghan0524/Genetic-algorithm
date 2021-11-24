from population import Population

def main():
    pop_size = 100
    mutation_rate = 0.01
    max_generation = 100
    graph = {
        1: {3},
        2: {3},
        3: {5},
        4: {1,5},
        5: {},
        6: {7,8},
        7: {},
        8: {5,7} 
    }
    
    pop = Population(graph, pop_size, mutation_rate, max_generation)

    pop.print_population_status()

    while not pop.finished:
        pop.natural_selection()
        pop.generate_new_population()
        pop.evaluate()
        pop.print_population_status()

if __name__ == "__main__":
    main()
