from flask import current_app, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm, EditProfileForm, EmptyForm
from app import photos, db
from app.models import Photo, User
from app.main.services import validate_and_add_photo, paginate_photos, paginate_user_photos, validate_and_update_profile \
    , handle_photos_in_database


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
    if (validate := validate_and_add_photo(form)):
        return validate
    photos_db, next_url, prev_url, page = paginate_photos()

    return render_template('index.html', form=form,
                           photos=photos_db.items, next_url=next_url,
                           prev_url=prev_url, page=page)


@bp.route('/user/<username>')
@login_required
def user(username):
    user, photos, next_url, prev_url = paginate_user_photos(username)
    form = EmptyForm()
    return render_template('user.html', user=user, photos=photos.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if (validate := validate_and_update_profile(form)):
        return validate
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/like/<int:photo_id>', methods=['POST'])
@login_required
def like_photo(photo_id):
    photo = Photo.query.get(photo_id)

    if photo:
        return(handle_photos_in_database(photo))
    else:
        return jsonify({'error': 'Photo not found'}), 404


    