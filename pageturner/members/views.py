from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Snippet, SharedSnippet, Book, Comment
from .utils import generate_avatar
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfilePicForm, CommentForm, SnippetUpdate, CommentUpdate
from django.shortcuts import get_object_or_404
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("welcome_page")
    else:
        form = CustomAuthenticationForm(request)

    return render(request, "authenticate/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('welcome_page')


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You are registered successfully.")
            return redirect("welcome_page")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "authenticate/register_user.html", {"form": form})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)

        # for profile in profiles:
        #     profile.avatar_svg = generate_avatar_list(profile.user.username)

        return render(request, "profiles/profile_list.html", {"profiles": profiles})

    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, f"You have unfollowed {profile}")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, f"You are following {profile}")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=pk)
        user_snippets = Snippet.objects.filter(user_id=pk).order_by("-created_at")
        shared_snippets = SharedSnippet.objects.filter(user_id=pk).order_by("-shared_at")
        books_bookmarked = Profile.objects.filter(books_bookmarked=True)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            current_user_profile.save()

        return render(request, "profiles/profile.html", {"profile": profile, "user_snippets": user_snippets, "shared_snippets": shared_snippets, "books_bookmarked": books_bookmarked})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


def update_user(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(User, id=request.user.id)
        profile_user = get_object_or_404(Profile, user__id=request.user.id)

        if request.method == 'POST':
            user_form = RegisterForm(request.POST, instance=current_user)
            profile_form = ProfilePicForm(request.POST, request.FILES, instance=profile_user)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                login(request, current_user)
                messages.success(request, "Your profile has been updated!")
                return redirect('welcome_page')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            user_form = RegisterForm(instance=current_user)
            profile_form = ProfilePicForm(instance=profile_user)

        return render(request, "profiles/update_user.html", {"user_form": user_form, "profile_form": profile_form})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


def snippet_like(request, pk):
    if request.user.is_authenticated:
        snippet = get_object_or_404(Snippet, id=pk)
        if snippet.likes.filter(id=request.user.id):
            snippet.likes.remove(request.user)
        else:
            snippet.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


@login_required()
def comment_like(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.likes.filter(id=request.user.id):
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return redirect(request.META.get("HTTP_REFERER"))


def snippet_delete(request, pk):
    if request.user.is_authenticated:
        snippet = get_object_or_404(Snippet, id=pk)
        snippet.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')


@login_required
def snippet_edit(request, pk):
    snippet = get_object_or_404(Snippet, id=pk)
    form = SnippetUpdate(request.POST, instance=snippet)
    if form.is_valid():
        form.save()
        messages.success(request, "Your snippet has been successfully updated!")
        return redirect('welcome_page')
    else:
        form = SnippetUpdate(instance=snippet)
    return render(request, 'snippets/edit_snippet.html', {"form": form, "snippet": snippet})


def snippet_share(request, pk):
    original_snippet = get_object_or_404(Snippet, id=pk)

    shared_snippet = SharedSnippet.objects.create(original_snippet=original_snippet, user=request.user)

    return redirect('profile', pk=request.user.pk)


@login_required
def snippet_comment(request, pk):
    original_snippet = get_object_or_404(Snippet, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.original_snippet = original_snippet
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been successfully posted.")
            return redirect("welcome_page")
    else:
        form = CommentForm()
    return render(request, "snippets/comment_snippet.html", {"original_snippet": original_snippet, "form": form})


@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def comment_edit(request, snippet_id, comment_id):
    original_snippet = get_object_or_404(Snippet, id=snippet_id)
    comment = get_object_or_404(Comment, id=comment_id, original_snippet=original_snippet)
    form = CommentUpdate(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        messages.success(request, "Your comment has been successfully updated!")
        return redirect('welcome_page')
    else:
        form = CommentUpdate(instance=comment)
    return render(request, 'snippets/edit_comment.html', {"form": form, "comment": comment, "original_snippet": original_snippet})


def bookmark_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.user.is_authenticated:
        request.user.profile.books_bookmarked.add(book)
        messages.success(request, f"You have bookmarked {book.title} by {book.author}.")
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')

    return redirect('profile', pk=request.user.pk)


def mark_as_read(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.user.is_authenticated:
        request.user.profile.books_read.add(book)
        messages.success(request, f"You have added {book.title} by {book.author} as a finished book.")
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('welcome_page')

    return redirect('profile', pk=request.user.pk)

