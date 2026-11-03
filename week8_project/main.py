
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
)


#  CREATE SYNTHETIC TRANSACTION DATASET

rng = np.random.default_rng(42)
total_transactions = 2000

df = pd.DataFrame({
    "transaction_id": range(1, total_transactions + 1),
    "amount": rng.integers(100, 100000, total_transactions),
    "hour": rng.integers(0, 24, total_transactions),
    "transactions_in_24h": rng.integers(1, 30, total_transactions)
})

# Generate sample risk labels with overlapping patterns
amount_score = df["amount"] / 100000
frequency_score = df["transactions_in_24h"] / 30

night_score = df["hour"].isin(
    [0, 1, 2, 3, 4, 5]
).astype(int)

risk_score = (
    -3.0
    + 1.5 * amount_score
    + 1.7 * frequency_score
    + 0.6 * night_score
)

risk_probability = 1 / (1 + np.exp(-risk_score))

df["risk"] = np.where(
    rng.random(total_transactions) < risk_probability,
    "RISKY",
    "NORMAL"
)

df.to_csv("transactions.csv", index=False)

print("\n========== DATASET ==========")
print(df.head())

print("\nRisk Distribution:")
print(df["risk"].value_counts())


#  SELECT FEATURES AND LABELS

X = df[[
    "amount",
    "hour",
    "transactions_in_24h"
]]

y = df["risk"]

print("\nFeatures:")
print(X.head())

print("\nLabels:")
print(y.head())


#  SPLIT DATASET
# 70% training, 15% validation, 15% testing

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    stratify=y,
    random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42
)

print("\n========== DATA SPLIT ==========")
print("Training:", len(X_train))
print("Validation:", len(X_val))
print("Testing:", len(X_test))


#  TRAIN AND VALIDATE MODEL

depth_options = [2, 3, 4, 5, 6, 8, 10]

train_scores = []
val_scores = []

best_model = None
best_depth = None
best_val_f1 = -1

for depth in depth_options:

    model = DecisionTreeClassifier(
        max_depth=depth,
        min_samples_leaf=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    val_predictions = model.predict(X_val)

    train_accuracy = accuracy_score(
        y_train, train_predictions
    )

    val_accuracy = accuracy_score(
        y_val, val_predictions
    )

    val_f1 = f1_score(
        y_val,
        val_predictions,
        pos_label="RISKY",
        zero_division=0
    )

    train_scores.append(train_accuracy)
    val_scores.append(val_accuracy)

    print(
        f"Depth {depth}: "
        f"Train={train_accuracy:.3f}, "
        f"Validation={val_accuracy:.3f}, "
        f"Risky F1={val_f1:.3f}"
    )

    if val_f1 > best_val_f1:
        best_val_f1 = val_f1
        best_depth = depth
        best_model = model

print("\nBest Tree Depth:", best_depth)
print("Best Validation F1:", round(best_val_f1, 3))


#  EVALUATE TRAINING VS TESTING

train_predictions = best_model.predict(X_train)
test_predictions = best_model.predict(X_test)

train_accuracy = accuracy_score(
    y_train, train_predictions
)

test_accuracy = accuracy_score(
    y_test, test_predictions
)

precision = precision_score(
    y_test,
    test_predictions,
    pos_label="RISKY",
    zero_division=0
)

recall = recall_score(
    y_test,
    test_predictions,
    pos_label="RISKY",
    zero_division=0
)

f1 = f1_score(
    y_test,
    test_predictions,
    pos_label="RISKY",
    zero_division=0
)

print("\n========== MODEL EVALUATION ==========")
print("Training Accuracy:", round(train_accuracy, 3))
print("Testing Accuracy:", round(test_accuracy, 3))
print("Precision:", round(precision, 3))
print("Recall:", round(recall, 3))
print("F1 Score:", round(f1, 3))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        test_predictions,
        labels=["NORMAL", "RISKY"],
        zero_division=0
    )
)


#  TRAINING VS VALIDATION GRAPH

plt.figure(figsize=(8, 5))

plt.plot(
    depth_options,
    train_scores,
    marker="o",
    label="Training Accuracy"
)

plt.plot(
    depth_options,
    val_scores,
    marker="o",
    label="Validation Accuracy"
)

plt.xlabel("Decision Tree Depth")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("training_validation.png")
plt.show()


#  CONFUSION MATRIX

ConfusionMatrixDisplay.from_predictions(
    y_test,
    test_predictions,
    labels=["NORMAL", "RISKY"],
    cmap="Blues"
)

plt.title("Financial Transaction Risk Classification")
plt.tight_layout()

plt.savefig("confusion_matrix.png")
plt.show()


#  PREDICT A NEW TRANSACTION

new_transaction = pd.DataFrame({
    "amount": [75000],
    "hour": [2],
    "transactions_in_24h": [20]
})

prediction = best_model.predict(new_transaction)

risk_index = list(best_model.classes_).index("RISKY")

risk_probability_prediction = best_model.predict_proba(
    new_transaction
)[0][risk_index]

print("\n========== NEW TRANSACTION ==========")
print(new_transaction)

print("\nPredicted Classification:", prediction[0])

print(
    "Estimated Risk Probability:",
    round(risk_probability_prediction * 100, 2),
    "%"
)
