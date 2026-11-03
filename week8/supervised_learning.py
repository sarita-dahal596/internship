
import pandas as pd
from sklearn.linear_model import LinearRegression

# Training data: transactions and monthly spending
data = {
    "transactions": [5, 10, 15, 20, 25, 30],
    "spending": [500, 1000, 1500, 2000, 2500, 3000]
}

df = pd.DataFrame(data)

# Input (X) and target (y)
X = df[["transactions"]]
y = df["spending"]

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Predict spending for 18 transactions
new_customer = pd.DataFrame({
    "transactions": [18]
})

prediction = model.predict(new_customer)

print("Predicted monthly spending: NPR", prediction[0])
