# © Max Miller, 2022
import random
import numpy as np
from math import floor, sqrt
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ 
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \
import Biomass
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
def gradient_descent(log, location, biomass_gradient, momentum):
    """returns the fish's current momentum"""
    # horizontal momentum
    momentum[0] = (
        25.0 * biomass_gradient[0][floor(location[0])][floor(location[1])]
        + 0.976 * momentum[0]
    )
    # vertical momentum
    momentum[1] = (
        25.0 * biomass_gradient[1][floor(location[0])][floor(location[1])]
        + 0.976 * momentum[1]
    )
    # velocity control : The fish can only swim so fast!
    # 0.5 represents maximum speed
    if Distance([location[0] - momentum[0], location[1] - momentum[1]], log) > 0.5:
        momentum[0], momentum[1] = 0.5 * momentum[0], 0.5 * momentum[1]

    # using a iterable facilitates easy access to x and y momentum
    return momentum


Distance = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
"""Returns the length of a line segment between two coordinates"""
# Using 2 dimensional Euclidean distance (x1-y1)^2 + (x2-y2)^2


def simulation(time):
    """creates a simulation of specified length"""
    # creates a container to store coordinates and current interval
    log = np.zeros(shape=[time + 1, 3])
    seed = random.randint(0, 10000)
    biomass = Biomass.biomass(seed)
    biomassGradient = np.gradient(biomass)

    # Spawns the fish in a random part of the map.
    # Uniform gives all possiblities an equal chance
    location = [np.random.uniform(0, 150, 1), np.random.uniform(0, 150, 1)]

    # 0th index = X-momentum, 
    # 1st index = Y-momentum
    momentum = [0.0, 0.0]

    i = 0
    while i < time:
    # this loop controls how many movements the fish makes during the simulation 
        seed, i = seed + 1, i + 1
        momentum = gradient_descent(log[i - 1], location, biomassGradient, momentum)

        # subtracting the momentum moves the fish's location
        # reminder: 0th index = X, 1st index = Y
        location[0] -= momentum[0]
        location[1] -= momentum[1]

        # Euclidean distance between current and former location
        # reinforcment when the gradient approches 0
        if Distance([location[0], location[1]], log[i - 1]) < 0.1:
            i -= 1
            biomassGradient = np.gradient(Biomass.biomass(seed))

        # This saves the simulation data 
        log[i] = [location[0], location[1], i]
        print(location[0], location[1], i)
    # visualizing the simulation:

    fig = plt.figure(facecolor="#1c1c1c")
    mpl.rc("axes", edgecolor="white", linewidth=2.5)
    (logasline,) = plt.plot([], [], "wo")
    plt.imshow(biomass, cmap="plasma")
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(

        "Simulating Spatial Trajectories of Pelagic Fish",
        color="White",
        family="monospace",
        labelpad=10,
        size="large",
    )
    plt.title(
        "© Max Miller, 2022",
        family="monospace",
        size="smaller",
        color="white",
        loc="left",
    )
    # The plasma Uniform Sequential colormap was used because of the high contrast 
    # "_r" gives the inverted version 
    cb = fig.colorbar(
        mpl.cm.ScalarMappable(
            cmap="plasma_r", norm=mpl.colors.Normalize(vmin=0, vmax=10)
        )
    )

    #these choices are just stylistic and don't serve a functional purpose
    cb.ax.yaxis.set_tick_params(color="white")
    cb.outline.set_edgecolor("White")
    cb.ax.set_title("Biomass (kg/km)", color="white", pad=15, family="monospace")
    plt.setp(plt.getp(cb.ax.axes, "yticklabels"), color="white")

    # typecasting ndarray to list makes it easier to utilize
    loglist = log.tolist()

    #this is the core function behind the animation
    #its called on each frame and moves the white circle
    def animate_log(i):
        """updates the fish's position"""
        logasline.set_xdata(loglist[i][0])
        logasline.set_ydata(loglist[i][1])
        return logasline

    # FuncAnimation works well, but its probably not the most optimal animation implementation 
    anim = FuncAnimation(fig, animate_log, frames=len(loglist), interval=1)
    plt.show()

    # this was added as a precaution for memory leaks caused by matplotlib objects holding onto memory 
    # Its unclear whether its addition was what solved the problem
    plt.gcf().clear()


# Modify this parameter to alter the duration of the simulation
simulation(1000)

# *longer simulations take more time to generate*
