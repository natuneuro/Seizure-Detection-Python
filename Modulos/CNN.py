import sklearn.model_selection
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
from tensorflow.keras.layers import (
    Activation,
    Conv2D,
    Dense,
    Flatten,
    MaxPool2D,
    GlobalMaxPooling2D,
)
from tensorflow.keras.models import Sequential
from Modulos import ConfusionMatrix, UsaRede, CriaImagen, ProcessamentoDoSinal, LeituraArquivos, \
    AssociaTrechoEvento, LeituraEventos

# Signal
sinal_eeg = LeituraArquivos.ImportarSinalEEG()

eventos = LeituraEventos.importar_evento()

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
    fft = np.log(np.abs(np.fft.fftshift(fft) ** 2))
    img_fft = tf.keras.preprocessing.image.array_to_img(fft)
    array_fft = tf.keras.preprocessing.image.img_to_array(img_fft)
    array_fft = array_fft * (1.0 / 255)
    fft_imagens.append(array_fft)

fft_imagens = np.array(fft_imagens)




# CNN model

#def CNN_fit(imagens, saidas):

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(fft_imagens, dados[1], test_size=0.30)

model = Sequential()

model.add(Conv2D(128, kernel_size=(3, 3), strides=(1, 1), input_shape=(None, None, 3)))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1)))
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(GlobalMaxPooling2D())

model.add(Flatten())

model.add(Dense(64))
model.add(Activation("relu"))

model.add(Dense(32))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(
        tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss="binary_crossentropy",
        metrics=["accuracy"],)

model.fit(
        X_train,
        y_train,
        batch_size=32,
        validation_data=(X_test, y_test),
        epochs=20,
        verbose=1,)

predictions = (model.predict(fft_imagens, batch_size=32, verbose=1) > 0.5).astype("int32")



cm = confusion_matrix(saidas, predictions)

# ---- Classification Accuracy  ---------
TP = cm[1][1]
TN = cm[0][0]
FP = cm[1][0]
FN = cm[0][1]
# metrics
accuracy = (TP + TN) / (TP + FP + TN + FN)*100
sensitivity=TP/(TP+FN)*100
specificity= TN/(TN+FP)*100

print("acc: ", accuracy)
print("sens:", sensitivity)
print("spec:", specificity)

    # recall=TP/(TP+FN)
    # print("recall: ",recall)

    #precision = TP / (TP + FP)
    # print("precision: ", precision)

    # f_score=2*(precision*recall)/(precision+recall)
    # print("f-score: ", f_score)

    # cm_plot_labels = ["Normal", "Epilepsy"]
    # ConfusionMatrix.plot_confusion_matrix(cm, cm_plot_labels, title="Confusion Matrix")

    #return [accuracy, sensitivity, specificity,  cm]
