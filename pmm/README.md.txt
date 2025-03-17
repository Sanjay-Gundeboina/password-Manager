# Password Manager

## 📌 Overview
A secure password management system built using **HTML, CSS, JavaScript, SQL, Python, and Flask**. This project allows users to securely store, manage, and retrieve their passwords while ensuring authentication and data protection.

## 🚀 Features
- **User Authentication**: Secure login/signup with **bcrypt-hashed passwords**.
- **Guest Access**: Limited functionality for guest users.
- **Password Management**:
  - Store new credentials (Website, Username, Password).
  - Search for saved passwords.
  - Update or delete existing passwords.
- **Database Integration**: Uses **SQLite** for secure password storage.
- **Session Management**: Implements **Flask sessions** to ensure authentication security.
- **Responsive UI**: User-friendly interface with seamless navigation.

## 🛠️ Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: SQLite
- **Security**: bcrypt (for password hashing)

## 🏗️ Installation & Setup
### Prerequisites:
- Python (>=3.6)
- Flask
- SQLite

### Steps:
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/password-manager.git
   cd password-manager
   ```
2. **Install Dependencies**
   ```sh
   pip install flask bcrypt
   ```
3. **Run the Application**
   ```sh
   python app.py
   ```
4. **Access the Application**
   Open your browser and go to:  
   `http://127.0.0.1:5000`

## 📂 Project Structure
```
password-manager/
│── static/
│   ├── styles.css  # CSS styles
│── templates/
│   ├── index.html  # Homepage & Password Manager UI
│   ├── login.html  # User Login Page
│   ├── signup.html  # User Signup Page
│── app.py  # Flask backend
│── users.db  # SQLite database
│── README.md  # Project documentation
```

## 🔒 Security Measures
- Passwords are **hashed using bcrypt** before storage.
- Flask **session management** ensures authentication security.
- Only logged-in users can access the password manager.

## ✨ Future Enhancements
- Implement **AES encryption** for stored passwords.
- Add **multi-user support** with unique vaults.
- Enable **password strength checker** during registration.
- Develop **mobile-friendly UI improvements**.

## 👨‍💻 Author
**Sanjay Gundeboina**

For any queries or suggestions, feel free to reach out! 🚀

