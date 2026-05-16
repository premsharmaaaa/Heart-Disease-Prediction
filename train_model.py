import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ======================================
# LOAD DATASET
# ======================================

df = pd.read_csv("dataset/heart.csv", encoding='latin1')

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# ======================================
# FEATURES & TARGET
# ======================================

# ======================================
# DROP UNNECESSARY TEXT COLUMNS
# ======================================

df = df.drop([
    "full_name",
    "country",
    "state",
    "gender",
    "first_name",
    "last_name",
    "hospital",
    "treatment",
    "treatment_date"
], axis=1)

# ======================================
# FEATURES & TARGET
# ======================================

X = df.drop("heart_disease", axis=1)
y = df["heart_disease"]

# ======================================
# TRAIN TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ======================================
# FEATURE SCALING
# ======================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, "models/scaler.pkl")

# ======================================
# MACHINE LEARNING MODELS
# ======================================

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True),
    "Naive Bayes": GaussianNB(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "AdaBoost": AdaBoostClassifier(),
    "XGBoost": XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss'
    )
}

# ======================================
# TRAINING & EVALUATION
# ======================================

best_accuracy = 0
best_model = None
best_model_name = ""

results = []

for name, model in models.items():

    print(f"\n==============================")
    print(f"Training: {name}")
    print(f"==============================")

    # Train model
    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    results.append([name, accuracy])

    print(f"\nAccuracy: {accuracy:.4f}")

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(5, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues'
    )

    plt.title(f"{name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.show()

    # Save best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# ======================================
# SAVE BEST MODEL
# ======================================

joblib.dump(best_model, "models/best_model.pkl")

# ======================================
# RESULTS COMPARISON
# ======================================

results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy"]
)

print("\n==============================")
print("FINAL RESULTS")
print("==============================")

print(results_df)

# ======================================
# ACCURACY GRAPH
# ======================================

plt.figure(figsize=(12, 6))

sns.barplot(
    x="Model",
    y="Accuracy",
    data=results_df
)

plt.xticks(rotation=45)

plt.title("Machine Learning Algorithm Comparison")

plt.show()

# ======================================
# BEST MODEL
# ======================================

print("\n==============================")
print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy:.4f}")
print("==============================")