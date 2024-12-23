from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import UserCreatingForm, UserLoginForm, PostForm, CommentForm, EditProfileForm
from django.views.generic import FormView, UpdateView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import User, Post, Comment
from django.views.generic import ListView
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


class Register(generic.CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreatingForm
    success_url = reverse_lazy('login')


class PostCreate(generic.CreateView):
    template_name = 'blog/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('')
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 50

    def get_queryset(self):
        return Post.objects.all().order_by('-published_at')


def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_list')


class Login(FormView):
    template_name = 'blog/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super(Login, self).form_valid(form)
        else:
            form.add_error('username', 'Неправильное имя пользователя или пароль')
            return super(Login, self).form_valid(form)


def custom_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('post_list')
    else:
        return redirect('login')


class UserProfileListView(ListView):
    model = User
    template_name = 'blog/profile_list.html'

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'blog/profile.html', {'user': user})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        post.delete()

    return redirect('post_list')


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=user.username)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'blog/edit_profile.html', {'form': form})


@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('login')
    return render(request, 'blog/delete_profile.html')