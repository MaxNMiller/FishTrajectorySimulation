# © Max Miller, 2022
from itertools import product
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ 
from numpy import amax, amin, interp, linspace, meshgrid, zeros
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ 
from noise import noisemap
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
def preparenoise(seed):
    """reduces varience in 2 dimensional noise"""
    horAxis, verAxis = meshgrid(
        # 150 samples for 150 meters^2
        linspace(0, 3, 150), linspace(0, 3, 150)
    )
    # v1 holds the two extremes of the noise array
    # these values are important when normalizing a dataset
    noise = noisemap(horAxis, verAxis, setseed=seed)
    v1 = [amin(noise), amax(noise)]

    # scaling noise with linear interpolation
    for x, y in product(range(len(noise)), range(len(noise))):
    # despite seeming verbose, range(length()) preforms better than enumuration here
        noise[x][y] = interp(noise[x][y], v1, [0, 1])
    return noise


def prepareboundary(noise):
    """adds a boundary of low values to 2-dimensional noise"""

    # an immediate issue during development was keeping the fish contained within the simulation area
    # modyifing the noise felt like the most natural solution, but its not mathematically impenetrable
    distancefromperimeter = zeros(noise.shape)
    xInterval, yInterval = linspace(2, 0, 75), linspace(2, 0, 75)

    for x, y in product(
        range(len(distancefromperimeter)), range(len(distancefromperimeter))
    ):
        #these equations require a lot of fine tuning since they directly affect the perimeter's biomass
        Xpower = x - 1 if x <= 75 else 75 - x
        Ypower = y - 1 if y <= 75 else 75 - y
        best = lambda a, b: a if a > b else b
        distancefromperimeter[x][y] += best(5.4, 2.7 ** (xInterval[Xpower]))
        distancefromperimeter[x][y] += best(5.4, 2.7 ** (yInterval[Ypower]))

    # scaling distance with linear interpolation
    v1 = [amin(distancefromperimeter), amax(distancefromperimeter)]
    for i, j in product(
        range(len(distancefromperimeter)), range(len(distancefromperimeter))
    ):
        distancefromperimeter[i][j] = interp(
            distancefromperimeter[i][j], v1, [0.0, 0.475]
        )

    return distancefromperimeter


def biomass(seed):
    """creates a refined random distribution of biomass"""
    noise = preparenoise(seed)
    return noise + prepareboundary(noise)
