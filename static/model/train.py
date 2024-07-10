import firebase_admin
from firebase_admin import credentials, firestore
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import random

# Initialize Firebase Admin SDK
cred = credentials.Certificate('codeaura-cbfbe-firebase-adminsdk-n70p3-2d51dede3d.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to fetch data from Firestore
def fetch_data_from_firestore():
    snippets = []
    docs = db.collection('code_snippets').stream()
    for doc in docs:
        data = doc.to_dict()
        if 'code_snippet' in data and 'personality' in data:
            snippets.append((data['code_snippet'], data['personality']))
    return snippets

def add_code_snippet(snippet, personality):
    ref = db.collection('code_snippets')
    new_snippet = ref.add({
        'code_snippet': snippet,
        'personality': personality
    })

# Example code snippets
code_snippets = [
    # Organizer
    {
        'code': '''
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

result = add(5, 3)
print("Result:", result)
''',
        'personality': 'Organizer'
    },
    {
        'code': '''
def merge_sorted_lists(list1, list2):
    merged_list = []
    i = j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    merged_list.extend(list1[i:])
    merged_list.extend(list2[j:])
    
    return merged_list

sorted_list = merge_sorted_lists([1, 3, 5], [2, 4, 6])
print("Merged and sorted list:", sorted_list)
''',
        'personality': 'Organizer'
    },
    {
        'code': '''
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

print(quicksort([3,6,8,10,1,2,1]))
''',
        'personality': 'Organizer'
    },
    # Helper
    {
        'code': '''
# Here is the solution you were looking for
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))
''',
        'personality': 'Helper'
    },
    {
        'code': '''
# This function calculates the greatest common divisor (GCD) of two numbers
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Example usage:
x = 48
y = 18
print(f"The GCD of {x} and {y} is {gcd(x, y)}")
''',
        'personality': 'Helper'
    },
    {
        'code': '''
# This function checks if a number is prime
def is_prime(n):
    """Returns True if n is a prime number, otherwise False."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage:
num = 29
if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")
''',
        'personality': 'Helper'
    },
    # Leader
    {
        'code': '''
class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def move(self):
        print(f'{self.name} is moving at {self.speed} mph')

class Car(Vehicle):
    def __init__(self, name, speed, brand):
        super().__init__(name, speed)
        self.brand = brand

    def move(self):
        print(f'{self.brand} {self.name} is zooming at {self.speed} mph')

car = Car('Model S', 150, 'Tesla')
car.move()
''',
        'personality': 'Leader'
    },
    {
        'code': '''
class Logger:
    def log(self, message):
        raise NotImplementedError("Subclasses should implement this method")

class FileLogger(Logger):
    def log(self, message):
        with open("logfile.txt", "a") as f:
            f.write(message + "\n")

class DatabaseLogger(Logger):
    def log(self, message):
        # Imagine this logs to a database
        print(f"Logging to database: {message}")

def process_data(data, logger: Logger):
    logger.log("Processing data: " + data)

# Example usage
logger = FileLogger()
process_data("Sample data", logger)
''',
        'personality': 'Leader'
    },
    {
        'code': '''
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing credit card payment of {amount}")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of {amount}")

# Example usage
processor = CreditCardProcessor()
processor.process_payment(100)
''',
        'personality': 'Leader'
    },
    # Adventurer
    {
        'code': '''
# Check out this cool function to reverse a string
def reverse_string(s):
    return s[::-1]

print(reverse_string("Adventurer"))
''',
        'personality': 'Adventurer'
    },
    {
        'code': '''
# Adventurer
import random

def generate_random_password(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()?"
    password = "".join(random.choice(characters) for _ in range(length))
    return password

print(generate_random_password(12))
''',
        'personality': 'Adventurer'
    },
    {
        'code': '''
# Adventurer
import itertools

def find_combinations(items, n):
    return list(itertools.combinations(items, n))

items = ['apple', 'banana', 'cherry']
print(find_combinations(items, 2))
''',
        'personality': 'Adventurer'
    },
    # Zenmaster
    {
        'code': '''
# As long as it works, right?
def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]

print(is_palindrome("A man a plan a canal Panama"))
''',
        'personality': 'Zenmaster'
    },
    {
        'code': '''
# Zenmaster
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
''',
        'personality': 'Zenmaster'
    },
    {
        'code': '''
# Zenmaster
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
''',
        'personality': 'Zenmaster'
    }
]

# Add code snippets to Firebase
for snippet in code_snippets:
    add_code_snippet(snippet['code'], snippet['personality'])

print("Code snippets added to Firebase!")

# Fetch data
data = fetch_data_from_firestore()

# Shuffle the data to ensure randomness
random.shuffle(data)

# Extract code snippets and their corresponding personalities
code_snippets, personalities = zip(*data)

# Vectorize the code snippets
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(code_snippets)

# Train the model
model = MultinomialNB()
model.fit(X, personalities)

# Save the model and vectorizer
joblib.dump(model, 'static/model/advanced_personality_model.joblib')
joblib.dump(vectorizer, 'static/model/advanced_vectorizer.joblib')
