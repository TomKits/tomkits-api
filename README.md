# **TOMKITS API**

TOMKITS API is a RESTful API built with Flask to manage user authentication and operations using JWT tokens. This guide provides the steps to set up, run, and use the API.

---

## **Requirements**
- **Python**: `3.10.11`
- **Dependencies**: Specified in `requirements.txt`

---

## **Setup Instructions**

Follow these steps to set up and run the application:

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>```

### **2. Create and Activate a Virtual Enviroment**
- Linux/macOS
```bash
python3 -m venv env
source env/bin/activate
```
- Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt

```

### **4. Set Enviroment Variable**
- Linux/macOS
```bash
export FLASK_APP=main.py
```
- Windows (Command Prompt)
```
set FLASK_APP=main.py
```
- Windows (PowerShell)
```
$env:FLASK_APP = "main.py"
```

### **5. Run the application**
```bash
flask run
```
