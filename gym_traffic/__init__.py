from gym.envs.registration import register

register(
    id='GymTraffic-v0',
    entry_point='gym_traffic.envs:GymTrafficEnv',
)
