from flask import Blueprint, render_template, request, flash, Flask, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Post,Image,User
from . import db
import json
import base64

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/uploads/'

"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user=current_user)
"""

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)

    if post:
        if post.user_id == current_user.user_id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})

@views.route('/', methods=['GET','POST'])
@login_required
def  home():
    if request.method == 'POST':
        note = request.form.get('note')

        pic = request.files['pic']

        if not pic:
            flash("No image uploaded!", category='error')
            return "No image uploaded!", 400
    
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        image_blob = base64.b64encode(pic.read())

        new_img = Image(img=image_blob, image_name=filename, mimetype=mimetype, user_id=current_user.user_id)

        db.session.add(new_img)

        new_post = Post(user_id=current_user.user_id, post_note=note,image_id=new_img.image_id)

        db.session.add(new_post)

        db.session.commit()

        flash('Post Created', category='success')
   
    return render_template("home.html", user=current_user)


@views.route('/img/<int:id>')
@login_required
def serve_img(id):

    img = Image.query.filter_by(image_id=id).first()

    if not img:
        return "Image Not Found", 404
    
    next_image = base64.b64decode(img.img)

    return Response(next_image, mimetype=img.mimetype)


@views.route('/explore', methods=['GET'])
def explore():
    return render_template("explore.html", user=current_user)

@views.route('/explore/<int:id>')
def explore_img(id):
    img = Image.query.filter_by(image_id=id).first()

    if not img:
        return "Image Not Found", 404
    
    next_image = base64.b64decode(img.img)

    return Response(next_image, mimetype=img.mimetype)

@views.route('/explore', methods=['GET'])
def posts():
    images = Image.query.all()
    
    return render_template("explore.html", images=images)