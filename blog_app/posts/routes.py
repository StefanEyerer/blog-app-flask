from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from blog_app import db
from blog_app.models import Post
from blog_app.posts.forms import DeletePostForm, PostForm

posts = Blueprint('posts', __name__)


@posts.route('/')
def index():
    return redirect('list')


@posts.route('/list')
@login_required
def list():
    posts = Post.query.order_by(Post.created_at.desc())
    return render_template('posts/post_list.html', posts=posts)


@posts.route('<int:pk>/')
@login_required
def detail(pk):
    post = Post.query.get_or_404(pk)
    return render_template('posts/post_detail.html', post=post)


@posts.route('create/', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('posts.detail', pk=post.id))
    return render_template('posts/post_form.html', form=form)


@posts.route('<int:pk>/update/', methods=['GET', 'POST'])
@login_required
def update(pk):
    post = Post.query.get_or_404(pk)
    if post.author != current_user:
        abort(403)
    form = PostForm(title=post.title, content=post.content)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('posts.detail', pk=post.id))
    return render_template('posts/post_form.html', form=form)


@posts.route('<int:pk>/delete/', methods=['GET', 'POST'])
@login_required
def delete(pk):
    post = Post.query.get_or_404(pk)
    form = DeletePostForm()
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted.', 'success')
        return redirect(url_for('posts.index'))
    return render_template('posts/post_confirm_delete.html', form=form, post=post)
