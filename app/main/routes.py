from flask import current_app, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm, EditProfileForm, EmptyForm
from app import photos, db
from app.models import Photo, User
from app.main.services import *


@bp.route('/display/<filename>')
@login_required
def display_image(filename):
    return redirect(url_for('static', filename='photos/' + filename),
                    code=301)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadForm()
    validate = validate_and_add_photo(form)
    if validate:
        return validate
    photos_db, next_url, prev_url, page = paginate_photos()

    return render_template('index.html', form=form,
                           photos=photos_db.items, next_url=next_url,
                           prev_url=prev_url, page=page)


@bp.route('/user/<username>')
@login_required
def user(username):
    user, photos, next_url, prev_url, page = paginate_user_photos(username)
    form = EmptyForm()
    return render_template('user.html', user=user, photos=photos.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    validate = validate_and_update_profile(form)
    if validate:
        return validate
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/like/<int:photo_id>', methods=['POST'])
@login_required
def like_photo(photo_id):
    photo = Photo.query.get(photo_id)

    if photo:
        if photo in current_user.liked_photos and photo.likes > 0:
            # User has already liked the photo, unlike it
            current_user.liked_photos.remove(photo)
            photo.likes -= 1
            liked = False
        else:
            # User has not liked the photo, like it

            if photo not in current_user.liked_photos:
                current_user.liked_photos.append(photo)
            photo.likes += 1
            liked = True

        db.session.commit()
        return jsonify({'likes': photo.likes, 'liked': liked})
    else:
        return jsonify({'error': 'Photo not found'}), 404


    