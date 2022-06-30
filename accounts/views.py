from collections import namedtuple
from datetime import timedelta
import re

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Post, Profile, Follow
from .additional import get_profile_photo, save_photo

FullProfile = namedtuple('FullProfile', 'photo user')
PostTuple = namedtuple('PostTuple', 'user photo post')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        username, password = username.strip(), password.strip()

        if re.match(r'^([A-Za-z0-9_]){2,30}$', username) and re.match(r'^([A-Za-z0-9_]){2,30}$', password):
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return render(request, 'accounts/login.html', {'message': 'Invalid username or password'})
            else:
                if user.check_password(password):
                    if user.is_active:
                        login(request, user)
                        return redirect(reverse('accounts:profile', args=[user.username]))
                    else:
                        return render(request, 'accounts/login.html', {'message': 'User is disable'})
                else:
                    return render(request, 'accounts/login.html', {'message': 'Wrong password'})
        else:
            return render(request, 'accounts/login.html', {'message': 'Invalid username or password'})

    return render(request, 'accounts/login.html', {'message': None})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        username, password = username.strip(), password.strip()

        if not re.match(r'^([A-Za-z0-9_]){2,30}$', username):
            message = 'Username can only consist of letters, digits and underscores. ' \
                      'Length should be at least 2 characters'
            return render(request, 'accounts/registration.html', {'message': message})

        elif not re.match(r'^([A-Za-z0-9_]){6,20}$', password):
            message = 'Password can only consist of letters, digits and underscores. ' \
                      'Length should be at least 6 characters'
            return render(request, 'accounts/registration.html', {'message': message})

        if User.objects.filter(username=username).exists():
            message = 'This username already taken'
            return render(request, 'accounts/registration.html', {'message': message})
        else:
            try:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                return redirect(reverse('accounts:edit', args=[user.username]))
            except Exception:
                message = 'Something went wrong'
                return render(request, 'accounts/registration.html', {'message': message})

    return render(request, 'accounts/registration.html')


def profile(request, username):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:home'))

    if request.method == 'POST':
        change_following = request.POST.get('follow', None)
        if change_following == 'start':
            try:
                first_user = User.objects.get(username=request.user.username)
                second_user = User.objects.get(username=username)
                if first_user and second_user:
                    f = Follow(first_user_id=first_user.id, second_user_id=second_user.id)
                    f.save()
            except ObjectDoesNotExist:
                pass

        if change_following == 'stop':
            try:
                first_user = User.objects.get(username=request.user.username)
                second_user = User.objects.get(username=username)
                if first_user and second_user:
                    f = Follow.objects.get(first_user_id=first_user.id, second_user_id=second_user.id)
                    f.delete()
            except ObjectDoesNotExist:
                pass

        if request.POST.get('publish', None):
            post_body = request.POST.get('post_body', None)
            post_title = request.POST.get('post_title', None)
            post_title, post_body = post_title.strip(), post_body.strip()

            if post_body and post_title:
                post = Post(title=post_title , author=request.user, body=post_body)
                post.save()

        try:
            delete_post_id = request.POST.get('delete_post', None)
            if delete_post_id:
                post = Post.objects.get(id=delete_post_id)
                post.delete()
        except ObjectDoesNotExist:
            pass

        logout_request = request.POST.get('logout', None)
        if logout_request:
            logout(request)
            return redirect(reverse('accounts:home'))

    status = 'NotFollowed'
    if username == request.user.username:
        mode = 'MyProfile'
    else:
        mode = 'OtherProfile'
        try:
            first_user = User.objects.get(username=request.user.username)
            second_user = User.objects.get(username=username)
            if Follow.objects.filter(first_user_id=first_user.id, second_user_id=second_user.id).first():
                status = 'Followed'
        except ObjectDoesNotExist:
            pass

    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user.id)

    profile_photo = get_profile_photo(user)

    posts = Post.objects.filter(author__username=username)

    context = {'user': user, 'posts': posts, 'profile': user_profile, 'profile_photo': profile_photo,
               'mode': mode, 'from_profile': request.user.username, 'status': status}
    return render(request, 'accounts/profile.html', context)


def edit_profile(request, username):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:home'))

    if request.user.username != username:
        return redirect(reverse('accounts:profile', args=[username]))

    invalid = False
    if request.method == 'POST':
        if request.POST.get('save', None):
            first_name = request.POST.get('firstname', '')
            last_name = request.POST.get('lastname', '')
            bio = request.POST.get('bio', '')
            birthday = request.POST.get('birthday', '')
            if not (first_name.strip() and last_name.strip() and bio.strip() and birthday.strip()):
                invalid = True
            else:
                user = get_object_or_404(User, username=request.user.username)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                profile = get_object_or_404(Profile, user=user.id)
                profile.bio = bio
                profile.birth_date = birthday
                profile.save()
                invalid = False

        photo = request.FILES.get('photo', None)
        if photo:
            try:
                user = get_object_or_404(User, username=request.user.username)
                profile = Profile.objects.get(user=user.id)
            except ObjectDoesNotExist:
                pass
            else:
                save_photo(photo, profile)

    user = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(Profile, user=user.id)
    profile_photo = get_profile_photo(user)

    context = {'from_profile': username, 'profile': profile, 'user': user,
               'profile_photo': profile_photo, 'invalid': invalid}
    return render(request, 'accounts/edit_profile.html', context)


def following_list(request, username):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:home'))

    if username == request.user.username:
        mode = 'MyProfile'
    else:
        mode = 'OtherProfile'

    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(first_user_id=user.id)
    followed = []
    if following:
        for link in following:
            try:
                followed_user = User.objects.get(id=link.second_user_id)
                if followed_user:
                    profile_photo = get_profile_photo(followed_user)
                    followed.append(FullProfile(profile_photo, followed_user))
            except ObjectDoesNotExist:
                pass

    return render(request, 'accounts/following.html', {'followed': followed, 'mode': mode, 'from_profile': user})


def search(request):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:home'))

    context = {}
    if request.POST:
        search_query = str.lower(request.POST.get('query', None))
        search_results = []
        recommendations = []
        if search_query:
            recommendations_count = 10
            for user in User.objects.all().exclude(username=request.user.username):
                if any(list(map(lambda n: n in ' '.join((user.first_name, user.last_name, user.username)).lower(),
                                search_query.split()))):
                    profile_photo = get_profile_photo(user)
                    search_results.append(FullProfile(profile_photo, user))
                else:
                    if recommendations_count:
                        profile_photo = get_profile_photo(user)
                        recommendations.append(FullProfile(profile_photo, user))
                        recommendations_count -= 1

        context['search_results'] = search_results
        context['recommendations'] = recommendations
        context['from_profile'] = request.user.username
    return render(request, 'accounts/search.html', context)


def feed(request):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:home'))

    from_profile = request.user.username
    posts = []

    following = list(Follow.objects.filter(first_user_id=request.user.id).values_list('second_user_id', flat=True))
    for post in Post.objects.filter(publish__gte=(timezone.now() - timedelta(days=5))):
        if post.author.id in following:
            try:
                author = User.objects.get(username=post.author)
                profile_photo = get_profile_photo(author)
                posts.append(PostTuple(author, profile_photo, post))
            except ObjectDoesNotExist:
                pass

    return render(request, 'accounts/feed.html', {'from_profile': from_profile, 'posts': posts})


def index(request):
    return render(request, 'accounts/home.html')
