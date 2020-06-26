import os
import numpy as np

import mne
import  matplotlib as plt
print(__doc__)

# load data

data ="/home/naty/Documents/Maestria/Dados/00000492/00000492_s003_t004.edf"
raw = mne.io.read_raw_edf(data)
print(raw)
print(raw.info)

# ---- Shown frequencies below 50Hz
#raw.plot_psd(fmax=50)

# ----- Shown eeg test
#raw.plot(duration=5, n_channels=31)
#plt.pyplot.show()


events = mne.find_events(raw)
print(events[:5])  # show the first 5
