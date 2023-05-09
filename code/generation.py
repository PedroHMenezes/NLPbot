from keras.layers import Input, Dense, Activation, TimeDistributed, Softmax, TextVectorization, Reshape, RepeatVector, Conv1D, Bidirectional, AveragePooling1D, UpSampling1D, Embedding, Concatenate, GlobalAveragePooling1D, LSTM, Multiply
from keras.models import Model
import tensorflow as tf
import keras
import numpy as np
import os
import json

def predict_word(seq_len, latent_dim, vocab_size):
    input_layer = Input(shape=(seq_len-1,))
    x = input_layer
    x = Embedding(vocab_size, latent_dim, name='embedding', mask_zero=True)(x)
    x = LSTM(latent_dim, kernel_initializer='glorot_uniform')(x)
    latent_rep = x
    x = Dense(vocab_size)(x)
    x = Softmax()(x)
    return Model(input_layer, x), Model(input_layer, latent_rep)

def colhe_texto():
    doc_frases = []
    score = []
    folder_path = '../links'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(f"{folder_path}/{filename}", 'r+') as f:
                dic_file = dict(json.load(f))
                for indice, values in dic_file.items():
                    doc_frases.append(values['text'])
                    
    return doc_frases

def predizer(entrada, numero_de_predicoes, modelo, vectorize_layer):
    frase = entrada
    contexto = frase # Contexto deslizante
    for n in range(numero_de_predicoes):
        pred = modelo.predict(vectorize_layer([contexto])[:,:-1])

        # Nao repetir palavras
        tentando = True
        while tentando:

            # Selecionar de k-best
            aleatorio = tf.random.uniform(shape=[1])
            candidatos = tf.math.top_k(pred, k=5).indices[0,:]
            idx = np.random.choice(candidatos.numpy())
            word = vectorize_layer.get_vocabulary()[idx]
            if word in frase.split():
                pred[0][idx] = 0
            else:
                tentando = False
                
        frase = frase + " " + word
        contexto = contexto + " " + word
        contexto = ' '.join(contexto.split()[1:])
        print(word)
    return frase

def retorna_resultado(entrada):
    vectorize_layer = TextVectorization(max_tokens=5000, output_sequence_length=10)
    vectorize_layer.adapt(colhe_texto())

    predictor, latent = predict_word(10, 15, 5000)
    opt = keras.optimizers.SGD(learning_rate=1, momentum=0.9)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(
        ignore_class=1,
        name="sparse_categorical_crossentropy",
    )

    predictor.compile(loss=loss_fn, optimizer=opt, metrics=["accuracy"])

    frase = predizer(entrada, 10, predictor, vectorize_layer)

    return frase