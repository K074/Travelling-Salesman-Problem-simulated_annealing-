import numpy as np
import random
import math
import matplotlib.pyplot as plt
import os

# Generate random cities
def randomcords(ncities, mx, my):
    cities = set()
    while len(cities) < ncities:
        city = (random.randint(0, mx), random.randint(0, my))
        cities.add(city)
    return list(cities)

def loadtext(file):
    cities = []
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            if ',' in line:
                x, y = line.split(',')
            else:
                x, y = line.split()         # for "Space"
            cities.append((int(x), int(y)))
    return cities

def totaldist(cities, path):
    dist = 0
    for i in range(len(path)):
        city1 = cities[path[i]]
        city2 = cities[path[(i + 1) % len(path)]]
        dist += ((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2) ** 0.5  # Euclidean distance
    return dist

def annealing(cities, inititmp, coorate, mintmp, nneighbors):
    curpath = list(range(len(cities)))
    random.shuffle(curpath)
    curdist = totaldist(cities, curpath)

    bpath = curpath
    bdist = curdist

    tmp = inititmp
    best_distances_per_iteration = []  # Track best distance at each iteration

    while tmp > mintmp:
        bneighbpath = None
        bneighbordist = 1144141  # sufficiently large for the first time

        # Multi neighbors
        for _ in range(nneighbors):
            npath = curpath[:]
            i, j = random.sample(range(len(cities)), 2)
            npath[i], npath[j] = npath[j], npath[i]
            newdist = totaldist(cities, npath)

            # Select the best neighbor
            if newdist < bneighbordist:
                bneighbpath = npath
                bneighbordist = newdist

        # % to accept the best neighbor
        betterneighbor = bneighbordist < curdist
        worseneighbor = random.random() < math.exp((curdist - bneighbordist) / tmp)

        if betterneighbor or worseneighbor:
            curpath = bneighbpath
            curdist = bneighbordist

            # Update the best path found
            if curdist < bdist:
                bpath = curpath
                bdist = curdist

        # Track best distance of the iteration
        best_distances_per_iteration.append(bdist)

        # Lower the temperature
        tmp *= coorate

    return bpath, bdist, best_distances_per_iteration


# Visualize route
def visuaroute(cities, route, title):
    x_coords = [cities[i][0] for i in route] + [cities[route[0]][0]]
    y_coords = [cities[i][1] for i in route] + [cities[route[0]][1]]
    
    # Increase plot size
    plt.figure(figsize=(8, 8))  
    plt.plot(x_coords, y_coords, 'o-', color='black', label="Route")
    plt.scatter(x_coords, y_coords, color='red', zorder=5)
    plt.scatter([x_coords[0]], [y_coords[0]], color='green', s=150, label="Start", edgecolor='black')

    # Add arrow
    plt.arrow(x_coords[-2], y_coords[-2], 
              x_coords[-1] - x_coords[-2], 
              y_coords[-1] - y_coords[-2], 
              head_width=0.5, head_length=0.5, fc='blue', ec='blue', zorder=4)
    
    # Add legend
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.legend()  
    plt.axis('equal')  
    plt.show()

def printcoord(cities, route):
    print("Coordinates:")
    for i in route:
        print(f"City {i}: {cities[i]}")


# Main 
if __name__ == "__main__":
    file = "text.txt"       

    if os.path.exists(file):
        print(f"Loading cities from {file}")
        cities = loadtext(file)
    else:
        print("File not found. Generating random cities.")        
        ncities = 20 
        x = 200
        y = 200   
        cities = randomcords(ncities, x, y)

    inititmp = 99
    coorate = 0.9999
    mintmp = 1

    nruns = 10  
    boverpath = None
    boverdist = 919819  # sufficiently large for the first time

    overall_best_distances = []  # Track the overall best distance at each iteration
    best_distances_per_run = []  # Store distances for plotting per run

    for run in range(nruns):
        print(f"\nRun {run + 1}/{nruns}:")
        bpath, bdist, best_distances = annealing(cities, inititmp, coorate, mintmp, 3)

        print("Best Path:", bpath)
        print(f"Best Distance: {bdist:.2f}")
        printcoord(cities, bpath)

        # Update overall best path and distance
        if bdist < boverdist:
            boverdist = bdist
            boverpath = bpath

        best_distances_per_run.append(best_distances)  # Save distances for this run

    print("\nOverall Best Path:", boverpath)
    print(f"Overall Best Distance: {boverdist:.2f}")
    printcoord(cities, boverpath)

    visuaroute(cities, boverpath, "Best route")

    # Flatten the list of distances from all runs
    for distances in best_distances_per_run:
        overall_best_distances.extend(distances)

    # Plot best distance over iterations
    plt.plot(range(len(overall_best_distances)), overall_best_distances, label='Best Distance')
    plt.title("Best Distance Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Distance")
    plt.legend()
    plt.show()
