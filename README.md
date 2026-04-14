# 🔐 Secure Login System

A **robust and secure web-based authentication system** built using **Flask**, designed to protect user accounts from common vulnerabilities such as **SQL Injection**, **credential theft**, and **unauthorized access**.
The system combines **strong backend security** with a **modern glassmorphism UI**, delivering both **safety and premium user experience**.

## 🌟 Features

### 🔒 Advanced Security Implementation

* **Password Hashing**
  * Uses `bcrypt` for secure password storage
  * No plaintext passwords are stored

* **SQL Injection Protection**
  * All database queries use **parameterized statements**

* **Session Security**
  * Secure sessions using `os.urandom(24)`
  * Prevents session tampering and hijacking

* **Two-Factor Authentication (2FA)**
  * TOTP-based authentication using `pyotp`
  * Compatible with apps like:
    * Google Authenticator
    * Authy
  * QR-based setup using `qrcode` (SVG rendering)


## 📄 Application Pages

| Route         | Description              |
| ------------- | ------------------------ |
| `/register`   | Secure user registration |
| `/login`      | User authentication      |
| `/setup_2fa`  | QR-based 2FA setup       |
| `/verify_2fa` | Enter 6-digit TOTP       |
| `/dashboard`  | Protected user dashboard |
| `/logout`     | End session securely     |

---

## 🏗️ Tech Stack

### Backend
* **Python (Flask)**
* **SQLite**
* **bcrypt**
* **pyotp**
* **qrcode**

### Frontend

* HTML5
* CSS3 (Glassmorphism + Animations)
* Vanilla JavaScript

---

## 📂 Project Structure

```
secure_login_system/
│── app.py
│── database.py
│── requirements.txt
│── app.db
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── setup_2fa.html
│   ├── verify_2fa.html
│   ├── dashboard.html
│
├── static/
│   ├── css/
│   ├── js/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd secure_login_system
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
python app.py
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🧪 How to Test the System

### ✔️ Basic Flow

1. Register a new account
2. Login using credentials
3. Access dashboard
4. Enable 2FA
5. Scan QR code using Authenticator app
6. Verify OTP
7. Logout and login again with 2FA

---

## 🔍 Security Validation

* ✅ Passwords stored as hashed values
* ✅ SQL injection attempts fail
* ✅ Sessions are securely managed
* ✅ 2FA enforced when enabled

---

## 📊 Database Schema

### `users` Table

| Field              | Description        |
| ------------------ | ------------------ |
| id                 | Primary Key        |
| username           | Unique username    |
| password_hash      | Hashed password    |
| totp_secret        | Secret key for 2FA |
| two_factor_enabled | Boolean flag       |

---

## 🧠 Key Concepts Used

* Authentication & Authorization
* Cryptographic Hashing (`bcrypt`)
* Time-Based One-Time Passwords (TOTP)
* Secure Session Handling
* Input Validation & Sanitization

---

## 🚀 Future Enhancements

* 🔐 Password complexity enforcement
* 🌐 OAuth login (Google, GitHub)
* 📱 Mobile responsive improvements
* 📊 Admin panel for monitoring users
* 🧠 AI-based suspicious login detection

---

## 🛠️ Developer Notes

* Database file: `app.db`
* To reset:

  * Delete `app.db`
  * Restart the app

---

## 📌 Verification Checklist

* [x] Register → Login flow works
* [x] Passwords are hashed
* [x] SQL injection blocked
* [x] 2FA setup and verification works
* [x] Dashboard accessible only after authentication
---

## 💡 Conclusion

This project demonstrates how to build a **secure, scalable authentication system** by combining:

* Strong **backend security practices**
* Modern **UI/UX design principles**
* Real-world **2FA implementation**

