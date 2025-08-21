 🏦 Banking System (Python, OOP, CLI)

[![Dockerized](https://img.shields.io/badge/Dockerized-Yes-blue?logo=docker&logoColor=white)](https://www.docker.com/)

A multi-module **banking application** built in Python that simulates the core functionality of a retail bank.  

## 🚀 Features
- **Account Management**
  - Open/close accounts with unique **8-digit account numbers** and system-generated **4-digit PINs**.
  - Secure account handling with **masked SSN** display.
  - Balances stored in **cents** to prevent floating-point errors.  

- **Transactions**
  - Deposits & withdrawals (PIN-verified).  
  - Account-to-account transfers.  
  - Monthly **interest accrual** (APR/12), with **half-up rounding** for accuracy.  

- **ATM & Coin Handling**
  - **ATM cash breakdown** (withdrawals return bills in $50/$20/$10/$5/$1).  
  - **Coin parser** accepts input like `10q 3d 7n 5p` and converts directly to cents.  

- **Menu-Driven CLI**
  - Intuitive text-based interface.  
  - Robust input validation and helpful error messages.  

## 🛠️ Tech Stack
- **Language:** Python 3.x  
- **Paradigm:** Object-Oriented Programming (OOP)  
- **Modules:**  
  - `Account.py` → Encapsulates account data (owner, SSN, PIN, balance).  
  - `Bank.py` → Manages accounts, generates unique IDs, ensures capacity.  
  - `BankManager.py` → Main CLI interface with transaction menus.  
  - `BankUtility.py` → Utility functions (currency formatting, dollar→cent conversion).  
  - `CoinCollector.py` → Regex-based coin string parser.  

## 📂 Project Structure
```
BankingSystem/
│── Account.py
│── Bank.py
│── BankManager.py   # Entry point (main program)
│── BankUtility.py
│── CoinCollector.py
```

## ▶️ How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/BankingSystem.git
   cd BankingSystem
   ```
2. Run the manager:
   ```bash
   python BankManager.py
   ```

## 💻 Sample Usage
```
=== Welcome to the Bank Manager ===
1) Open Account
2) Close Account
3) Deposit
4) Withdraw
5) Transfer
6) ATM Withdrawal
7) Deposit Coins
8) Apply Monthly Interest
0) Exit

>> Selection: 1
Enter Name: John Doe
Enter SSN: 123-45-6789
Account created!
Account #: 12345678 | PIN: 4821
```

## 🌟 Future Improvements
- Add persistent storage (SQLite or JSON).  
- Support multiple currencies.  
- Add unit tests for core functionality.  
- Enhance security (hashed PINs, encryption).  

## 📜 License
MIT License — free to use, modify, and distribute.  
