from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from .models import Post, Comment
from .forms import PostCreatedForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy



class BaseView(ListView):
    template_name = "post_list.html"
    model = Post


class CreatePost(LoginRequiredMixin, View):
    form = PostCreatedForm
    login_url = '/accounts/login'

    def get(self, request):
        return render(request, 'create.html', {'form': self.form})

    def post(self, request):
        form = PostCreatedForm(data=request.POST, files=request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("/")
        else:
            return render(request, 'create.html', {'form': form})


class PostCheck(View):
    model = Post
    template_name = "post_check.html"
    comment_form = CommentForm

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.views = int(post.views) + 1
        post.save()
        like = post.likes.filter(id=request.user.id).exists()
        comment = Comment.objects.filter(post=post).order_by("-id")
        return render(request, self.template_name, {
            'object': post,
            'like': like,
            'comment_form': self.comment_form,
            'comments': comment,
        })

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(
                post=post,
                comment=comment,
                user=request.user,
            )
            return redirect(post.get_absolute_url())


class Search(View):
    def get(self, request):
        q = request.GET.get("q")
        object_list = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q) |
            Q(author__username=q)
        )
        return render(request, "post_list.html", {'object_list': object_list})


def like_dislike(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_pk'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(post.get_absolute_url())


class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'edit.html'

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy("home")

class ProfileView(ListView):
    model = Post
    template_name = 'profile.html'
