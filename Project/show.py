from stable_baselines3 import PPO
from enviorment import TowerClimberEnv

env = TowerClimberEnv(render_mode="human")

model = PPO.load("models/savedModel", env=env)

obs, _ = env.reset()
while True:
    action, _ = model.predict(obs)
    obs, rewards, terminated, truncated, info = env.step(action)
    env.render()
