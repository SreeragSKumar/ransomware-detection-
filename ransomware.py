import os
import math
import pickle
from cryptography.fernet import Fernet
from sklearn.ensemble import RandomForestClassifier

# =========================
# 📁 Setup folders
# =========================
DATASET_DIR = "dataset"
BENIGN_DIR = os.path.join(DATASET_DIR, "benign")
RANSOM_DIR = os.path.join(DATASET_DIR, "ransomware")
MODEL_PATH = "model.pkl"

os.makedirs(BENIGN_DIR, exist_ok=True)
os.makedirs(RANSOM_DIR, exist_ok=True)

# =========================
# 🧪 Step 1: Generate Benign Files
# =========================
def generate_benign_files():
    for i in range(20):
        file_path = os.path.join(BENIGN_DIR, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write("This is a normal harmless file.\n" * 50)

# =========================
# 🔴 Step 2: Generate Fake Ransomware Files
# =========================
def generate_ransomware_files():
    key = Fernet.generate_key()
    cipher = Fernet(key)

    for i in range(20):
        original_data = ("Sensitive data " * 50).encode()

        encrypted_data = cipher.encrypt(original_data)

        file_path = os.path.join(RANSOM_DIR, f"ransom_{i}.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)

# =========================
# 🧠 Feature Extraction
# =========================
def calculate_entropy(data):
    if len(data) == 0:
        return 0

    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1

    entropy = 0
    for count in byte_counts:
        if count == 0:
            continue
        p = count / len(data)
        entropy -= p * math.log2(p)

    return entropy

def extract_features(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        file_size = len(data)
        entropy = calculate_entropy(data)

        return [file_size, entropy]
    except:
        return [0, 0]

# =========================
# 📊 Load Dataset
# =========================
def load_data():
    X = []
    y = []

    # Benign = 0
    for file in os.listdir(BENIGN_DIR):
        path = os.path.join(BENIGN_DIR, file)
        X.append(extract_features(path))
        y.append(0)

    # Ransomware = 1
    for file in os.listdir(RANSOM_DIR):
        path = os.path.join(RANSOM_DIR, file)
        X.append(extract_features(path))
        y.append(1)

    return X, y

# =========================
# 🏋️ Train Model
# =========================
def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("[✔] Model trained and saved!")

# =========================
# 🔍 Detection
# =========================
def detect_file(file_path):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    features = extract_features(file_path)
    prediction = model.predict([features])[0]

    print("\n--- Detection Result ---")
    print(f"File: {file_path}")
    print(f"Size: {features[0]} bytes")
    print(f"Entropy: {features[1]:.4f}")

    if prediction == 1:
        print("⚠️ RANSOMWARE DETECTED")
    else:
        print("✅ BENIGN FILE")

# =========================
# 🚀 Main Execution
# =========================
if __name__ == "__main__":
    print("[1] Generating dataset...")
    generate_benign_files()
    generate_ransomware_files()

    print("[2] Loading data...")
    X, y = load_data()

    print("[3] Training model...")
    train_model(X, y)

    print("[4] Testing detection...")

    # Test on a benign file
    test_file = os.path.join(BENIGN_DIR, "file_0.txt")
    detect_file(test_file)

    # Test on ransomware file
    test_file = os.path.join(RANSOM_DIR, "ransom_0.enc")
    detect_file(test_file)