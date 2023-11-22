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

global prob_forest, prob_scrubland, prob_chaparral, prob_water, prob_town, forest_rate, scrub_rate, chaparral_rate, town_rate

prob_forest = 0.85
prob_chaparral = 0.6
prob_scrubland = 0.3
prob_water = 0
prob_town = 0.5

def wind_func(neighbourstates, winddirection):
    #  nw, n, ne, w, e, sw, s, se
    nw, n, ne, w, e, sw, s, se = neighbourstates
    if ((winddirection == "nw") and (se == 1 or se == 2 or se == 3)):
        return True
    elif ((winddirection == "n") and (s == 1 or s == 2 or s == 3)):
        return True
    elif ((winddirection == "ne") and (sw == 1 or sw == 2 or sw == 3)):
        return True
    elif ((winddirection == "w") and (e == 1 or e == 2 or e == 3)):
        return True
    elif ((winddirection == "e") and (w == 1 or w == 2 or w == 3)):
        return True
    elif ((winddirection == "sw") and (ne == 1 or ne == 2 or ne == 3)):
        return True
    elif ((winddirection == "s") and (n == 1 or n == 2 or n == 3)):
        return True
    elif ((winddirection == "se") and (nw == 1 or nw == 2 or nw == 3)):
        return True
    else: return False


def transition_func(grid, neighbourstates, neighbourcounts, fuelgrid, initgrid):
    # dead = state == 0, live = state == 1, sick = state == 2
    # unpack state counts for all states
    burnt, burning1, burning2, burning3, chapparral, lake, dense_forest, scrubland, town = neighbourcounts
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    burning = burning1 + burning2 + burning3
    # create boolean arrays for the birth & survival rules
    
    
    fuel_grid = update_fuel_grid(grid, fuelgrid, initgrid)
    
    now_burnt = (fuel_grid <= 0)

    not_burning_cells = (grid != 1) & (grid != 0) & (grid != 5)
    burning_neighbours = (neighbourcounts[1] > 0)
    winddirection = (S != -100)
    wind_effect = (burning_neighbours) & winddirection
    burn_prob = update_probability()
    print(burn_prob)
    prob_grid = burn_prob_grid(grid, wind_effect)
    
    now_burning1 = ((not_burning_cells & burning_neighbours) & (burn_prob > prob_grid))
    still_burning1 = (grid == 1) & (fuel_grid > 0)

    grid[now_burnt] = 0
    grid[now_burning1] = 1
    grid[still_burning1] = 1
    
    return grid

def burn_prob_grid(grid, wind):
    
    forest = (grid == 6) * (1-prob_forest)
    chaparral = (grid == 4) * (1-prob_chaparral)
    scrub_land = (grid == 7) * (1-prob_scrubland)
    water = (grid == 5) 
    town = (grid == 8) * prob_town
    
    prob_grid = forest + chaparral + scrub_land + water + town
    prob_grid[wind] += 0.15
    return prob_grid

def update_fuel_grid(grid, fuel_grid, init_grid):
    burning_cells = (grid == 1)
    
    forest = (init_grid == 6)
    burning_forest = burning_cells & forest
    fuel_grid[burning_forest] -= 50
    
    chaparral = (init_grid == 4)
    burning_chaparral = burning_cells & chaparral
    fuel_grid[burning_chaparral] -= 100
    
    scrub_land = (init_grid == 7)
    burning_scrub = burning_cells & scrub_land
    fuel_grid[burning_scrub] -= 300
    
    town = (init_grid == 8)
    burning_town = burning_cells & town
    fuel_grid[burning_town] -= 100
    
    return fuel_grid

def update_probability():
    return random.uniform(0,1)

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "CA Simultation of Forest Fires"
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
    initial_grid = config.initial_grid

    fuel_grid = np.ones(initial_grid.shape) * 1000
    # Create grid object
    grid = Grid2D(config, (transition_func, fuel_grid, initial_grid))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()
    
    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
