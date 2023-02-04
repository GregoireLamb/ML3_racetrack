from episode import Episode


class RLRacetrack:
    def __init__(self, config, racetrack):
        self.racetrack = racetrack
        self.n_episodes = config['episodes']
        self.epsilon = config['epsilon']
        self.state_values = {}      # (pos, vel) -> (estimated return, count)
        self.episodes = []

    def run(self):
        for episode in range(self.n_episodes):
            ep = Episode(self.racetrack, self.epsilon, self.state_values)
            self.episodes.append(ep)
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
        # 1. Plot the state values map (project into position space)
        # 2. Plot the convergence curve: return vs iteration
        # 3. Plot path following learnt policy (use follow_policy method)
        pass

    def follow_policy(self):
        # Run the policy and print the path
        pass