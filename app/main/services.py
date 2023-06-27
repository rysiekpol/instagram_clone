from flask import redirect, url_for, flash, request, current_app
from app.main.forms import UploadForm
from app import photos, db
from flask_login import current_user
from app.models import Photo


def validate_and_add_photo(form: UploadForm):
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        print(filename)
        #file_url = url_for('main.get_file', filename=filename)

        photo = Photo(path=filename, description=form.description.data, author=current_user)
        db.session.add(photo)
        db.session.commit()
        flash('Your photo is now live!')
        return redirect(url_for('main.index'))
    else:
        filename = None


def paginate_photos():
    page = request.args.get('page', 1, type=int)

    photos_db = Photo.query.order_by(Photo.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    
    next_url = url_for('main.index', page=photos_db.next_num) \
        if photos_db.has_next else None
    prev_url = url_for('main.index', page=photos_db.prev_num) \
        if photos_db.has_prev else None

    return photos_db, next_url, prev_url, page