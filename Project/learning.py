import os

from enviorment import TowerClimberEnv

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.policies import MultiInputActorCriticPolicy

from stable_baselines3.common.env_checker import check_env

log_dir = "model/"
os.makedirs(log_dir, exist_ok=True)

if __name__ == '__main__':
    env = TowerClimberEnv(render_mode=None)

    check_env(env)
    env = Monitor(env, "models/TestMonitor")

    learning_rate=0.0003
    model = PPO(MultiInputActorCriticPolicy, env, verbose=1, tensorboard_log="./board/", learning_rate=learning_rate)

    #model = PPO.load("model/savedModel,new1M", env=env)
    
    print("------------- Start Learning -------------")
    model.learn(total_timesteps=20000, tb_log_name="PPO-" + str(learning_rate))
    model.save("models/savedModel")
    print("------------- Done Learning -------------")
    
    env = TowerClimberEnv("human")
    
    obs, _ = env.reset()
    while True:
        action, _ = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        env.render()