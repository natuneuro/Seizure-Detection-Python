import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import mne
from Functions import load, network, processing
from sklearn.metrics import precision_recall_curve


def plot_loss_curve(loss1, val_loss1):
    plt.rcParams["font.family"] = "cmr10"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure()
    epoch = np.arange(1, 21, step=1)
    plt.plot(epoch, loss1, 'o-', color='#46bdc6')
    plt.plot(epoch, val_loss1, '*-', color='#ff6d01')
    # plt.title('\\textb{Loss Curve}', fontsize=16)
    plt.ylabel('Loss', fontsize=13)
    plt.xlabel('Epoch', fontsize=13)
    plt.xticks(np.arange(0, 21, step=2))
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()


def plot_acc_curve(acc, val_acc):
    plt.rcParams["font.family"] = "cmr10"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure()
    epoch = np.arange(1, 21, step=1)
    plt.plot(epoch, acc, 'o-', color='#46bdc6')
    plt.plot(epoch, val_acc, '*-', color='#ff6d01')
    # plt.title('Accuracy Curve', fontsize=16, fontweight='bold')
    plt.ylabel('Accuracy', fontsize=13)
    plt.xlabel('Epoch', fontsize=13)
    plt.xticks(np.arange(0, 21, step=2))
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def plot_predict(t, event_vec, predictions):
    plt.rcParams["font.family"] = "cmr10"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure()
    time = t[60:]
    predictions = np.array(predictions)
    plt.plot(time, event_vec, 'bs', markersize=7)
    plt.plot(time, predictions, 'r.', markersize=2)
    #plt.ylabel('Epilepsy Detection', fontsize=13)
    plt.xlabel('Time [s]', fontsize=13)
    plt.yticks(np.arange(0, 1.5, 0.5), ('Seizure-free', '', 'Seizure'))
    plt.legend(['True event', 'Predicted event'], loc='right')
    print("---------------------------- Salvando IMAGE --------------------")
    plt.savefig("Prediction.png")
    print("---------------------------- Salva IMAGE --------------------")
    #plt.show()


def plot_precision_recall_curve():
    plt.rcParams["font.family"] = "cmr10"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.figure()


def plot_matrix_3d(Input_net):
    print("1:7")
    plt.figure(figsize=(5, 5))
    plt.imshow(Input_net[305, range(2, 14, 1), :, 0],
               extent=[0, 21, 0, 256],
               aspect='auto',
               interpolation='nearest')

    print("8:30")
    plt.figure(figsize=(5, 5))
    plt.imshow(Input_net[305, range(16, 60, 1), :, 1],
               extent=[0, 21, 0, 256],
               aspect='auto',
               interpolation='nearest')

    print("31:100")
    plt.figure(figsize=(5, 5))
    plt.imshow(Input_net[305, range(62, 102, 1), :, 2],
               extent=[0, 21, 0, 256],
               aspect='auto',
               interpolation='nearest')
