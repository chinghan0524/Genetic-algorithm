import random
import string


class Individual:
    """
        Individual in the population
    """

    def __init__(self, maxClusterSize):
        self.fitness = 0
        self.genes = self.generate_random_genes(maxClusterSize)

    @staticmethod
    def generate_random_genes(maxClusterSize):
        genes = []

        for i in range(maxClusterSize):
             genes.append(random.randint(1, maxClusterSize))
        #genes = [1, 1, 1, 2, 2, 3, 3, 3]
        
        return genes

    def calc_fitness(self, graph):
        cluster2classMap = {}
        classIndex = 1
        for cluster in self.genes:
            try:
                cluster2classMap[cluster].add(classIndex)
            except KeyError:
                cluster2classMap[cluster] = {classIndex}
            classIndex += 1
        #print(f"cluster2classMap: {cluster2classMap}")

        clusterConnectivity = {}
        for cluster_i in cluster2classMap:
            for cluster_j in cluster2classMap:
                if cluster_i != cluster_j:
                    key = str(cluster_i) + "_" + str(cluster_j)
                    if cluster_i > cluster_j:
                         key = str(cluster_j) + "_" + str(cluster_i)
                    
                    if key in clusterConnectivity:
                        continue
                    else:
                        count = 0
                        for class_i in cluster2classMap[cluster_i]:
                            for class_j in cluster2classMap[cluster_j]:
                                if class_i in graph[class_j]:
                                    count += 1
                                if class_j in graph[class_i]:
                                    count += 1

                        clusterConnectivity[key] = count 
        #print(f"clusterConnectivity: {clusterConnectivity}")

        interConnectivity = {}
        for cluster in cluster2classMap:
            count = 0
            for (class_i, class_j) in ((class_i, class_j) for class_i in cluster2classMap[cluster] for class_j in cluster2classMap[cluster] if class_i != class_j):
                if class_j in graph[class_i]:
                    count += 1

            interConnectivity[cluster] = count
        #print(f"interConnectivity: {interConnectivity}")

        turboMQ = 0
        for (cluster_i, cluster_j) in ((cluster_i, cluster_j) for cluster_i in cluster2classMap for cluster_j in cluster2classMap if cluster_i != cluster_j):
            key = str(cluster_i) + "_" + str(cluster_j)
            if (cluster_i > cluster_j):
                key = str(cluster_j) + "_" + str(cluster_i)

            if (2 * interConnectivity[cluster_i] + clusterConnectivity[key]) != 0:
                turboMQ += (2 * interConnectivity[cluster_i]) / (2 * interConnectivity[cluster_i] + clusterConnectivity[key])
        #print(f"turboMQ: {turboMQ}")

        self.fitness = turboMQ

    def crossover(self, partner):
        # Crossover suggestion: child with half genes from one parent and half from the other parent
        ind_len = len(self.genes)
        child = Individual(ind_len)

        midpoint = random.randint(0, ind_len)

        # crossover
        child.genes = self.genes[:midpoint] + partner.genes[midpoint:]

        return child

    def mutate(self, mutation_rate, maxClusterSize):
        # code to mutate the individual here
        for elem in enumerate(self.genes):
            if random.uniform(0, 1) < mutation_rate:
                self.genes[elem[0]] = random.randint(1, maxClusterSize)