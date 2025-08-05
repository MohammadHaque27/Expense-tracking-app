from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#007bff')
    expenses = db.relationship('Expense', backref='category', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    # Get recent expenses
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    
    # Get monthly summary
    current_month = date.today().replace(day=1)
    monthly_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= current_month
    ).scalar() or 0
    
    # Get category totals for current month
    category_totals = db.session.query(
        Category.name, 
        Category.color,
        func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.date >= current_month
    ).group_by(Category.id).all()
    
    return render_template('index.html', 
                         recent_expenses=recent_expenses,
                         monthly_total=monthly_total,
                         category_totals=category_totals)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        category_id = int(request.form['category_id'])
        
        expense = Expense(
            description=description,
            amount=amount,
            date=expense_date,
            category_id=category_id
        )
        
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('add_expense.html', categories=categories)

@app.route('/expenses')
def expenses():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', type=int)
    
    query = Expense.query
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    
    expenses = query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categories = Category.query.all()
    return render_template('expenses.html', expenses=expenses, categories=categories)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    color = request.form['color']
    
    category = Category(name=name, color=color)
    db.session.add(category)
    db.session.commit()
    flash('Category added successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/delete_expense/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses'))

@app.route('/api/monthly_data')
def monthly_data():
    # Get last 12 months of data
    monthly_data = db.session.query(
        func.strftime('%Y-%m', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).group_by(func.strftime('%Y-%m', Expense.date)).order_by('month').limit(12).all()
    
    return jsonify([{'month': month, 'total': float(total)} for month, total in monthly_data])

def init_db():
    with app.app_context():
        db.create_all()
        
        # Add default categories if none exist
        if Category.query.count() == 0:
            default_categories = [
                Category(name='Food & Dining', color='#ff6b6b'),
                Category(name='Transportation', color='#4ecdc4'),
                Category(name='Shopping', color='#45b7d1'),
                Category(name='Entertainment', color='#96ceb4'),
                Category(name='Bills & Utilities', color='#feca57'),
                Category(name='Healthcare', color='#ff9ff3'),
                Category(name='Education', color='#54a0ff'),
                Category(name='Other', color='#5f27cd')
            ]
            
            for category in default_categories:
                db.session.add(category)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
