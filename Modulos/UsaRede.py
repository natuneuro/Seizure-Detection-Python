import sklearn.model_selection
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from Classes import ImagemEntrada


def treina_rede(model, entradas: ImagemEntrada, saidas):
    # tf.keras.utils.normalize(entradas)

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        entradas, saidas, test_size=0.3
    )

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
def classifica_dados(model, entradas: ImagemEntrada, saidas):
    # tf.keras.utils.normalize(entradas)

    predictions = (model.predict(entradas, batch_size=10, verbose=1) > 0.5).astype(
        "int32"
    )

    cm = confusion_matrix(saidas, predictions)

    return cm

# para usar solo con .edf
def classifica_sem_saidas(model, entradas: ImagemEntrada):
    
    predictions = (model.predict(entradas, batch_size=10, verbose=0) > 0.5).astype(
        "int32"
    )

    return predictions
