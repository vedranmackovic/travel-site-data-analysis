# Travel Booking Web App – Internship Project

A full-stack travel booking web application developed as part of a 9-week internship. The project combines core web development techniques with integrated data analysis and dynamic content generation from a relational database.

## 🔍 Overview

The application allows users to explore, compare, and select travel destinations based on location, accommodation, transport options, and service prices. It also includes an admin panel for managing destination data, booking data, user data, contact data and section with interactive charts based on booking data and destination data.

## 🛠️ Technologies Used

- **Backend**: Flask (Python), SQLAlchemy, SQLite
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Charts**: Plotly (via Flask integration)

## 📊 Key Features

### 🔹 Public Side
- **Dynamic destination listing** based on database content
- **Detailed destination pages** with accommodation and transport info
- **Pre-filled booking form** with logged-in user information for a faster checkout experience
- **Responsive design** and intuitive user interface

### 🔹 Admin Panel
- Dashboard overview
- View, create, edit, and delete destinations
- Toggle active/inactive destinations
- View and delete Users
- View and delete Bookings
- View Contact messages
- View data analytics via interactive charts

### 🔹 Charts & Data Analysis
- Top Destinations – most visited locations
- Service Cost per Destination – combined accommodation and transport costs
- Total Earnings – estimated revenue per destination
- Age Group Distribution – demographics of travelers
- Gender Comparison per Location – male vs. female bookings
- Traveler Nationalities – distribution of customers by nationality
- Top Travelers – users with the most bookings
- Accommodation Spending – total spent on accommodation per destination
- Transport Spending – total spent on transportation per destination
- Total Cost Spent – combined costs across all services
- Average Cost per Person – per capita travel cost
- Minimum Cost per Location – lowest recorded cost by destination
- Monthly Trends – bookings over time (by month)
- Monthly Total Cost – cost trends across months
- Yearly Trends and Total Cost – annual performance overview

## 📁 Project Structure
```
INTERNSHIP/
│
├── data/
│   ├── travel_data.csv           # CSV file used to generate data
│   └── app.db                   # SQLite database file generated on first run
│
├── migrations/                 # Database migrations via Flask-Migrate
├── models/                     # SQLAlchemy database models
│
├── static/
│   ├── img/                    # Destination images
│   ├── css/                    # Stylesheets
│   └── js/                     # Client-side JavaScript files
│
├── templates/                  # Jinja2 HTML templates
│
├── utils/                     # Data seeding and helper functions
│
├── app.py                     # Main Flask app and routes
├── charts.py                  # Chart-building logic using Plotly
│
├── .gitignore
├── NewDestination.txt          # Admin test file for creating new destinations
├── requirements.txt            # Project dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation
1. Clone the repo:
     ```bash
    git clone https://github.com/vedranmackovic/travel-site-data-analysis.git
    cd travel-site-data-analysis
    ```
2. (Optional) Create and activate a virtual environment:
    - macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    - Windows (PowerShell):
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application and initialize the database:
    ```bash
    python app.py
    ```
5. Open your browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

## 💻 Usage

Users can register, log in, and log out to access personalized features such as pre-filled booking forms.

An admin user is preconfigured with the following credentials (for testing and management purposes):

- **Email:** admin@admin.com  
- **Password:** vetravel

Admin users have access to the admin panel to manage destinations, bookings, users, messages, and view analytics.

## 📬 Contact

If you have questions, suggestions, or just want to connect:

- 📧 Email: [vedran.m.dev@gmail.com](mailto:vedran.m.dev@gmail.com)
- 🐙 GitHub: [vedranmackovic](https://github.com/vedranmackovic)

## License  
This project and its source code are provided for educational and non-commercial use only.  
You may use, study, and modify the materials for personal learning and academic projects.  
Any commercial use, redistribution, or publication without explicit permission is prohibited.  
No warranty is provided; use at your own risk. 