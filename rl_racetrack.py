from episode import Episode

class RLRacetrack:
    def __init__(self, config, racetrack):
        self.racetrack = racetrack
        self.episodes = config['episodes']
        self.epsilon = config['epsilon']
        self.state_values = {}      # (pos, vel) -> (estimated return, count)

    def run(self):
        for episode in range(self.episodes):
            ep = Episode(self.racetrack, self.epsilon, self.state_values)
            path = ep.simulate()
            self.update_state_values(path)

    def update_state_values(self, path):
        # Evaluate the path.
        """
        Loop for each step of episode, t = T 1, T 2,..., 0:
        G <- G + Rt+1
        Append G to Returns(St)
        V (St) <- average(Returns(St))
        """
        pass

    def report(self):
        # Print some stuff
        pass

    def follow_policy(self):
        # Run the policy and print the path
        pass