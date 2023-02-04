from racetrack import Racetrack
from rl_racetrack import RLRacetrack
from view import View


if __name__ == '__main__':
    track = Racetrack()

    config = {
        'episodes': int(1e5),
        'epsilon': 0.1,     # probability of choosing random action
        'delta': 0.1,       # prob to not update velocity (not take action)
    }

    rl_racetrack = RLRacetrack(config, track)

    rl_racetrack.run()
    rl_racetrack.report()

    visualization = View(config, rl_racetrack)
    visualization.show()

