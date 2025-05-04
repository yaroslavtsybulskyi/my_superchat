# Django WebSocket Chat App

This is a minimal Django application that supports real-time chat functionality via WebSockets. Users are grouped based on their company and can only communicate within their group. WebSocket messages are broadcast via Redis.

---

## 🚀 Features

- WebSocket communication using Django Channels
- Only authenticated users can join the chat
- Users are grouped by company
- Messages are broadcast only within the user's company
- Company updates trigger WebSocket notifications
- Async database queries in consumers

---

## 🧱 Requirements

- Python 3.11+
- Redis running locally (default on port 6379)
- Virtualenv (optional but recommended)

---

## 🛠️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yaroslavtsybulskyi/my_superchat.git
cd my_superchat
```
2. **Create a virtual environment and activate it**:
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. **Install dependencies**:
```bash
pip install -r requirements.txt
```
4. **Run Redis locally:**:
Make sure Redis is installed and running:
```bash
redis-server
```
5.	**Apply migrations**:
```bash
python manage.py migrate
```

6. **Create a superuser:**:
```bash
python manage.py createsuperuser
```

7. **Run the ASGI server (Daphne)**:
```bash
daphne -b 0.0.0.0 -p 8000 my_superchat.asgi:application
```

🧪 Usage  
	1.	Go to the admin panel: http://localhost:8000/admin/  
	2.	Create a Company  
	3.	Create User accounts and assign them Profile objects linked to a Company  
	4.	Log in with one of the users at: http://localhost:8000/login/  
	5.	Join a group via URL: http://localhost:8000/chat/company_<company_id>/  
	6.	Test the WebSocket connection by sending messages or triggering a company update:  

Trigger a company name update

You can test real-time system messages by making a POST request (e.g. via Postman):
```
POST http://localhost:8000/update-company/1/
Body (form-data):
name: New Company Name
```

💡 Notes  
	•	Redis must be running locally on port 6379.  
	•	The app uses Django Channels with Redis as the backing store.  
	•	Users must be authenticated and have a related Profile to join the chat.  
	•	Messages do not persist — the app is designed for real-time, not history.  
