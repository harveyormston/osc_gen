import matplotlib.pyplot as plt

def plot_wave(wave):
    
    plt.plot(wave.values)
    plt.show()
    plt.gcf().clear()
    
def plot_wavetable(wavetable):
    
    slots = wavetable.slots
    signals = [slot.wave.values for slot in slots]
    for s in signals:
        plt.plot(s)
    plt.show()
    plt.gcf().clear()
