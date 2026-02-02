import numpy as np
from sklearn.linear_model import LinearRegression

model = LinearRegression()

# Dummy training data (industry-style simulation)
X_train = np.array([
    [55, 150, 1, 800, 2.0],
    [40, 90, 0, 300, 4.0],
    [60, 160, 1, 1200, 1.5],
    [30, 70, 0, 200, 5.0]
])

y_train = np.array([85, 40, 90, 35])

model.fit(X_train, y_train)

def ml_seo_score(features):
    return int(model.predict([features])[0])
