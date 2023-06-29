from flask import current_app, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm, EditProfileForm, EmptyForm
from app import photos, db
from app.models import Photo, User
from app.main.services import validate_and_add_photo, paginate_photos


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
    validate_and_add_photo(form)
    photos_db, next_url, prev_url, page = paginate_photos()

    return render_template('index.html', form=form,
                           photos=photos_db.items, next_url=next_url,
                           prev_url=prev_url, page=page)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    photos = user.photos.order_by(Photo.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.user', username=user.username,
                       page=photos.next_num) if photos.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=photos.prev_num) if photos.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, photos=photos.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


    