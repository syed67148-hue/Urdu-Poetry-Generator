import tensorflow as tf
import pickle
import numpy as np

MODEL_PATH = "models/urdu_lstm_model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"

model = tf.keras.models.load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

MAX_LEN = 12


def sample_with_temperature(preds, temperature=0.8):

    preds = np.asarray(preds).astype("float64")

    preds = np.log(preds + 1e-8) / temperature

    exp_preds = np.exp(preds)

    preds = exp_preds / np.sum(exp_preds)

    return np.random.choice(len(preds), p=preds)


def generate_poetry(seed_text, next_words=20):

    result = seed_text

    for _ in range(next_words):

        token_list = tokenizer.texts_to_sequences([result])[0]

        token_list = tf.keras.preprocessing.sequence.pad_sequences(
            [token_list],
            maxlen=MAX_LEN - 1,
            padding="pre"
        )

        prediction = model.predict(token_list, verbose=0)[0]

        predicted_index = sample_with_temperature(
            prediction,
            temperature=0.8
        )

        output_word = ""

        for word, index in tokenizer.word_index.items():

            if index == predicted_index:
                output_word = word
                break

        if output_word == "":
            break

        result += " " + output_word

    return result