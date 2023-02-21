from racetrack import Racetrack
from rl_racetrack import RLRacetrack
from view import View
import yaml

if __name__ == '__main__':
    # Read config.yaml file
    config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)

    track = Racetrack(config)
    grid_file = track.create_grid()

    #track.test_crash()
    track.print()

    rl_racetrack = RLRacetrack(config, track)

    logs = 'runs_' + grid_file.lstrip('grid_')
    rl_racetrack.run('runs/' + logs)
    rl_racetrack.report()

    visualization = View()

    visualization.load_map('runs/'+grid_file)
    visualization.load_path('runs/'+logs)
    visualization.show()

    #visualization.show()
    #visualization.save()
