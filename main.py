import random
import math
import numpy as np
import matplotlib.pyplot as plt
from database import insert_result

# Ініціалізація популяції
def initialize_population(pop_size, cities):
    population = []
    for _ in range(pop_size):
        individual = random.sample(cities, len(cities))
        population.append(individual)
    return population

# Оцінка придатності (функція обчислення відстані)
def calculate_fitness(individual):
    distance = 0
    for i in range(len(individual) - 1):
        distance += math.sqrt((individual[i][0] - individual[i + 1][0]) ** 2 + (individual[i][1] - individual[i + 1][1]) ** 2)
    distance += math.sqrt((individual[-1][0] - individual[0][0]) ** 2 + (individual[-1][1] - individual[0][1]) ** 2)
    return distance

# Вибір батьків (метод турніру)
def select_parents(population, fitnesses, k=3):
    selected = []
    for _ in range(2):
        tournament = random.sample(list(zip(population, fitnesses)), k)
        winner = min(tournament, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

# Кросовер
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]
    pointer = 0
    for i in range(size):
        if child[i] is None:
            while parent2[pointer] in child:
                pointer += 1
            child[i] = parent2[pointer]
    return child

# Мутація (swap mutation)
def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

# Створення нової популяції
def create_new_population(population, fitnesses, mutation_rate=0.01):
    new_population = []
    for _ in range(len(population) // 2):
        parent1, parent2 = select_parents(population, fitnesses)
        child1 = mutate(crossover(parent1, parent2), mutation_rate)
        child2 = mutate(crossover(parent2, parent1), mutation_rate)
        new_population.extend([child1, child2])
    return new_population

# Перевірка дійсності розв'язку
def is_valid_solution(solution, cities):
    return len(solution) == len(cities) and len(set(solution)) == len(cities)

# Основна функція генетичного алгоритму
def genetic_algorithm(cities, pop_size, generations, mutation_rate=0.01, max_no_improvement=100):
    population = initialize_population(pop_size, cities)
    best_distance = float('inf')
    best_solution = None
    no_improvement_count = 0

    for generation in range(generations):
        fitnesses = [calculate_fitness(individual) for individual in population]
        min_distance = min(fitnesses)
        if min_distance < best_distance:
            best_distance = min_distance
            best_solution = population[fitnesses.index(min_distance)]
            no_improvement_count = 0
        else:
            no_improvement_count += 1
        
        print(f"Generation {generation}: Best Distance = {best_distance}")
        
        if no_improvement_count >= max_no_improvement:
            print("No improvement for 100 generations, stopping early.")
            break

        population = create_new_population(population, fitnesses, mutation_rate)
        # Валідація найкращого рішення
        assert is_valid_solution(best_solution, cities), "Invalid solution found!"
    
    return best_solution, best_distance

# Візуалізація результату
def visualize_route(solution):
    x = [city[0] for city in solution]
    y = [city[1] for city in solution]
    plt.plot(x + [x[0]], y + [y[0]], 'o-')
    plt.show()

if __name__ == "__main__":
    cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(20)]
    pop_size = 1000
    generations = 300
    mutation_rate = 0.01

    best_solution, best_distance = genetic_algorithm(cities, pop_size, generations, mutation_rate)
    insert_result(best_solution, best_distance)
    print(f"Best Distance Found: {best_distance}")
    visualize_route(best_solution)
