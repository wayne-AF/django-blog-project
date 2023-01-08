from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post
# don't forget, must import the class from the forms.py file
from .forms import CommentForm

# This creates our view for the list of posts
# generic is built-in django model
class PostList(generic.ListView):
    model = Post
    # the status=1 refers to published posts as opposed to draft posts
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    # determines how many posts can be viewed on a single page
    paginate_by = 6


# not using generic views here so must do everything ourselves
class PostDetail(View):

    # we figure out which post we want to display by using the slug, which is unique to each post
    def get(self, request, slug, *args, **kwargs):
        # status=1 because we only want the published posts
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # checks to see if user has liked the post
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            # dictionary object to provide context for the post details
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "commented": False,
                # to add the commentform to the view, we can just add it to the context
                "comment_form": CommentForm()
            },
        )

    # post method in order to be able to post comments
    def post(self, request, slug, *args, **kwargs):
        # status=1 because we only want the published posts
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # checks to see if user has liked the post
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # we have to get the data from the form and assign it to a variable
        # this will get all the data that we posted from our form
        comment_form = CommentForm(data=request.POST)
        # form has a method called is_valid that returns a boolean

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # don't commit the form content to the database yet because we want to assign a post to it
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "You successfully posted a comment.")

        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            # dictionary object to provide context for the post details
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                # to add the commentform to the view, we can just add it to the context
                "comment_form": CommentForm()
            },
        )


class PostLike(View):
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
        # checks to see if user has liked the post
        if post.likes.filter(id=request.user.id).exists():
            # if the like exists, remove the option for the user
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        # when we like or unlike a post, it will reload the page
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))