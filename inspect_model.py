import joblib

obj = joblib.load("model/ids_model.joblib")
print(type(obj))
print(obj)
