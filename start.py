from population import Population

def main():
    pop_size = 100
    mutation_rate = 0.01
    max_generation = 100
    graph = {
        0: {2},
        1: {2},
        2: {4},
        3: {0,4},
        4: {},
        5: {6,7},
        6: {},
        7: {4,6} 
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
