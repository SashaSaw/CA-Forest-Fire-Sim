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


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1, sick = state == 2
    # unpack state counts for all states
    burnt, burning1, burning2, burning3, chapparral, lake, dense_forest, scrubland = neighbourcounts
    burning = burning1 + burning2 + burning3
    # create boolean arrays for the birth & survival rules

    still_burnt = (grid == 1)
    now_burning1 = (grid == 2) | ((grid == 7) & (burning > 0))
    now_burning2 = (grid == 3) | ((grid == 4) & (burning > 1))
    now_burning3 = (grid == 6) & (burning > 2)
    still_chapparral = ((grid == 4) & (burning < 2))
    still_lake = (grid == 5)
    still_forest = (grid == 6) & (burning < 3)
    still_scrubland = (grid == 7) & (burning == 0)

    grid[still_burnt] = 0
    grid[now_burning1] = 1
    grid[now_burning2] = 2
    grid[now_burning3] = 3
    grid[still_chapparral] = 4
    grid[still_lake] = 5
    grid[still_forest] = 6
    grid[still_scrubland] = 7

    '''
    # if 3 live neighbours and is dead -> cell born
    birth = (live_neighbours == 3) & (grid == 0)

    # if more than 2 neighbours are sick, live -> sick, 4 or less neighbours are sick, sick -> sick  or if there are more
    # than 0 sick neighbours and sick, sick -> sick
    sick = (((sick_neighbours > 2) | (sick_neighbours <= 4)) & (grid == 1)) | (
        (sick_neighbours > 0) & (grid == 2)
    )

    # if 2 or 3 live neighbours and is alive -> survives, if no sick neighbours, sick -> survive
    survive = (((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)) | (
        (sick_neighbours == 0) & (grid == 2)
    )

    # death = (live_neighbours <= 1) | (sick_neighbours <= 1) | (sick_neighbours > 4)

    # Set all cells to 0 (dead)
    grid[:, :] = 0

    # Set cells to 1 where either cell is born or survives
    grid[birth | survive] = 1
    grid[sick] = 2
    '''
    
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7)
    #States: burnt, burning1, burning2, burning3, chapparral, lake, dense forest, canyon
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0.6, 0.6, 0), (0.4, 1, 1), (0.4, 0.2, 0), (1, 1, 0.2)]
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
