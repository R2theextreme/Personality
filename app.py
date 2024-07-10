import json  # Add this import statement
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import firebase_admin
from firebase_admin import credentials, firestore
app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load('static/model/advanced_personality_model.joblib')
vectorizer = joblib.load('static/model/advanced_vectorizer.joblib')

def is_valid_syntax(code, language):
    if language == 'Python':
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    code_snippet = None
    error_message = None
    if request.method == 'POST':
        code_snippet = request.form['code_snippet']
        language = request.form.get('language')
        if code_snippet:
            lines = code_snippet.strip().split('\n')
            if len(lines) < 15:
                error_message = "The code snippet must be at least 15 lines long."
            elif not is_valid_syntax(code_snippet, language):
                error_message = f"The provided code snippet is not valid {language} syntax."
            else:
                try:
                    # Transform the input snippet using the vectorizer
                    input_vector = vectorizer.transform([code_snippet])
                    # Predict the personality
                    prediction = model.predict(input_vector)[0]
                except Exception as e:
                    error_message = str(e)
    
    return render_template('index.html', prediction=prediction, code_snippet=code_snippet, error_message=error_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/find_language', methods=['GET', 'POST'])
def find_language():
    if request.method == 'POST':
        selected_tags = json.loads(request.form['selectedTags'])
        if len(selected_tags) != 10:
            return render_template('find_language.html', message="Please select exactly 10 tags.")
        
        language_recommendations = {
            "Adventurous": ["Python", "JavaScript"],
            "Analytical": ["R", "MATLAB"],
            "Creative": ["Ruby", "Swift"],
            "Detail-Oriented": ["Java", "C++"],
            "Innovative": ["Go", "Rust"],
            "Patient": ["Perl", "Haskell"],
            "Empathetic": ["PHP", "TypeScript"],
            "Leader": ["Kotlin", "Scala"],
            "Spontaneous": ["Elixir", "Clojure"],
            "Team Player": ["Dart", "Julia"]
        }
        languages = []
        for tag in selected_tags:
            if tag in language_recommendations:
                languages.extend(language_recommendations[tag])
        languages = list(set(languages))[:5]
        return render_template('find_language.html', languages=languages)
    return render_template('find_language.html', languages=None)

if __name__ == '__main__':
    app.run(debug=True)
