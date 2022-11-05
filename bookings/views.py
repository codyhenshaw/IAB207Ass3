from flask import Blueprint, render_template, request, redirect,url_for
from .models import Booking 

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    bookings = Booking.query.all()    
    return render_template('index.html', bookings=bookings)

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        book = "%" + request.args['search'] + '%'
        bookings = Booking.query.filter(Booking.description.like(book)).all()
        return render_template('index.html', bookings=bookings)
    else:
        return redirect(url_for('main.index'))