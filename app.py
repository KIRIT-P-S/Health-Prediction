from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("heart.csv")

# Split the data into features and target
X = df.drop(columns="target")
y = df["target"]

# Train a Random Forest Classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

@app.route('/')
def home():
    return render_template('index.html')  # Serves the HTML form

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive input data from the frontend
        input_data = request.get_json()

        # Convert input data into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Make the prediction
        prediction = rf.predict(input_df)

        # Return the prediction result
        response = {"prediction": int(prediction[0])}
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
