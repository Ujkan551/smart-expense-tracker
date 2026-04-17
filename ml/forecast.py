from ml.model import predict_month_end

def get_forecast(user_id, budget=10000):
    predicted_total, spent_so_far, predictions = predict_month_end(user_id)

    alert = predicted_total > budget

    return {
        'predicted': float(round(predicted_total, 2)),
        'spent_so_far': float(round(spent_so_far, 2)),
        'budget': budget,
        'alert': alert,
        'predictions': [float(p) for p in predictions]
    }