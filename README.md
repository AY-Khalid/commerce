# 🏷️ CS50 Commerce – Online Auction Site

This is my implementation of **Project 2 – Commerce** from [CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/).  
It is a Django-powered auction site where users can create listings, place bids, comment on items, and manage a watchlist.

---

## Features
- User authentication (register, login, logout)
- Create auction listings with title, description, category, and optional image
- Place bids (must be higher than current bid)
- Track highest bidder and winning auction
- Add/remove listings from your personal watchlist
- Comment on listings
- Close/Remove listings (owner only)
- Auction history (active, removed, won)
- Mobile responsive design using **Bootstrap 4**

---

## Technologies
- [Django 5](https://www.djangoproject.com/) – Web framework
- [Bootstrap 4](https://getbootstrap.com/) – Responsive design
- SQLite – Database (default for Django)
- [Whitenoise](http://whitenoise.evans.io/) – Static files for deployment
- Gunicorn – Production WSGI server

---

## ⚙️ Installation (Local Setup)

1. Clone repository:

   git clone https://github.com/YOUR_USERNAME/cs50-commerce.git
   cd cs50-commerce
Create and activate virtual environment:


python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies:


pip install -r requirements.txt
Run migrations:


python manage.py migrate
Start development server:


python manage.py runserver
Open in browser:

cpp
http://127.0.0.1:8000/
📦 Deployment (Render/Heroku)
Files needed for deployment are already included:

requirements.txt – Python dependencies

Procfile – Gunicorn command

runtime.txt – Python version

Example Procfile
makefile

web: gunicorn commerce.wsgi
Example runtime.txt
Copy code
python-3.11.9
Static files are handled with Whitenoise.
On deployment, run:


python manage.py collectstatic --noinput
📂 Project Structure

commerce/
│── auctions/        # App (models, views, templates)
│── commerce/        # Project settings and URLs
│── templates/       # HTML templates
│── static/          # CSS and images
│── manage.py
│── requirements.txt
│── Procfile
│── runtime.txt
│── README.md
🎯 To Do / Future Improvements
Add categories filter on index page

Improve styling of comments

Switch to PostgreSQL for production

Add real-time bid updates (WebSockets/Channels)

📝 License
This project was created as part of CS50 Web Programming with Python and JavaScript.
Feel free to fork, modify, and learn from it.