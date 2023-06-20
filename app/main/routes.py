from flask import current_app, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm
from app import photos, db
from app.models import Photo

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
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('main.get_file', filename=filename)

        photo = Photo(path=file_url, description=form.description.data, author=current_user)
        db.session.add(photo)
        db.session.commit()
        flash('Your photo is now live!')
        return redirect(url_for('main.index'))
    else:
        file_url = None
        
    page = request.args.get('page', 1, type=int)

    photos_db = Photo.query.order_by(Photo.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    
    next_url = url_for('main.index', page=photos_db.next_num) \
        if photos_db.has_next else None
    prev_url = url_for('main.index', page=photos_db.prev_num) \
        if photos_db.has_prev else None
    return render_template('index.html', form=form,
                           photos=photos_db.items, next_url=next_url,
                           prev_url=prev_url, page=page)


    