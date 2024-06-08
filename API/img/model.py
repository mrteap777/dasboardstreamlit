from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df_breed = pd.read_csv('breed.csv')
classes = df_breed['breed'].values

model = load_model(r'dog_breed_classifier.h5')


def predict_class(file):
    img = load_img(file,target_size=(128,128))
    img_arr = img_to_array(img)
    img_arr = img_arr/255
    arr = np.array([img_arr])
    prediction = model.predict(arr)
    decoded_labels = classes[np.argmax(prediction)]
    return decoded_labels
