from flask import current_app, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import UploadForm, EditProfileForm, EmptyForm, CommentForm
from app import photos, db
from app.models import Photo, Comment
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
    form_c = CommentForm()
    validate = validate_and_add_photo(form)
    if validate:
        return validate
    photos_db, next_url, prev_url, page = paginate_followed_photos()

    return render_template('index.html', form=form, form_c=form_c,
                           photos=photos_db.items, next_url=next_url,
                           prev_url=prev_url, page=page, Comment=Comment)


@bp.route('/user/<username>')
@login_required
def user(username):
    user, photos, next_url, prev_url = paginate_user_photos(username)
    form = EmptyForm()
    form_c = CommentForm()

    return render_template('user.html', user=user, photos=photos.items,
                           next_url=next_url, prev_url=prev_url, form=form, form_c=form_c,
                           Comment=Comment)

@bp.route('/explore')
@login_required
def explore():
    photos, next_url, prev_url, page = paginate_photos()
    form_c = CommentForm()

    return render_template('index.html', photos=photos.items,
                           next_url=next_url, prev_url=prev_url, page=page, form_c=form_c,
                           Comment=Comment)


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
    

@bp.route('/photo/comment/<int:photo_id>', methods=['POST'])
@login_required
def comment_photo(photo_id):
    photo = Photo.query.get(photo_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, photo_id=photo_id, user_id=current_user.id)
        print(comment.user_id)
        if photo:
            if comment:
                photo.comments.append(comment)
                db.session.commit()
                flash('Your comment is now live!')
                return redirect(url_for('main.index'))
            else:
                flash('Comment body is empty')
                return redirect(url_for('main.index'))
        else:
            flash('Photo not found')
            return redirect(url_for('main.index'))
        

@bp.route('/photo/comments/<int:photo_id>', methods=['GET'])
@login_required
def get_photo_comments(photo_id):
    page = request.args.get('page', 1, type=int)
    per_page = 5

    photo = Photo.query.get(photo_id)
    if not photo:
        flash('Photo not found')
        return redirect(url_for('main.index'))

    comments = Comment.query.filter_by(photo_id=photo_id).order_by(Comment.timestamp.desc()).paginate(page=page, per_page=per_page)

    return comments

@bp.route('/comments', methods=['GET'])
def load_more_comments():
    page = request.args.get('page', type=int)
    photo_id = request.args.get('photoId')
    photo = Photo.query.get(photo_id)

    comments = photo.comments.order_by(Comment.timestamp.desc()).offset((page - 1) * 5).limit(5)
    html = ''
    for comment in comments:
        html += render_template('_comment.html', comment=comment, photo=photo)

    return jsonify(html=html)

@bp.route('/add-friend/<username>', methods=['POST'])
@login_required
def add_friend(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found')
            return redirect(url_for('main.index'))
        
        if user == current_user:
            flash('You cannot add yourself as friend')
            return redirect(url_for('main.user', username=username))
        
        current_user.add_friend(user)
        db.session.commit()
        flash(f'You are now friends with {username}')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/remove-friend/<username>', methods=['POST'])
@login_required
def remove_friend(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found')
            return redirect(url_for('main.index'))
        
        if user == current_user:
            flash('You cannot remove yourself as friend')
            return redirect(url_for('main.user', username=username))
        
        current_user.remove_friend(user)
        db.session.commit()
        flash(f'You are not friends with {username}')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


    