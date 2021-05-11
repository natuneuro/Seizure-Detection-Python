import math
import numpy as np
from scipy.signal import butter, filtfilt, stft
from Classes import ImagemEntrada, SinalDividido
from Modulos import VerificaConv


def butter_bandstop_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    i, u = butter(order, [low, high], btype='bandstop')
    x = filtfilt(i, u, data)
    return x

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


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

def STFT(input_signal,fs):
    f, t, Zxx = stft(input_signal, fs, nperseg=512) # STFT of signal
    Zmod = np.abs(Zxx)  # modul of 3D matrix Zxx
    Zmax = np.max(Zmod) # Maximum value of modul of Zxx 
    Znorm = (Zmod * 1)/ Zmax #normalize the 3D matrix Zxx
    Ztrain=Znorm.T           #Transposta da Znorm
    return f, t, Ztrain

def EventVector(eventos,total_time):

    quantidade_trechos = total_time
    lista_tipos_conv = ["cpsz", "gnsz", "absz", "tnsz", "cnsz", "tcsz","fnsz","spsz"]

    event_vec=[0]*len(quantidade_trechos)
    for i in range(0, len(quantidade_trechos)):
        for k in range(0,len(eventos)):
            inicio=round(eventos[k].inicio,0)
            fim=round(eventos[k].fim,0)
            if i>=inicio and i<=fim :
                for j in range(0,len(lista_tipos_conv)):
                    if eventos[k].tipo == lista_tipos_conv[j] :
                        event_vec[i]=1

                

    return event_vec