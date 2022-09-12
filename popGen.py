from collections import Counter
import numpy as np

class PopGen:

    def __init__(self, N, MALE_PROPORTION):
        self.N = N
        self.MALE_PROPORTION = MALE_PROPORTION

    def getN(self):
        return self.N

    def getMALE_PROPORTION(self):
        return self.MALE_PROPORTION

    def make_couples(self, generation:np.ndarray) -> np.ndarray:
        """Split the generation into male and female segments, form couples
        
        Returns: array of couple, where each couple is represented as the union of their ancestors
        """
        # population size and male_proportion are parameters to allow for more dynamic simulations
        male_proportion = self.getMALE_PROPORTION()
        population_size = len(generation)
        num_males = int(male_proportion * population_size)
        num_females = population_size - num_males
        men = generation[:num_males]
        women = generation[num_males:]
        np.random.shuffle(men)
        np.random.shuffle(women)
        couples = []
        for i in range(min(num_males, num_females)):
            couples.append(men[i].union(women[i]))
        if not num_males == num_females:
            for i in range(abs(num_females - num_males)):
                if num_males < num_females:
                    couples.append(men[i].union(women[i + num_males]))
                else:
                    couples.append(women[i].union(men[i + num_females]))
        return np.array(couples)

    def create_next_generation(self, couples:np.ndarray) -> np.ndarray:
        """Create the next population generation"""
        population_size = self.getN()
        num_couples = len(couples)
        children_index = np.random.randint(0, high=num_couples, size=population_size)
        return np.take(couples, children_index)

    def count_descendants(self, generation:np.ndarray) -> Counter:
        """Return a Counter with info on how many descendants first-gen ancestors have.
        
        Note: Ancestors with no descendants do not have an indexed entry in the Counter
        """
        c = Counter()
        for individual in generation:
            c += Counter(individual)
        return c

    def is_genealogical_ae_present(self, descendant_counts:Counter) -> bool:
        population_size = self.getN()
        if max(descendant_counts.values()) == population_size:
            return True
        else:
            return False

    def run_simulation(self):
        generation = np.array([{i} for i in range(self.N)])
        for i in range(1000):
            couples = self.make_couples(generation)
            next_gen = self.create_next_generation(couples)
            descendants = self.count_descendants(next_gen)
            if self.is_genealogical_ae_present(descendants):
                break
            else:
                generation = next_gen

        start_population:int
        num_generations:int
        num_ancestors_represented:int
        num_ae_couples:int
        distribution_of_couples_descendants:Counter

        start_population = self.getN()
        num_generations = i + 1 # Python iteration starts at zero, but we start at 1
        num_ancestors_represented = len(descendants)
        d = Counter(descendants.values())
        c = Counter()
        for k in d:
            c[k] = int(d[k]/2)
        distribution_of_couples_descendants = c
        num_ae_couples = distribution_of_couples_descendants[self.getN()]

        almost_ae = 0
        for k in distribution_of_couples_descendants:
            if k >= self.getN() * 0.9:
                almost_ae += distribution_of_couples_descendants[k]

        return ("{\"pop\": \"" + str(start_population) + "\", \"num_gens\": \"" + str(num_generations) + 
            "\", \"num_anc_rep\": \"" + str(num_ancestors_represented) + "\", \"num_ae_couples\": \"" + str(num_ae_couples) +
            "\", \"almost_ae\": \"" + str(almost_ae) + "\"}")

