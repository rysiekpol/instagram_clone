from flask import current_app, flash, jsonify, redirect, request, url_for
from flask_login import current_user

from app import db, photos
from app.main.forms import UploadForm
from app.models import Photo, User


def validate_and_add_photo(form: UploadForm):
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        print(filename)
        # file_url = url_for('main.get_file', filename=filename)

        photo = Photo(
            path=filename, description=form.description.data, author=current_user
        )
        db.session.add(photo)
        db.session.commit()
        flash("Your photo is now live!")
        return redirect(url_for("main.index"))
    elif request.method == "POST":
        flash("Invalid photo type. We accept only jpg/png. Please try again.")
    filename = None


def paginate_photos():
    page = request.args.get("page", 1, type=int)

    photos_db = Photo.query.order_by(Photo.timestamp.desc()).paginate(
        page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )

    next_url = (
        url_for("main.index", page=photos_db.next_num) if photos_db.has_next else None
    )
    prev_url = (
        url_for("main.index", page=photos_db.prev_num) if photos_db.has_prev else None
    )

    return photos_db, next_url, prev_url, page


def paginate_followed_photos():
    page = request.args.get("page", 1, type=int)

    photos_db = current_user.get_followed_photos().paginate(
        page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )

    next_url = (
        url_for("main.index", page=photos_db.next_num) if photos_db.has_next else None
    )
    prev_url = (
        url_for("main.index", page=photos_db.prev_num) if photos_db.has_prev else None
    )

    return photos_db, next_url, prev_url, page


def paginate_user_photos(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    photos = user.photos.order_by(Photo.timestamp.desc()).paginate(
        page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    next_url = (
        url_for("main.user", username=user.username, page=photos.next_num)
        if photos.has_next
        else None
    )
    prev_url = (
        url_for("main.user", username=user.username, page=photos.prev_num)
        if photos.has_prev
        else None
    )
    return user, photos, next_url, prev_url


def validate_and_update_profile(form):
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me


def handle_photos_in_database(photo: Photo):
    if photo in current_user.liked_photos:
        # User has already liked the photo, unlike it
        current_user.liked_photos.remove(photo)
        photo.likes = Photo.likes - 1
        liked = False
    else:
        # User has not liked the photo, like it
        if photo not in current_user.liked_photos:
            current_user.liked_photos.append(photo)
        photo.likes = Photo.likes + 1
        liked = True

    db.session.commit()
    return jsonify({"likes": photo.likes, "liked": liked})
