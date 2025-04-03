# Event Registration and Management App

## 📌 Overview
This is a **Django-based** event registration and management application that allows users to **create, register, and manage events**. Users can log in, register for events, and manage their own events.

## 🚀 Features
- User authentication (Register/Login/Logout)
- Create, edit, and delete events
- Categorized event listings (Upcoming, Ongoing, Past)
- Register/Unregister for events
- Organizer controls for event management
- Responsive and styled UI using **inline CSS** (no external stylesheets required)

## 🛠️ Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS (inline styling)
- **Database:** SQLite (default, can be changed to PostgreSQL/MySQL)

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
$ git clone https://github.com/yourusername/event-management.git
$ cd event-management
```

### 2️⃣ Create and Activate Virtual Environment
```bash
$ python -m venv venv
$ source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
$ pip install -r requirements.txt
```

### 4️⃣ Run Database Migrations
```bash
$ python manage.py migrate
```

### 5️⃣ Create Superuser (Optional for Admin Access)
```bash
$ python manage.py createsuperuser
```

### 6️⃣ Run the Development Server
```bash
$ python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser.

## 🎯 Usage
- **Users** can register/login and register for events.
- **Organizers** can create, edit, and delete events.
- **Event categories** help users track upcoming, ongoing, and past events.

## 📜 Folder Structure
```
📂 event_management/
├── 📂 events/               # Django app for event management
│   ├── 📄 models.py         # Database models
│   ├── 📄 views.py          # Business logic
│   ├── 📄 urls.py           # URL routing
│   ├── 📄 templates/        # HTML templates
│   ├── 📄 static/           # Static files (CSS, JS, images)
├── 📂 users/                # Django app for user authentication
├── 📂 templates/            # Global templates
├── 📄 manage.py             # Django management script
├── 📄 requirements.txt       # Python dependencies
└── 📄 README.md             # Project documentation
```

## 🚀 Future Enhancements
- Add email notifications for event registration
- Implement event search and filtering
- Improve UI with Bootstrap or TailwindCSS

## 📄 License
This project is open-source under the **MIT License**.

---
💡 **Developed with ❤️ using Django**

