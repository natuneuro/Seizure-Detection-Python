import math
import numpy as np
from scipy.signal import butter, filtfilt
from Classes import ImagemEntrada, SinalDividido

def signal_split(signal, freq):
    L = len(signal[0,0,:]) # length of input signal
    N = freq +1 # Number of samples per intervals 
    Num_int = math.floor(L/N) # Numbers of intervals

    ti = 1 # Initial time
    tf = int(N) # Final time

    windows = [] # windows of signal

    window = SinalDividido.SinalDividido(np.array(signal[:,:, (ti-1):(tf-1)]),0,N*(1/freq),)

    windows.append(window)

    for i in range(2, Num_int):
        ti = tf + 1
        tf = i * N

        if tf > L:
            window = SinalDividido.SinalDividido(
                np.array(signal[:,:, (ti - 1): (tf - 1)]),
                ti * (1 / freq),
                L * (1 / freq),
            )

            windows.append(window)
        else:
            window = SinalDividido.SinalDividido(
                np.array(signal[:,:, ( ti - 1): (tf - 1)]),
                ti * (1 / freq),
                tf * (1 / freq),
            )

            windows.append(window)

    return windows


