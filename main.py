from racetrack import Racetrack
from rl_racetrack import RLRacetrack
from view import View


if __name__ == '__main__':
    config = {
        'grid_shape': (30, 30),
        'episodes': int(1e4),
        'epsilon': 0.1,                                 # probability of choosing random action
        'delta': 0.1,                                   # prob to not update velocity (not take action)
        'timestep_reward': -1,                          # reward for each timestep. Actually has no impact
        'update_state_values_rule': 'every_visit',      # 'first_visit' or 'every_visit'
        'min_speed_x': 0,
        'max_speed_x': 5,
        'min_speed_y': -5,
        'max_speed_y': 0,
        'max_episode_length': 1e3,
        'seed': 754,                                   #  754 # other ok seeds 171#55#51 #754 47585
    }
    track = Racetrack(config)
    grid_file = track.create_grid()

    track.print()

    rl_racetrack = RLRacetrack(config, track)

    logs = 'runs_'+grid_file.lstrip('grid_')
    rl_racetrack.run('runs/'+logs)
    rl_racetrack.report()

    #visualization = View()

    #visualization.load_map('runs/'+grid_file)
    #visualization.load_path('runs/'+logs)
    #visualization.show()

    #visualization.show()
    #visualization.save()
