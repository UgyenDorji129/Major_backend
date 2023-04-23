import joblib
import numpy as np

def predict(data):
    x =np.array(data).reshape(-1, 87)
    print(x)
    rfc_loaded = joblib.load('model/model.joblib')
    y_pred = rfc_loaded.predict(x)
    return y_pred