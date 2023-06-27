from flask import current_app, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm
from app import photos, db
from app.models import Photo
from app.main.services import validate_and_add_photo, paginate_photos


@bp.route('/uploads/<filename>')
@login_required
def get_file(filename):
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],
                               filename)

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


    