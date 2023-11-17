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


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1, sick = state == 2
    # unpack state counts for all states
    burnt, burning1, burning2, burning3, chapparral, lake, dense_forest, scrubland, town = neighbourcounts
    burning = burning1 + burning2 + burning3
    # create boolean arrays for the birth & survival rules

    now_burnt = (grid == 1)
    now_burning1 = (grid == 2) | ((grid == 7) & (burning > 0)) | ((grid == 8) & (burning > 0))
    now_burning2 = (grid == 3) | ((grid == 4) & (burning > 1))
    now_burning3 = (grid == 6) & (burning > 2)
    still_burning1 = ((grid == 1) & (random.randint(1, 100) > 90))
    still_burning2 = ((grid == 2) & (random.randint(1, 100) > 50))
    still_burning3 = ((grid == 3) & (random.randint(1, 100) > 20))

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
    #States: burnt, burning, chapparral, lake, dense forest, canyon
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0, 0, 0), (1, 0, 0), (0.6, 0, 0), (1, 0.5, 0), (0.6, 0.6, 0), (0.4, 1, 1), (0.4, 0.2, 0), (1, 1, 0.2), (1, 0, 1)]
    config.num_generations = 150

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
