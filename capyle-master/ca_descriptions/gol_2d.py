# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect

this_file_loc = inspect.stack()[0][1]
main_dir_loc = this_file_loc[: this_file_loc.index("ca_descriptions")]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + "capyle")
sys.path.append(main_dir_loc + "capyle/ca")
sys.path.append(main_dir_loc + "capyle/guicomponents")
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
import random

# loops through the neighbour grid setting values that correspond to burning to True
# and all other values to false
def burningneighbourboolean(neighbour):
    for x in range(80):
        for y in range(80):
            if (neighbour[x][y] == 1 or neighbour[x][y] == 2 or neighbour[x][y] == 3):
                neighbour[x][y] = True
            else:
                neighbour[x][y] = False
    return neighbour

# sets all burning values from True to False based on a probability
# lower probability for cells without a burning neighbour on the opposite side of wind direction
def compareburningandneighbourboolean(neighbour, burning, probability):
    for i in range(80):
        for j in range(80):
            if (burning[i][j] and neighbour[i][j]):
                if (random.randint(1, 100) > probability):
                    burning[i][j] = False
            elif (burning[i][j] == True):
                if (random.randint(1, 100) > probability-15):
                    burning[i][j] = False
            # else: burning[i][j] = False
    return burning

# loops through and sets all burning values from True to False using a lower probability
# to represent no wind
def applyburningprobabilities(burning, probability):
    for i in range(80):
        for j in range(80):
            if (burning[i][j] == True & (random.randint(1,100) > probability-15)):
                burning[i][j] = False
    return burning

# uses the above functions to edit now_burning grids so that the corresponding wind probabilities are applied
# based on an input of winddirection
def wind_func(neighbourstates, winddirection, now_burning, probability):
    #  nw, n, ne, w, e, sw, s, se
    nw, n, ne, w, e, sw, s, se = neighbourstates
    if (winddirection == "nw"):
        se = burningneighbourboolean(se)
        now_burning = compareburningandneighbourboolean(se, now_burning, probability)
        return now_burning
    elif (winddirection == "n"):
        s = burningneighbourboolean(s)
        now_burning = compareburningandneighbourboolean(s, now_burning, probability)
        return now_burning
    elif (winddirection == "ne"):
        sw = burningneighbourboolean(sw)
        now_burning = compareburningandneighbourboolean(sw, now_burning, probability)
        return now_burning
    elif (winddirection == "w"):
        e = burningneighbourboolean(e)
        now_burning = compareburningandneighbourboolean(e, now_burning, probability)
        return now_burning
    elif (winddirection == "e"):
        w = burningneighbourboolean(w)
        now_burning = compareburningandneighbourboolean(w, now_burning, probability)
        return now_burning
    elif (winddirection == "sw"):
        ne = burningneighbourboolean(ne)
        now_burning = compareburningandneighbourboolean(ne, now_burning, probability)
        return now_burning
    elif (winddirection == "s"):
        n = burningneighbourboolean(n)
        now_burning = compareburningandneighbourboolean(n, now_burning, probability)
        return now_burning
    elif (winddirection == "se"):
        nw = burningneighbourboolean(nw)
        now_burning = compareburningandneighbourboolean(nw, now_burning, probability)
        return now_burning


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1, sick = state == 2
    # unpack state counts for all states
    burnt, burning1, burning2, burning3, chapparral, lake, dense_forest, scrubland, town = neighbourcounts
    burning = burning1 + burning2 + burning3
    # create boolean arrays for the birth & survival rules
    #winddirection can be set to s for southern wind,se,e,ne,n,nw,w or sw for their corresponding wind directions
    winddirection = "s"
    # setting wind to true means that wind effects fire spread in the wind direction
    # setting win to false means that the wind has no effect
    wind = True
    prob_forest = 0.25
    prob_scrubland = 0.8
    prob_chaparral = 0.6
    prob_water = 0
    prob_town = 0.5

    now_burnt = (grid == 1)

        # now_burning1 = (grid == 2) | (((grid == 7) & (burning > 0)) | ((grid == 8) & (burning > 0)) & (
        #             random.randint(1, 100) < 85))
        # now_burning2 = (grid == 3) | ((grid == 4) & (burning > 1) & (random.randint(1, 100) < 55))
        # now_burning3 = (grid == 6) & (burning > 2) & (random.randint(1, 100) < 15)
        #
        # now_burning1 = (grid == 2) | (((grid == 7) & (burning > 0)) | ((grid == 8) & (burning > 0)) & (
        #             random.randint(1, 100) < 75))
        # now_burning2 = (grid == 3) | ((grid == 4) & (burning > 1) & (random.randint(1, 100) < 45))
        # now_burning3 = (grid == 6) & (burning > 2) & (random.randint(1, 100) < 5)


    now_burning1 = (grid == 2) | (((grid == 7) & (burning > 0) | (grid == 8)) & (burning > 0))
    now_burning2 = (grid == 3) | ((grid == 4) & (burning > 1))
    now_burning3 = (grid == 6) & (burning > 1)
    if (wind):
        now_burning1 = wind_func(neighbourstates, winddirection, now_burning1, prob_scrubland*100)
        now_burning2 = wind_func(neighbourstates, winddirection, now_burning2, prob_chaparral*100)
        now_burning3 = wind_func(neighbourstates, winddirection, now_burning3, prob_forest*100)
    else:
        now_burning1 = applyburningprobabilities(now_burning1, prob_scrubland*100)
        now_burning2 = applyburningprobabilities(now_burning2, prob_chaparral*100)
        now_burning3 = applyburningprobabilities(now_burning3, prob_forest*100)

    still_burning1 = ((grid == 1) & (random.randint(1, 100) < 10))
    still_burning2 = ((grid == 2) & (random.randint(1, 100) < 60))
    still_burning3 = ((grid == 3) & (random.randint(1, 100) < 80))

    grid[now_burnt] = 0
    grid[now_burning1] = 1
    grid[now_burning2] = 2
    grid[now_burning3] = 3
    grid[still_burning1] = 1
    grid[still_burning2] = 2
    grid[still_burning3] = 3
    
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    #States: burnt, burning1, burning2, burning3, chapparral, lake, dense forest, canyon, town
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0, 0, 0), (1, 0, 0), (0.6, 0, 0), (1, 0.5, 0), (0.6, 0.6, 0), (0.4, 1, 1), (0.4, 0.2, 0), (1, 1, 0.2), (1, 0, 1)]
    config.num_generations = 200
    config.wrap = False

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
