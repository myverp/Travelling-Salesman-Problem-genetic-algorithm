import unittest
import math
from main import (
    initialize_population, 
    calculate_fitness, 
    select_parents, 
    crossover, 
    mutate, 
    create_new_population, 
    is_valid_solution, 
    genetic_algorithm
)

class TestGeneticAlgorithm(unittest.TestCase):
    
    def setUp(self):
        """Створення базових даних для тестів"""
        self.cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        self.pop_size = 10
        self.population = initialize_population(self.pop_size, self.cities)
    
    def test_initialize_population(self):
        """Тест на ініціалізацію популяції з правильним розміром і дійсними особинами"""
        # Перевіряємо розмір популяції
        self.assertEqual(len(self.population), self.pop_size)
        for individual in self.population:
            # Перевіряємо, чи кожен індивідуум є дійсним маршрутом
            self.assertTrue(is_valid_solution(individual, self.cities))

    def test_calculate_fitness(self):
        """Тест на обчислення придатності (довжини маршруту)"""
        individual = self.cities  # Відомий маршрут
        fitness = calculate_fitness(individual)
        # Відстань між кожними двома сусідніми містами
        segment_distance = math.sqrt(2)
        # Повна відстань маршруту (включаючи зворотній шлях)
        expected_fitness = 4 * segment_distance + 4 * segment_distance
        self.assertAlmostEqual(fitness, expected_fitness, places=5)

    def test_select_parents(self):
        """Тест на вибір батьків за методом турніру"""
        fitnesses = [calculate_fitness(ind) for ind in self.population]
        parents = select_parents(self.population, fitnesses)
        # Перевіряємо, що вибрано двох батьків
        self.assertEqual(len(parents), 2)
        # Перевіряємо, що кожен батько є дійсним маршрутом
        for parent in parents:
            self.assertTrue(is_valid_solution(parent, self.cities))

    def test_crossover(self):
        """Тест на операцію кросовера"""
        parent1, parent2 = self.population[0], self.population[1]
        child = crossover(parent1, parent2)
        # Перевіряємо, що дитина є дійсним маршрутом
        self.assertTrue(is_valid_solution(child, self.cities))

    def test_mutate(self):
        """Тест на операцію мутації"""
        individual = self.population[0]
        mutated = mutate(individual)
        # Перевіряємо, що мутація не створює недійсний маршрут
        self.assertTrue(is_valid_solution(mutated, self.cities))

    def test_create_new_population(self):
        """Тест на створення нової популяції"""
        fitnesses = [calculate_fitness(ind) for ind in self.population]
        new_population = create_new_population(self.population, fitnesses)
        # Перевіряємо розмір нової популяції
        self.assertEqual(len(new_population), self.pop_size)
        # Перевіряємо, що кожен індивідуум в новій популяції є дійсним маршрутом
        for individual in new_population:
            self.assertTrue(is_valid_solution(individual, self.cities))
    
    def test_genetic_algorithm(self):
        """Тест на повний генетичний алгоритм"""
        best_solution, best_distance = genetic_algorithm(self.cities, self.pop_size, generations=50, mutation_rate=0.01)
        # Перевіряємо, що знайдено дійсний маршрут
        self.assertTrue(is_valid_solution(best_solution, self.cities))
        # Перевіряємо, що обчислено довжину маршруту
        self.assertTrue(isinstance(best_distance, float))

if __name__ == "__main__":
    unittest.main()
