from flask import Blueprint, render_template, request, redirect, url_for
from .models import Booking, Comment
from .forms import BookingForm, CommentForm
from . import db, app
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

bp = Blueprint('booking', __name__, url_prefix='/bookings')

@bp.route('/<id>')
def show(id):
    booking = Booking.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('bookings/show.html', booking=booking, form=cform)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = BookingForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    booking=Booking(name=form.name.data,description=form.description.data, 
    image=db_file_path,currency=form.currency.data)
    # add the object to the db session
    db.session.add(booking)
    # commit to the database
    db.session.commit()
    print('Successfully created new travel booking', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('booking.create'))
  return render_template('bookings/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<booking>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(booking):  
    form = CommentForm()  
    #get the booking object associated to the page and the comment
    booking_obj = Booking.query.filter_by(id=booking).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        booking=booking_obj,
                        user=current_user) 
      #here the back-referencing works - comment.booking is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to booking.show
    return redirect(url_for('booking.show', id=booking))