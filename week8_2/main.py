
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


#  CREATE FINANCIAL TRANSACTION DATASET


np.random.seed(42)

total_transactions = 500

data = {
    "transaction_id": range(1, total_transactions + 1),

    "amount": np.random.randint(
        100, 100000, total_transactions
    ),

    "hour": np.random.randint(
        0, 24, total_transactions
    ),

    "transactions_in_24h": np.random.randint(
        1, 30, total_transactions
    )
}

df = pd.DataFrame(data)

# Create artificial risk labels for learning
# These are not real banking fraud-detection rules
df["risk"] = np.where(
    (df["amount"] > 50000) &
    (df["transactions_in_24h"] > 15),
    "RISKY",
    "NORMAL"
)

# Save dataset for inspection
df.to_csv("transactions.csv", index=False)

print("\nDataset:")
print(df.head())

print("\nRisk Distribution:")
print(df["risk"].value_counts())



# SELECT FEATURES


# Features are the inputs used for prediction
X = df[
    [
        "amount",
        "hour",
        "transactions_in_24h"
    ]
]



#  SELECT LABELS


# Label is the output the model learns to predict
y = df["risk"]


# SPLIT DATA


# 70% training, 15% validation, 15% testing
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

print("\nTraining records:", len(X_train))
print("Validation records:", len(X_val))
print("Testing records:", len(X_test))



#  TRAINING AND VALIDATION


# Try different tree depths to select a model
depth_options = [2, 3, 4, 5, 6]

best_model = None
best_depth = None
best_score = -1

training_scores = []
validation_scores = []

for depth in depth_options:

    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    val_predictions = model.predict(X_val)

    train_accuracy = accuracy_score(
        y_train,
        train_predictions
    )

    val_accuracy = accuracy_score(
        y_val,
        val_predictions
    )

    training_scores.append(train_accuracy)
    validation_scores.append(val_accuracy)

    print(
        f"Depth: {depth}, "
        f"Train Accuracy: {train_accuracy:.3f}, "
        f"Validation Accuracy: {val_accuracy:.3f}"
    )

    # Select the best model using validation data
    if val_accuracy > best_score:
        best_score = val_accuracy
        best_depth = depth
        best_model = model

print("\nBest Tree Depth:", best_depth)
print("Best Validation Accuracy:", round(best_score, 3))



# STEP 6: FINAL TESTING


# Test data was not used for training or selection
test_predictions = best_model.predict(X_test)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

print("\nFinal Test Accuracy:", round(test_accuracy, 3))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        test_predictions,
        labels=["NORMAL", "RISKY"],
        zero_division=0
    )
)



# GRAPH 1: TRAINING VS VALIDATION ACCURACY


plt.figure(figsize=(8, 5))

plt.plot(
    depth_options,
    training_scores,
    marker="o",
    label="Training Accuracy"
)

plt.plot(
    depth_options,
    validation_scores,
    marker="o",
    label="Validation Accuracy"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# GRAPH 2: CONFUSION MATRIX


matrix = confusion_matrix(
    y_test,
    test_predictions,
    labels=["NORMAL", "RISKY"]
)

display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=["NORMAL", "RISKY"]
)

display.plot()
plt.title("Transaction Risk Classification")
plt.tight_layout()
plt.show()



# STEP 7: PREDICT A NEW TRANSACTION


new_transaction = pd.DataFrame({
    "amount": [75000],
    "hour": [2],
    "transactions_in_24h": [20]
})

prediction = best_model.predict(new_transaction)

print("\nNew Transaction:")
print(new_transaction)

print("\nPredicted Risk:", prediction[0])
