import matplotlib.pyplot as plt

def plot_wave(wave):
    
    plt.plot(wave.values)
    plt.show()
    plt.gcf().clear()
    
def plot_wavetable(wavetable):
    
    for s in [wave.values for wave in wavetable.waves]:
        plt.plot(s)
    plt.show()
    plt.gcf().clear()
