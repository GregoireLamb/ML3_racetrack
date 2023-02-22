# Reinforcement Learning for the Optimization of Racetrack Trajectories
In this project, we solve the problem of finding the optimal (fastest) trajectory in a curve. We use a Monte-Carlo approach for optimizing the RL formulation of the problem. We want to maximize the max expected return, which is defined as (minus) the length of the path from current position to the endline.

### Classes and modules
![image](https://user-images.githubusercontent.com/38510928/220766756-f98305dd-5d92-488e-82ae-28129565803c.png)

### How to run
A configuration file should be provided in .yaml format. Set the configuration to match the desired execution settings.

- Single Optimization: 
`python main.py`

- Multiple Optimization: in the multiple_rl.py script, specify the parameters their ranges of values to test.
`python multiple_rl.py`

### Results and Visualization:
Multiple reports and visualizations are provided after the Optimization, including the following:
- State values map: we plot the max expected return (over all possible velocities) for a particular position. 
![image](https://user-images.githubusercontent.com/38510928/220769701-25704848-ef2c-4587-889c-2301d0621627.png)

- Learning curve: a 100-moving average of the return by episode. 
![image](https://user-images.githubusercontent.com/38510928/220770011-130be703-8305-409c-94af-04895e71f6f1.png)

- Simulations visualization: using pygame, we visualize 10 episodes spread among all the trials.
![image](https://user-images.githubusercontent.com/38510928/220768947-656b54da-936e-424b-a5ea-a02c8b78e57c.png)

- Learning curve comparison: when the **multiple_rl** is executed, we compare the learning curves for the different tested settings:
![image](https://user-images.githubusercontent.com/38510928/220770466-72a36d05-c4be-4d8b-97fd-769455201cb5.png)





