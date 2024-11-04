from algorithm import *

def genericPrinter(output):
   print("\n========================== OUTPUT RESULTS ==========================")
   print("Final H: ", output['final H'])
   print("Duration: ", output['duration'])


isFile = input("Do you want to input your own file? TODO (y/n) => ")
print("========================== Choose your algorithm ==========================")
print("1. Steepest Ascent Hill Climb")
print("2. Hill Climb with Sideways Move")
print("3. Random Restart Hill Climb")
print("4. Stochastic Hill Climbing")
print("5. Simulated Annealing")
print("6. Genetic Algorithm")
alg = int(input("=> "))

while True:
    if(alg == 1 or alg == 4 or alg == 5):
        output = None
        if(alg==1):
         output = run_algorithm("steepest ascent")
         genericPrinter(output)
        elif(alg==4):
         output = run_algorithm("stochastic")
         genericPrinter(output)
        elif(alg==5):
         output = run_algorithm("simulated annealing")
         genericPrinter(output)
         print("Stucks: ", output['stucks'])
    elif(alg == 2):
        max_limit = int(input("Max Limit => "))
        output = run_algorithm("sideways ascent",{"max_limit": max_limit})
        genericPrinter(output)
    elif(alg== 3):
        max_restart = int(input("Max Restart => "))
        output = run_algorithm("random restart",{"max_restart": max_restart})
        genericPrinter(output)
        print("Iteration per Restarts: ", output['iteration_per_restarts'])
        print("Restart Counts: ", output['restart_counts'])
    elif(alg==6):
        population_size = int(input("Population Size => "))
        iteration_max = int(input("Maximum Iteration => "))
        output = run_algorithm("genetic algorithm",{"popSize": population_size, "max_iteration": iteration_max})
        genericPrinter(output)
    else:
        print("Invalid input, Exiting Program..")
        break
    print("\n\n========================== Choose your algorithm ==========================")
    print("Choose your algorithm:")
    print("1. Steepest Ascent Hill Climb")
    print("2. Hill Climb with Sideways Move")
    print("3. Random Restart Hill Climb")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    print("6. Genetic Algorithm")
    alg = int(input("=> "))
