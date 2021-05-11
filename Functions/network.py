import tensorflow as tf
from tensorflow.keras.layers import (
    Activation,
    Conv2D,
    Dense,
    Flatten,
    MaxPool2D,
    GlobalMaxPooling2D,
    Dropout,
)
from tensorflow.keras.models import Sequential
import sklearn.model_selection
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, cohen_kappa_score


def Model():
    model = Sequential()

    model.add(
        # Conv2D(128, kernel_size=(3, 3), strides=(1, 1), input_shape=(None, None, 3)))
        Conv2D(128,
               kernel_size=(3, 3),
               strides=(1, 1),
               input_shape=(None, None, 3)))
    model.add(Activation("relu"))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1)))
    model.add(Activation("relu"))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(GlobalMaxPooling2D())

    model.add(Flatten())
    #antes 64
    model.add(Dense(64))
    model.add(Activation("relu"))
    #antes 32
    model.add(Dense(32))
    model.add(Activation("relu"))

    #antes 1
    model.add(Dense(1))
    model.add(Activation("sigmoid"))

    model.compile(
        tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss="binary_crossentropy",
        metrics=["accuracy", "mse"],
    )

    return model


def train(model, entradas, clases):
    # entrada: archivos eeg
    # clases : los eventos de convulsion
    # tf.keras.utils.normalize(entradas)

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        entradas, clases, test_size=0.3)
    #
    print(X_train.shape)
    print(X_test.shape)

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    #size_Xtrain=X_train.shape
    #size_Xtest=X_test.shape

    #X_train = X_train.reshape(size_Xtrain[0],size_Xtrain[1],size_Xtrain[2],1)
    #X_test = X_test.reshape(size_Xtest[0],size_Xtest[1],size_Xtest[2],1)
    print(X_train.shape)
    print(X_test.shape)
    #
    CNN_train = model.fit(
        X_train,
        y_train,
        batch_size=32,
        validation_data=(X_test, y_test),
        epochs=20,
        verbose=1,
    )

    print(CNN_train.history.keys())
    acc = CNN_train.history['accuracy']
    val_acc = CNN_train.history['val_accuracy']
    loss1 = CNN_train.history['loss']
    val_loss1 = CNN_train.history['val_loss']
    return [acc, val_acc, loss1, val_loss1], model


# usar con .tse classifica
def classify(model, entradas, clases):
    # tf.keras.utils.normalize(entradas)
    #size_entradas = entradas.shape
    #entradas = entradas.reshape(size_entradas[0],size_entradas[1],size_entradas[2],1)
    # predictions = (model.predict(entradas, batch_size=10, verbose=1) > 0.5).astype(
    #     "int32"
    # )
    predictions = (model.predict(entradas, batch_size=10, verbose=1) >
                   0.5).astype("int32")

    cm = confusion_matrix(clases, predictions)
    #-- metrics
    precision = precision_score(clases, predictions)
    recall = recall_score(clases, predictions)
    f1 = f1_score(clases, predictions)
    target_names = ["Seizure-free", "Seizure"]
    print(classification_report(clases, predictions,
                                target_names=target_names))
    return cm, predictions, precision, recall, f1


# para usar solo con .edf
def classifica_sem_saidas(model, entradas):

    predictions = (model.predict(entradas, batch_size=10, verbose=0) >
                   0.5).astype("int32")

    return predictions


def plot_confusion_matrix(cm,
                          classes,
                          normalize=False,
                          title="Confusion Matix",
                          cmap=plt.cm.Blues):

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized Confusion Matrix")
    else:
        print("\nConfusion Matrix")

    print(cm)

    thresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.savefig('../Resultado.png')
    #plt.show()


def train_test(model, entradas, clases):
    # tf.keras.utils.normalize(entradas)

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        entradas, clases, test_size=0.3)
    #
    print(X_train.shape)
    print(X_test.shape)

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    #size_Xtrain=X_train.shape
    #size_Xtest=X_test.shape

    #X_train = X_train.reshape(size_Xtrain[0],size_Xtrain[1],size_Xtrain[2],1)
    #X_test = X_test.reshape(size_Xtest[0],size_Xtest[1],size_Xtest[2],1)
    print(X_train.shape)
    print(X_test.shape)
    #
    CNN_train = model.fit(
        X_train,
        y_train,
        batch_size=32,
        validation_data=(X_test, y_test),
        epochs=20,
        verbose=1,
    )

    predictions = (model.predict(X_test, batch_size=32, verbose=1) >
                   0.5).astype("int32")

    cm = confusion_matrix(y_test, predictions)

    print(CNN_train.history.keys())
    acc = CNN_train.history['accuracy']
    val_acc = CNN_train.history['val_accuracy']
    loss1 = CNN_train.history['loss']
    val_loss1 = CNN_train.history['val_loss']
    return [acc, val_acc, loss1, val_loss1], model, cm