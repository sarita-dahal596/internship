
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Customer data without predefined group labels
data = {
    "transactions": [2, 3, 5, 15, 18, 20, 35, 40, 45],
    "spending": [
        200, 300, 500,
        2500, 3000, 3500,
        8000, 9000, 10000
    ]
}

df = pd.DataFrame(data)

X = df[["transactions", "spending"]]

# Scale features before clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Automatically divide customers into 3 groups
model = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

df["cluster"] = model.fit_predict(X_scaled)

print(df)

# Visualize the customer groups
plt.scatter(
    df["transactions"],
    df["spending"],
    c=df["cluster"]
)

plt.xlabel("Number of Transactions")
plt.ylabel("Monthly Spending (NPR)")
plt.title("Customer Segmentation")
plt.show()
