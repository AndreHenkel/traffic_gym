import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Traffic-v0',
    entry_point='gym_traffic.envs:TrafficEnv',
)
