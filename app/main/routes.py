from flask import current_app, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm
from app import photos, db
from app.models import Photo
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


    