import random
import time
import numpy as np
import subprocess
import json

class Cube:

  stdfactor = 1

  def __init__(self, dimension):
    self.dimension = dimension
    self.cube = [[[0 for k in range(dimension)] for j in range(dimension)] for i in range(dimension)]

  def __str__(self):
    string = ""
    for i in range(self.dimension):
      for j in range(self.dimension):
        for k in range(self.dimension):
          string += f"[{i}][{j}][{k}] = {self.cube[i][j][k]}\n"
    return string
  
  def initialize(self):
    numbers = list(range(1, self.dimension**3+1))
    for i in range(self.dimension**3):
      index = random.randint(0, self.dimension**3 - 1 - i)
      self.cube[i // (self.dimension**2)][(i % (self.dimension**2)) // self.dimension][i % self.dimension] = numbers[index]
      numbers[index], numbers[self.dimension**3 - 1 - i] = numbers[self.dimension**3 - 1 - i], numbers[index]

  def copyCube(other) :
    new_cube = Cube(other.dimension)

    for z in range(other.dimension) :
      for y in range(other.dimension) :
        for x in range(other.dimension) :
          new_cube.cube[z][y][x] = other.cube[z][y][x]

    return new_cube
  
  def rowSums(self):
    results = []
    for z in range(self.dimension) :
      for y in range(self.dimension) :
        sum = 0
        for x in range(self.dimension) :
          sum += self.cube[z][y][x]
        results.append(sum)
    return results
  
  def columnSums(self):
    results = []
    for z in range(self.dimension) :
      for x in range(self.dimension) :
        sum = 0
        for y in range(self.dimension) :
          sum += self.cube[z][y][x]
        results.append(sum)
    return results
  
  def pillarSums(self):
    results = []
    for y in range(self.dimension) :
      for x in range(self.dimension) :
        sum = 0
        for z in range(self.dimension) :
          sum += self.cube[z][y][x]
        results.append(sum)
    return results
  
  def spatialDiagonalSums(self):
    diagonal_sums = [0, 0, 0, 0]
    for i in range(self.dimension):
      diagonal_sums[0] += self.cube[i][i][i]
      diagonal_sums[1] += self.cube[i][self.dimension - 1 - i][i]
      diagonal_sums[2] += self.cube[i][i][self.dimension-1 - i]
      diagonal_sums[3] += self.cube[i][self.dimension-1 - i][self.dimension-1 - i]
    return diagonal_sums
  
  def xyIntersectionDiagonalSums(self):
    diagonal_sums = []
    for z in range(self.dimension) :
      diagon1 = 0
      diagon2 = 0
      for i in range(self.dimension) :
        diagon1 += self.cube[z][i][i]
        diagon2 += self.cube[z][i][self.dimension-1-i]
      diagonal_sums.append(diagon1)
      diagonal_sums.append(diagon2)
    return diagonal_sums
  
  def xzIntersectionDiagonalSums(self):
    diagonal_sums = []
    for y in range(self.dimension) :
      diagon1 = 0
      diagon2 = 0
      for i in range(self.dimension) :
        diagon1 += self.cube[i][y][i]
        diagon2 += self.cube[i][y][self.dimension-1-i]
      diagonal_sums.append(diagon1)
      diagonal_sums.append(diagon2)
    return diagonal_sums
  
  def yzIntersectionDiagonalSums(self):
    diagonal_sums = []
    for x in range(self.dimension) :
      diagon1 = 0
      diagon2 = 0
      for i in range(self.dimension) :
        diagon1 += self.cube[i][i][x]
        diagon2 += self.cube[i][self.dimension-1-i][x]
      diagonal_sums.append(diagon1)
      diagonal_sums.append(diagon2)
    return diagonal_sums
  
  def allSums(self) :
    sums = []
    sums += self.rowSums()
    sums += self.columnSums()
    sums += self.pillarSums()
    sums += self.spatialDiagonalSums()
    sums += self.xyIntersectionDiagonalSums()
    sums += self.xzIntersectionDiagonalSums()
    sums += self.yzIntersectionDiagonalSums()
    return sums
  
  def allCoordinatePairs(dimension) :
    coordinate_pairs = []
    coordinates = [(i, j, k) for i in range(dimension) for j in range(dimension) for k in range(dimension)]

    for i, coordinate1 in enumerate(coordinates):
      for coordinate2 in coordinates[i+1:]:
        coordinate_pairs.append((coordinate1, coordinate2))
    random.shuffle(coordinate_pairs)

    return coordinate_pairs
  
  def getH(self) :
    sums = np.array(self.allSums())
    target = self.dimension * (self.dimension**3 + 1) / 2
    stddev = np.std(sums)
    n = 0
    for sum in sums :
      if (sum == target) :
        n += 1
    return n - stddev*Cube.stdfactor
  
  def controlH(self) :
    sums = self.allSums()
    target = self.dimension * (self.dimension**3 + 1) / 2
    n = 0
    e = 0
    for sum in sums :
      if (sum == target) :
        n += 1
      e += abs(target - sum)
    e /= 32700
    return n + e


class GeneticCube:

  def  __init__(self, dimension, popSize = 8) :
    self.dimension = dimension
    self.popSize = popSize
    self.population = [Cube(dimension) for i in range(popSize)]

  def initPopulation(self) :
    for cube in self.population :
      cube.initialize()

  def getFitnesses(self) :
    fitnesses = []
    for cube in self.population :
      fitnesses.append(cube.controlH())
    return fitnesses

  def getBucketsFromFitnesses(self, fitnesses) :
    sum = 0
    for fitness in fitnesses :
      sum += fitness
    
    buckets = []
    progress = 0
    for fitness in fitnesses :
      progress += fitness/sum
      buckets.append(progress)
    return buckets

  def generateRandom(self, buckets) :
    roll = random.random()
    for i in range(self.popSize) :
      if roll < buckets[i] :
        return i
      
  def combine(self, cube1, cube2) :
    child1 = Cube(self.dimension)
    child2 = Cube(self.dimension)

    posCounts = self.dimension**3
    for i in range(posCounts) :
      z = i // (self.dimension**2)
      y = (i % (self.dimension**2)) // self.dimension
      x = i % self.dimension
      
      if (i < 2*posCounts//self.dimension) :
        child1.cube[x][y][z] = cube1.cube[x][y][z]
        child2.cube[x][y][z] = cube2.cube[x][y][z]
      else :
        child1.cube[x][y][z] = cube2.cube[x][y][z]
        child2.cube[x][y][z] = cube1.cube[x][y][z]

    return (child1, child2)
  
  def mutate(self, cube: Cube) :
      mutated = {}
      counts = dict()

      for i in range(1, self.dimension**3 + 1) :
          counts[i] = 0

      for z in range(5) :
          for y in range(5) :
              for x in range(5) :
                  counts[cube.cube[x][y][z]] += 1

      unplacedNumbers = [key for key, value in counts.items() if value == 0]

      for z in range(5) :
        for y in range(5) :
          for x in range(5) :
            number = cube.cube[x][y][z]
            if (counts[number] > 1) :
              cube.cube[x][y][z] = unplacedNumbers.pop()
              mutated[f"{x} {y} {z}"] = cube.cube[x][y][z]
              counts[number] -= 1
      return mutated
  
  def pop_max(self):
    return max(self.population, key=lambda x: x.getH())
  
  def avg_by_getH(self):
    return sum(x.getH() for x in self.population) / len(self.population)

  def geneticAlgorithm(self, iterationCount = 1000) :
    self.initPopulation()
    results = {}
    results["max_h"] = []
    results["avg_h"] = []
    results["max_cubes"] = [] 

    for i in range(iterationCount) :
      fitnesses = self.getFitnesses()
      buckets = self.getBucketsFromFitnesses(fitnesses)

      parents = []
      parents_idx = []
      for j in range(self.popSize) :
        randomIdx = self.generateRandom(buckets)
        parents_idx.append(randomIdx)
        parents.append(self.population[randomIdx])
      
      mutations = []
      for j in range(self.popSize//2) :
        self.population[2*j], self.population[2*j + 1] = self.combine(parents[2*j], parents[2*j + 1])
        mutations.append(self.mutate(self.population[2*j]))
        mutations.append(self.mutate(self.population[2*j + 1]))

    best_cube = max(self.population, key=lambda cube: cube.getH())
    results["final_state"] = best_cube.cube
    results["final H"] = best_cube.getH()
    results["control H"] = best_cube.controlH()
    return results
  
def run_algorithm(algorithm, argv=None):
  argv = argv or {}
  
  command = ["./Cube.exe", algorithm]

  for key, value in argv.items():
      command.extend([f"--{key}", str(value)])

  if (algorithm in ["steepest ascent", "sideways ascent", "random restart", "stochastic", "simulated annealing"]) :
    try:
        result_json = subprocess.check_output(command, text=True)
        result = json.loads(result_json)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
        result = {"error": str(e)}

    except json.JSONDecodeError:
        print("Failed to parse JSON output from the binary.")
        result = {"error": "Invalid JSON output"}
  elif algorithm == "genetic algorithm" :
    start_time = time.time()
    geneticAgent = GeneticCube(5, argv.get("popSize") or 8)
    result = geneticAgent.geneticAlgorithm(argv.get("max_iteration") or 1000)
    result["duration"] = time.time() - start_time
  else :
    result = "What are you doing man!"
  return result