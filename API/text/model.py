import pickle
from keras.models import load_model
import pymorphy2
import re
from nltk.tokenize import word_tokenize
from keras.utils import pad_sequences


enc_file = open(r'model\encoder.pickle','rb')
token_file = open(r'model\tokenizer.pickle','rb')
encoder = pickle.load(enc_file)
tokenizer = pickle.load(token_file)
model = load_model(r'model\model.h5')

MAX_LEN=100

morph=pymorphy2.MorphAnalyzer()

def normalize_text(text):
    s1 = re.sub(r'[^\w\s]+|[\d]+', r'',text).strip()
    s1 = s1.lower()
    s1 = word_tokenize(s1)
    words=[]
    for i in s1:
        pv = morph.parse(i)
        words.append(pv[0].normal_form)
    sentence=' '.join(words)
    return sentence


def predict_class(text):
    text = normalize_text(text)
    vector = tokenizer.texts_to_sequences([text])
    vector_x = pad_sequences(vector, padding='post', maxlen=MAX_LEN)
    y_preds = model.predict(vector_x)
    y_class = y_preds.argmax(axis=-1)
    return encoder.inverse_transform(y_class)[0]