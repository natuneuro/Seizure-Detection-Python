import numpy as np
import tensorflow as tf

from Modulos import ConfusionMatrix, CriaImagen, ProcessamentoDoSinal, LeituraArquivos, \
    AssociaTrechoEvento, LeituraEventos
from Classes import Evento, SinalEEG


def Image_processing(sinal_eeg: SinalEEG, eventos: Evento ):

    fs = sinal_eeg.frequencia_de_amostragem

    sinal_delta_theta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([1, 7])
    sinal_alpha_beta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([8, 30])
    sinal_gama = sinal_eeg.decomporSinalEmFaixaDeFrequencia([31, 100])

    delta_theta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_delta_theta, fs)
    alpha_beta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_alpha_beta, fs)
    gama_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_gama, fs)

    AssociaTrechoEvento.associa_trecho_evento(delta_theta_dividido, eventos)
    AssociaTrechoEvento.associa_trecho_evento(alpha_beta_dividido, eventos)
    AssociaTrechoEvento.associa_trecho_evento(gama_dividido, eventos)

    dados = CriaImagen.cria_imagens_saidas(
        gama_dividido, delta_theta_dividido, alpha_beta_dividido
    )

    fft_imagens = []

    for i in range(0, len(dados[0])):
        fft = np.fft.fftn(dados[0][i])
        # fft = np.log(np.abs(np.fft.fftshift(fft) ** 2))
        fft = np.abs(np.fft.fftshift(fft))
        img_fft = tf.keras.preprocessing.image.array_to_img(fft)
        array_fft = tf.keras.preprocessing.image.img_to_array(img_fft)
        array_fft = array_fft * (1.0 / 255)
        fft_imagens.append(array_fft)

    fft_imagens = np.array(fft_imagens)
    return fft_imagens, dados