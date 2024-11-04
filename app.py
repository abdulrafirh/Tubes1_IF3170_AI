from algorithm import *
from beta import *

def mainDihitungDulu(algo, argv = {}):

    result = algorithm.run_algorithm(algo, argv)
    genericPrinter(result)

    cube_states = resultToStates(result)
    objective_value = result["h_values"]
    visualizer = CubeVisualizer(cube_states)
    visualizer.fig.show()

    line_fig1 = go.Figure()
    line_fig1.add_trace(go.Scatter(x=list(range(len(objective_value))), y=objective_value, mode='lines+markers', name='Objective Value'))
    line_fig1.update_layout(title='Objective Value with respect to Iteration Number',
                            xaxis_title='Iteration Number',
                            yaxis_title='Objective Value')

    plot(line_fig1, filename='objective_value_plot.html', auto_open=True)

    if algo == "simulated annealing":
        edeltaT = result["boltzmanns"]

        line_fig2 = go.Figure()
        line_fig2.add_trace(go.Scatter(x=list(range(len(edeltaT))), y=edeltaT, mode='lines+markers', name='e^delta(E)/T Value'))
        line_fig2.update_layout(title='e^delta(E)/T Value with respect to Iteration Number',
                                xaxis_title='Iteration Number',
                                yaxis_title='e^delta(E)/T Value')

        plot(line_fig2, filename='edeltaT_value_plot.html', auto_open=True)

def genericPrinter(output):
   print("\n========================== OUTPUT RESULTS ==========================")
   print("Final H: ", output['final H'])
   print("Duration: ", output['duration'])

   if (output.get('stucks')) :
      print("Stucks: ", output['stucks'])

   if(output.get('iteration_per_restarts')) :
       print("Iteration per Restarts: ", output['iteration_per_restarts'])
       print("Restart Counts: ", output['restart_counts'])


isFile = input("Do you want to input your own file? TODO (y/n) => ")
print("========================== Choose your algorithm ==========================")
print("1. Steepest Ascent Hill Climb")
print("2. Hill Climb with Sideways Move")
print("3. Random Restart Hill Climb")
print("4. Stochastic Hill Climbing")
print("5. Simulated Annealing")
print("6. Genetic Algorithm")
print("7. Die")
alg = int(input("=> "))

while True:
    if(alg == 1 or alg == 4 or alg == 5):
        output = None
        if(alg==1):
         mainDihitungDulu("steepest ascent")
        elif(alg==4):
         mainDihitungDulu("stochastic")
        elif(alg==5):
         mainDihitungDulu("simulated annealing")
    elif(alg == 2):
        max_limit = int(input("Max Limit => "))
        mainDihitungDulu("sideways ascent",{"max_limit": max_limit})
    elif(alg== 3):
        max_restart = int(input("Max Restart => "))
        mainDihitungDulu("random restart",{"max_restart": max_restart})
    elif(alg==6):
        population_size = int(input("Population Size => "))
        iteration_max = int(input("Maximum Iteration => "))
        output = mainDihitungDulu("genetic algorithm",{"popSize": population_size, "max_iteration": iteration_max})
    elif(alg==7):
        exit()
    else:
        print("Invalid input, so i will die")
        break
    print("\n\n========================== Choose your algorithm ==========================")
    print("Choose your algorithm:")
    print("1. Steepest Ascent Hill Climb")
    print("2. Hill Climb with Sideways Move")
    print("3. Random Restart Hill Climb")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    print("6. Genetic Algorithm")
    print("7. Die")
    alg = int(input("=> "))
