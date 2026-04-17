import numpy as np
from sklearn.linear_model import LinearRegression
from ml.preprocess import preprocess

def predict_month_end(user_id):
    daily, spent_so_far = preprocess(user_id)

    if daily is None:
        return 0, 0, []

    X = daily[['day']].values
    y = daily['total'].values

    model = LinearRegression()
    model.fit(X, y)

    all_days = np.array(range(1, 31)).reshape(-1, 1)
    predictions = model.predict(all_days)

    predicted_total = round(sum(predictions), 2)

    if predicted_total < 0:
        predicted_total = spent_so_far

    return predicted_total, spent_so_far, predictions.tolist()