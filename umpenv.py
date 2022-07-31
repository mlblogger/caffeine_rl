import os
import sys
import caffeine
import gym
from gym import spaces
import numpy as np

class UMPEnv(gym.Env):
    def __init__(self):
        self.caffeine_model = caffeine.UMP()
        self.day = None
        self.days_max = 5
        self.time = None
        self.time_period = 24
        self.mode = None
        self.time_delta = 0.2
        self.days_hours = 24

        self.action_space = spaces.Discrete(1)
        self.observation_space = spaces.Box(low=-1,high=1,dtype=np.float32)

        self.caffeine_stock = None

        self.caffeine_doses_map = {
            0 : 0.0,
            1 : 0.05,
            2 : 0.1,
            3 : 0.2
        }
        
        return

    def step(self,action):
        done = False

        if action > 0:
            action = self.caffeine_doses_map[action]
            if action <= self.caffeine_stock:
                self.caffeine_model.caffeine_dose_update(action,self.time)
                self.caffeine_stock -= action
            
        if self.time < self.caffeine_model.sleep_time:
            caffeine_free_perf, caffeine_perf = self.caffeine_model.caffeine_performance(self.time,self.mode)
            info = { 'time' : self.time, 'caff_perf' : caffeine_perf, 'caff_free_perf' : caffeine_free_perf, 'sleep_time' : self.caffeine_model.sleep_time, 'stock' : self.caffeine_stock }
            obs = self.get_obs(self.day,self.time,caffeine_perf)
        else:
            self.mode = 'sleep'
            while self.time < self.days_hours:
                self.caffeine_model.caffeine_free_performance(self.time,self.mode)
                self.time += self.time_delta
            info = {}
            obs = None
            done = True
            return obs, 0, done, info

        self.time += self.time_delta

        reward = caffeine_free_perf - caffeine_perf
        
        return obs, reward, done, info

    def reset(self):
        if self.day is None:
            self.day = 0
        else:
            self.day += 1
            self.day = self.day % self.days_max
            if self.day == 0:
                self.caffeine_model = caffeine.UMP()

        self.caffeine_stock = 0.3
        self.caffeine_model.reset_start_day()
        self.time = 0
        self.mode = 'wake'
        sleep_time = np.random.choice(list(range(160,240,2)))/10
        self.caffeine_model.sleep_time = sleep_time

        caffeine_perf, caffeine_free_perf = self.caffeine_model.caffeine_performance(self.time,'wake')
        obs = self.get_obs(self.day,self.time,caffeine_perf)
        return obs

    def get_obs(self,day,time,perf):
        days = [0]*self.days_max
        days[day] = 1
        days.append(time/self.days_hours)
        days.append(perf/1000)
        return np.array(days)

    def render():
        pass
