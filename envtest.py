import os
import sys
import gym
import umpenv
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    gym.envs.register(
        id='CaffeineEnv-v0',
        entry_point='umpenv:UMPEnv',
    )

    env = gym.make('CaffeineEnv-v0')

    env.reset()
    done = False

    actions = [ 0, 1, 2, 3 ]
    actions_prob = [ 0.95, 0.02, 0.02, 0.01 ]
    caffeine_total = 0.5

    logs = []
    while not done:
        act = np.random.choice(actions,p=actions_prob)
        obs,r,done,info = env.step(act)
        if not done:
            logs.append(info)
        print(obs,r,done,info)
    #{'time': 17.79999999999997, 'caff_perf': 179.39446267027643, 'caff_free_perf': 273.94831015679495, 'sleep_time': 18.8, 'stock': 0.30000000000000004}

    caff_perf = [ x['caff_perf'] for x in logs ]
    caff_free = [ x['caff_free_perf'] for x in logs ]
    caff_stock = [ x['stock'] for x in logs ]
    ii = [ x['time'] for x in logs ]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time in Hrs')
    ax1.set_ylabel('MRT (ms)')
    ax1.plot(ii, caff_perf, label='Caffeine MRT')
    ax1.plot(ii, caff_free, label='Caffeine Free MRT')
    ax1.tick_params(axis='y')#, labelcolor=color)
    ax1.legend()
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:green'
    ax2.set_ylabel('Caffeine Stock (gm)')#, color=color)  # we already handled the x-label with ax1
    ax2.plot(ii, caff_stock,color='tab:green',label='Caffeine Stock')#, color=color)
    ax2.tick_params(axis='y', labelcolor='tab:green')
    ax2.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()
