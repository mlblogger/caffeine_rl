import os
import sys
import numpy as np
import matplotlib.pyplot as plt

class UMP():
    def __init__(self,m=0):
        # Caffeine free model
        self.U = 18.4 if m else 497
        self.L = 0.0 if m else 140# lower asymptote
        self.tauw = 40.0 if m else 23
        self.taus = 2.1 if m else 4.0
        self.So = 0.5 if m else 176
        self.kappa = 3.3 if m else 75
        self.psi = 2.3 if m else 2.5
        self.taula = 7.0*24 if m else 7.0*24
        self.Lo = 0.0 if m else 140
        self.tau = 24

        # Caffeine Model
        self.Mo = 9.86 if m else 3.59
        self.ko = 0.49 if m else 0.49
        self.z = 1.63 if m else 1.63
        self.ka = 2.06 if m else 2.06
        self.ka = 3.21 if m else 3.21

        # a_i values for circadian
        self.a = np.array( [ 0.97, 0.22, 0.07, 0.03, 0.001 ])
        self.cd = ''
        self.ct = ''

        self.dose_time = 0.0
        self.dose = 0.0
        self.ts = 1/24

        self.sleep_time = 19.0
        self.So_sleep = self.So


    def reset_start_day(self):
        self.dose = 0.0
        self.dose_time = 0.0
        return

    def caffeine_decay_model(self,t):
        kdj = self.ko*np.exp(-self.z*self.dose)
        Dt = self.dose*np.exp(-kdj*((t - self.dose_time)*self.ts))
        return Dt

    def caffeine_dose_update(self,dose_new,t):
        decayed_dose = self.caffeine_decay_model(t)
        dose_updated = dose_new + decayed_dose
        self.dose = dose_updated
        self.dose_time = t
        return

    def caffeine_effect_gpd(self,t):
        if self.dose == 0.0 or t < self.dose_time:
            return 1
        else:
            Md = self.Mo*self.dose
            kdj = self.ko*np.exp(-self.z*self.dose)
            output = 1 + Md*np.exp(-kdj*(t-self.dose_time))
            print('Caffeine ', Md, kdj, output - 1)            
            return 1/(output)

    def caffeine_free_performance(self,t,mode):
        return self.homeostatic(t,mode) + self.kappa*self.circadian(t)

    def caffeine_performance(self,t,mode):
        pt = self.caffeine_free_performance(t,mode)
        gcd = self.caffeine_effect_gpd(t)
        print('Caffeine ', gcd)
        return pt, pt*gcd
    
    def circadian(self,t):
        inputs = np.array([ ((i*2*np.pi)/self.tau)*(t + self.psi) for i in\
                   range(1,6) ])
        outputs = np.sum(self.a*np.sin(inputs))
        return outputs

    def homeostatic(self,t,mode='wake'):
        if mode == 'wake':
            output = self.U - (self.U - self.So)*np.exp(-t/self.tauw)
            self.So_sleep = output
        elif mode == 'sleep':
            L = self.L_dynamics(t,mode)
            t = t - self.sleep_time
            output = -2*self.U + (2*self.U + self.So_sleep)*np.exp(-t/self.taus) +\
                (2*self.U + L)*(self.taula/(self.taula - self.taus)) * \
                (np.exp(-t/self.taula) - np.exp(-t/self.taus))
            self.So = output
        return output

    def L_dynamics(self,t,mode='wake'):
        if mode == 'wake':
            a = self.U - (self.U - self.Lo)*np.exp(-t/self.taula)
            L = max(a, -0.11*self.U)
        elif mode == 'sleep':
            t = t - (self.sleep_time + 24*int(t/24))
            a = -2*self.U + (2*self.U + self.Lo)*np.exp(-t/self.taula)
            L = max(a, -0.11*self.U)
        return L
