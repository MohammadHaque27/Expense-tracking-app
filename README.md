
# Automated Expense Tracker Web App

A modern, responsive web application for tracking personal expenses built with Flask, SQLite, Bootstrap, and Chart.js.

## Features

- **Dashboard Overview**: Visual charts showing monthly expenses and category breakdowns
- **Expense Management**: Add, view, and delete expenses with categorization
- **Category System**: Organize expenses with color-coded categories
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Data Visualization**: Interactive charts for expense analysis
- **Pagination**: Efficient browsing of large expense lists
- **Filtering**: Filter expenses by category

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite (easily configurable to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Installation

1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and go to `http://localhost:5000`

## Usage

1. **Adding Expenses**: Click "Add Expense" to record new expenses with description, amount, date, and category
2. **Viewing Dashboard**: The main dashboard shows recent expenses, monthly totals, and category breakdowns
3. **Managing Categories**: Add custom categories with colors in the Categories section
4. **Filtering**: Use the category filter on the expenses page to view specific types of expenses

## Default Categories

The app comes with pre-configured categories:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Other

## Database

The app uses SQLite by default with the database file `expenses.db`. To switch to PostgreSQL, update the `SQLALCHEMY_DATABASE_URI` in `app.py`.

## Security Note

Remember to change the `SECRET_KEY` in `app.py` before deploying to production.

## License

This project is open source and available under the MIT License.
