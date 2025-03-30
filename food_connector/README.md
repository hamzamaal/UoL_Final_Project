# 🥕 Food Donation Management & Tracking System

## 🧭 Overview

The **Food Donation Management and Tracking System** is a Python-based web application designed to streamline the process of food donation. Built with **Flask**, it features a user-friendly interface using HTML/CSS and integrates with a **MySQL** database for secure and reliable data handling.  

The platform connects **donors**, **recipients**, and **administrators** through a role-based system that enhances transparency, accountability, and the efficiency of food redistribution.

---

## 🚀 Key Features

### 👨‍🍳 Donor Capabilities
- Add new food donations with detailed item information.
- Track both active and completed donations.
- Cancel pending donations.
- Receive:
  - Real-time status notifications.
  - Alerts for items nearing expiration.
  - Feedback from recipients.

### 👩‍👧 Recipient Capabilities
- Browse available donations and request specific items using their unique IDs.
- Track status of current and past requests.
- Receive:
  - Notifications about request progress.
  - Feedback for completed donations.

### 🛠️ Admin Capabilities
- View live statistics on donations (pending, completed, canceled).
- Monitor user activity and review system logs.
- Remove users and associated records when necessary.

---

## 📦 Requirements

Ensure the following are installed:

- **Python 3.8 or higher**  
  👉 [Download Python](https://www.python.org/downloads/)

- **MySQL Server 8.0 or higher**  
  👉 [Download MySQL](https://dev.mysql.com/downloads/)

- **Flask**  
  A lightweight Python web framework.

- **python-dotenv**  
  For secure management of environment variables.

---

## 📥 Installation

Install the required libraries using `pip`:

```bash
pip install flask flask-mysql-connector python-dotenv
```

Alternatively, use a `requirements.txt` file:

```txt
flask
flask-mysql-connector
python-dotenv
```

Then run:

```bash
pip install -r requirements.txt
```

---

## 💡 Optional: Future Enhancements

- Role-based access control improvements
- Email/SMS notification integration
- Graphical analytics dashboard for stakeholders
