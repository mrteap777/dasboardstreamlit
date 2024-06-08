from flask import Flask, jsonify, request #pip install flask
from keras.models import load_model
import joblib
from io import StringIO
import pandas as pd



app = Flask(__name__)

model = load_model(r'C:\projects\API\tabular\model\my_model.keras')
scaler = joblib.load(r'C:\projects\API\tabular\model\scaler.joblib')
features = pd.read_csv(r'C:\projects\API\tabular\model\features.csv')

#делаем срез по столбцам и предобработку
def data_prepare(json_obj):
    df_test = pd.read_json(StringIO(json_obj))
    df_test=df_test[features['Feature'].values]
    df_test["sex"] = df_test["sex"].map({'Female': 0, 'Male': 1}).astype(int)
    df_test=df_test[:5]
    return df_test



@app.route('/get_gammagpt', methods=['POST'])
def predict():
    new_data = request.get_json()
    df = data_prepare(new_data)
    
    #стандартизация
    df_scal = scaler.transform(df)
    df['prediction'] = model.predict(df_scal)
    return jsonify(df.to_json())




if __name__ == '__main__':
    app.run(debug=True)