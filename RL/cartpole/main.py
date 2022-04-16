import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from time import sleep

from DQN_Agent import DQN_Agent

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

from tqdm import tqdm

# https://blog.gofynd.com/building-a-deep-q-network-in-pytorch-fa1086aa5435

env = gym.make('CartPole-v0')
input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n
exp_replay_size = 256
agent = DQN_Agent(seed=1423, layer_sizes=[
                  input_dim, 64, output_dim], lr=1e-3, sync_freq=5, exp_replay_size=exp_replay_size)

# initiliaze experiance replay
index = 0
for i in range(exp_replay_size):
    obs = env.reset()
    done = False
    while(done != True):
        A = agent.get_action(obs, env.action_space.n, epsilon=1)
        obs_next, reward, done, _ = env.step(A.item())
        agent.collect_experience([obs, A.item(), reward, obs_next])
        obs = obs_next
        index += 1
        if(index > exp_replay_size):
            break

# Main training loop
losses_list, reward_list, episode_len_list, epsilon_list = [], [], [], []
index = 128
episodes = 200  # 10000
epsilon = 1

for i in tqdm(range(episodes)):
    obs, done, losses, ep_len, rew = env.reset(), False, 0, 0, 0
    while(done != True):
        ep_len += 1
        A = agent.get_action(obs, env.action_space.n, epsilon)
        obs_next, reward, done, _ = env.step(A.item())
        agent.collect_experience([obs, A.item(), reward, obs_next])

        obs = obs_next
        rew += reward
        index += 1

        if(index > 128):
            index = 0
            for j in range(4):
                loss = agent.train(batch_size=16)
                losses += loss
    if epsilon > 0.05:
        epsilon -= (1 / 5000)

    losses_list.append(losses/ep_len), reward_list.append(
        rew), episode_len_list.append(ep_len), epsilon_list.append(epsilon)


for i in tqdm(range(2)):
    obs, done, rew = env.reset(), False, 0
    while (done != True):
        A = agent.get_action(obs, env.action_space.n, epsilon=0)
        obs, reward, done, info = env.step(A.item())
        rew += reward
        sleep(0.01)
        env.render()
    print("episode : {}, reward : {}".format(i, rew))
