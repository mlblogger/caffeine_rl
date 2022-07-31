import matplotlib.pyplot as plt
import caffeine

if __name__ == "__main__":
    caff = caffeine.UMP()

    ts = [ i/10 for i in range(720) ]
    sleep_times = { 0 : 20.0, 1 : 23, 2 : 23, 3 : 22, 4: 21 } 
    caffeine_doses = { 0 : [ 0.05, 0.05, 0.05 ] , 1 : [ 0.1 ,0.05 ], 2 : [ 0.2, 0.05 ], 3 : [ 0.1, 0.2 ], 4 : 0.2 }
    caffeine_times = { 0 : [ 4.5, 8, 9 ], 1 : [ 5.5, 10 ], 2 : [ 2, 5 ], 3 : [ 1, 3], 4 : 4.9 }
    
    wakec = []
    wakef = []
    sleep = []
    sub = 0
    day = 0
    for t in ts:
        caff.sleep_time = sleep_times[int(t/24)]
        day = int(t/24)
        t = t % 24
        if t == 0.0:
            caff.reset_start_day()
        for i,dt in enumerate(caffeine_times[day]):
            if t == dt:
                dose = caffeine_doses[day][i]
                caff.caffeine_dose_update(dose,t)
        print('Sleep Time ', caff.sleep_time)
        
        if t < caff.sleep_time :
            mode = 'wake'
            cf, wc = caff.caffeine_performance(t,mode)
            wakec.append(cf)
            wakef.append(wc)
        else:
            mode = 'sleep'
            value = caff.caffeine_free_performance(t,mode)
            wakec.append(float('nan'))
            wakef.append(float('nan'))
    
    values = wakec
    i = [ x/10 for x in list(range(len(values))) ]
    plt.plot(i,values,label="MRT without Caffeine")
    values = wakef
    i = [ x/10 for x in list(range(len(values))) ]
    plt.plot(i,values,label="MRT with Caffeine")
    plt.title("Mean Response Time")
    plt.xlabel("Time in Hours")
    plt.ylabel("Mean Response Time (MRT) ( in ms)")
    plt.arrow(4.5,0,0,40,width = 0.2,head_length=10,color='red')
    plt.arrow(8,0,0,40,width = 0.2,head_length=10,color='red')
    plt.arrow(9,0,0,40,width = 0.2,head_length=10, label='Caffeine Dose',color='red')
    plt.arrow(5.5 + 24,0,0,40,width = 0.2,head_length=10,color='red')
    plt.arrow(10 + 24,0,0,40,width = 0.2,head_length=10,color='red')
    plt.arrow(2 + 48,0,0,40,width = 0.2,head_length=10,color='red')
    plt.arrow(5 + 48,0,0,40,width = 0.2,head_length=10,color='red')
    plt.axvspan(20,24,color='cadetblue',label='Sleep')
    plt.axvspan(23+24,24+24,color='cadetblue')
    plt.axvspan(23+48,24+48,color='cadetblue')
    plt.legend()
    plt.show()
