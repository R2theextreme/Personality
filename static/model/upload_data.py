import random
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('codeaura-cbfbe-firebase-adminsdk-n70p3-2d51dede3d.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Example function to generate random code snippets
def generate_code_snippet(language, personality):
    snippets = {
        "Helper": [
            "# This function adds two numbers\ndef add(a, b):\n    return a + b",
            "# Comment about the function\ndef multiply(a, b):\n    result = a * b\n    return result",
        ],
        "Organiser": [
            "def divide(a, b):\n    if b == 0:\n        raise ValueError('Cannot divide by zero')\n    return a / b",
            "def calculate(a, b):\n    return (a + b) / 2",
        ],
        "Zenmaster": [
            "def subtract(a, b): return a - b",
            "def multiply(a, b): return a * b",
        ],
        "Leader": [
            "class Calculator:\n    def __init__(self):\n        self.result = 0\n\n    def add(self, a, b):\n        self.result = a + b\n        return self.result",
            "class Processor:\n    def process(self, data):\n        self.data = data\n        return self.data",
        ],
        "Adventurer": [
            "for i in range(10): print(i)",
            "while True:\n    print('Running...')\n    break",
        ]
    }
    return random.choice(snippets[personality])

# Define languages and personalities
languages = ["Python", "Java", "C++"]
personalities = ["Helper", "Organiser", "Zenmaster", "Leader", "Adventurer"]

# Generate and upload a large dataset
for i in range(1000):  # Adjust the range for more data
    language = random.choice(languages)
    personality = random.choice(personalities)
    code_snippet = generate_code_snippet(language, personality)
    
    data = {
        'language': language,
        'personality': personality,
        'code_snippet': code_snippet
    }
    
    db.collection('code_snippets').add(data)

print("Data upload complete!")
