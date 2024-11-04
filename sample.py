import random
import time
import math
import json

class Cube:
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
  
  def findSteepestAscent(self) :
    dummy_cube = Cube.copyCube(self)

    coordinatePairs = Cube.allCoordinatePairs(self.dimension)

    maxCoordPairs = None
    maxH = -1
    for coord1, coord2 in coordinatePairs :
      x1, y1, z1 = coord1
      x2, y2, z2 = coord2
      dummy_cube.cube[z1][y1][x1], dummy_cube.cube[z2][y2][x2] = dummy_cube.cube[z2][y2][x2], dummy_cube.cube[z1][y1][x1]

      currentH = dummy_cube.getH()

      if currentH > maxH :
        maxH = currentH
        maxCoordPairs = (coord1, coord2)

      dummy_cube.cube[z1][y1][x1], dummy_cube.cube[z2][y2][x2] = dummy_cube.cube[z2][y2][x2], dummy_cube.cube[z1][y1][x1]

    return (maxCoordPairs, maxH)
  
  def steepestAscentHillClimb(self) :
    self.initialize()
    result = {}
    result["initial_state"] = self.copyCube().cube
    result["switches"] = []
    result["h_values"] = []

    done = False
    while not done :
      currentH = self.getH()
      result["h_values"].append(currentH)
      pair, newH = self.findSteepestAscent()
    
      if (newH > currentH) :
        coord1, coord2 = pair
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
        self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]

        result["switches"] += [pair]
      else :
        done = True

    result["h_values"].append(self.getH())
    return result

  def sidewayAscentHillClimb(self, limit = 100) :
    self.initialize()
    result = {}
    result["initial_state"] = self.copyCube().cube
    result["switches"] = []
    result["h_values"] = []
    done = False
    currentStreak = 0
    while not done :
      currentH = self.getH()
      result["h_values"].append(currentH)
      pair, newH = self.findSteepestAscent()
    
      if (newH > currentH or (newH == currentH and currentStreak < limit)) :
        coord1, coord2 = pair
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
        self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]

        result["switches"] += [pair]

        if (newH > currentH) :
          currentStreak = 0
        else :
          currentStreak += 1
      else :
        done = True

    result["h_values"].append(self.getH())
    return result

  def randomRestartHillClimb(self, max_restart = 10) :
    result = {}
    iteration = 1
    result["iteration_per_restarts"] = []

    maxH = 0
    while self.getH() != 109 and iteration < max_restart :
      currResult = self.steepestAscentHillClimb()
      result["iteration_per_restarts"].append(len(currResult["h_values"]))
      if (self.getH() > maxH) :
        result = currResult
        maxH = self.getH()
      iteration += 1

    result["restart_counts"] = iteration
    return result

  def stochasticHillClimb(self) :
    self.initialize()
    result = {}
    result["initial_state"] = self.copyCube().cube
    result["switches"] = []
    result["h_values"] = []

    nmax = 100000

    for i in range(nmax) :
      
      x1, y1, z1, x2, y2, z2 = 0, 0, 0, 0, 0, 0
      while(x1 == x2 and y1 == y2 and z1 == z2) :
        x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

      currentH = self.getH()
      self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]

      newH = self.getH()

      if (currentH >= newH) :
        self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]
      else :
        result["switches"] += [((x1, y1, z1), (x2, y2, z2))]
    
    return result
  
  def getTemperature(self, iteration) :
    return 400*pow(iteration, -0.5) - 1
  
  def getProbability(self, deltaE, temp) :
    return math.exp(deltaE/temp)

  def simulatedAnnealing(self) :
    self.initialize()
    result = {}
    result["initial_state"] = self.copyCube().cube
    result["switches"] = []
    result["boltzmanns"] = []
    result["stucks"] = 0

    iteration = 1
    temperature = self.getTemperature(iteration)

    while temperature > 0 :
      
      x1, y1, z1, x2, y2, z2 = 0, 0, 0, 0, 0, 0
      while(x1 == x2 and y1 == y2 and z1 == z2) :
        x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

      currentH = self.getH()
      self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]

      newH = self.getH()

      if (newH >= currentH) :
        result["boltzmanns"].append(1)
      else :
        roll = random.random()
        probability = self.getProbability(newH - currentH, temperature)
        result["boltzmanns"].append(probability)
        result["stucks"] += 1

        if (roll > probability) :
          self.cube[z1][y1][x1], self.cube[z2][y2][x2] = self.cube[z2][y2][x2], self.cube[z1][y1][x1]
        else :
          result["switches"] += [((x1, y1, z1), (x2, y2, z2))]

      iteration += 1
      temperature = self.getTemperature(iteration)
    
    return result


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
      fitnesses.append(cube.getH())
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

  def geneticAlgorithm(self, iterationCount = 1000) :
    self.initPopulation()
    results = {}
    results["populations"] = []
    results["selected_parent"] = []
    results["mutations"] = []

    for i in range(iterationCount) :
      results["populations"].append(list(map(lambda x: x.cube, self.population)))
      fitnesses = self.getFitnesses()
      buckets = self.getBucketsFromFitnesses(fitnesses)

      parents = []
      parents_idx = []
      for j in range(self.popSize) :
        randomIdx = self.generateRandom(buckets)
        parents_idx.append(randomIdx)
        parents.append(self.population[randomIdx])
      results["selected_parent"].append(parents_idx)
      
      mutations = []
      for j in range(self.popSize//2) :
        self.population[2*j], self.population[2*j + 1] = self.combine(parents[2*j], parents[2*j + 1])
        mutations.append(self.mutate(self.population[2*j]))
        mutations.append(self.mutate(self.population[2*j + 1]))
      results["mutations"].append(mutations)

    best_cube = max(self.population, key=lambda cube: cube.getH())
    results["final_state"] = best_cube.cube
    results["final H"] = best_cube.getH()
    return results
  
def run_algorithm(algorithm, argv) :
  cube = Cube(5)
  
  start_time = time.time()
  if (algorithm == "steepest ascent") :
    result = cube.steepestAscentHillClimb()
    result["duration"] = time.time() - start_time
    result["final H"] = cube.getH()
    result["final_state"] = cube.cube
  elif (algorithm == "sideways ascent") :
    result = cube.sidewayAscentHillClimb(argv['limit'] or 100)
    result["duration"] = time.time() - start_time
    result["final H"] = cube.getH()
    result["final_state"] = cube.cube
  elif (algorithm == "random restart") :
    result = cube.randomRestartHillClimb(argv["max_restart"] or 10)
    result["duration"] = time.time() - start_time
    result["final H"] = cube.getH()
  elif (algorithm == "stochastic") :
    result = cube.stochasticHillClimb()
    result["duration"] = time.time() - start_time
    result["final H"] = cube.getH()
  elif (algorithm == "simulated annealing") :
    result = cube.simulatedAnnealing()
    result["duration"] = time.time() - start_time
    result["final H"] = cube.getH()
  elif (algorithm == "genetic algorithm") :
    geneticAgent = GeneticCube(5, argv["popSize"] or 8)
    result = geneticAgent.geneticAlgorithm(argv["max_iteration"] or 1000)
    result["duration"] = time.time() - start_time
  return result

result = run_algorithm("genetic algorithm")

text_file = open("output.txt", "w")
text_file.write(json.dumps(result))
text_file.close()