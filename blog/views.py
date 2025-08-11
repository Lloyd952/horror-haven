from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag
from .forms import CommentForm
from .models import Review, Comment


def post_list(request):
    """
    The request parameter is required by all views!
    Here we get all reviews using our custom manager (i.e the PublishedManager)
    It retrieves all reviews with a status of PUBLISHED
    """
    review_list = Review.published.all()
    # Pagination with 3 reviews per page
    paginator = Paginator(review_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        reviews = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        reviews = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': reviews}
    )


def post_detail(request, year, month, day, post):
    """
    This review detail view takes the id arguement of a review. It uses the
    get_object_or_404 shortcut.
    If the review is not found a HTTP 404 exception is raised.
    """
    post = get_object_or_404(
        Review,
        status=Review.Status.PUBLISHED,
        slug=post,
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    )

    comments = post.comments.filter(is_active=True)
    form = CommentForm()
    most_commented_posts = Review.published.most_commented()
    highest_rated = Review.published.highest_rated()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'most_commented_posts': most_commented_posts,
            'highest_rated': highest_rated
        }
    )


class PostListView(ListView):
    """
    Alternative review list view
    """
    queryset = Review.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        queryset = Review.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        else:
            self.tag = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['most_commented_posts'] = Review.published.most_commented()
        context['highest_rated'] = Review.published.highest_rated()
        return context


@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Review, id=post_id, status=Review.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect(post.get_absolute_url())
    else:
        comments = post.comments.filter(is_active=True)
        return render(
            request,
            'blog/post/detail.html',
            {
                'post': post,
                'comments': comments,
                'form': form
            }
        )


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    
    return render(
        request,
        'blog/post/comment/edit_comment.html',
        {'form': form, 'comment': comment}
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect(comment.post.get_absolute_url())
    
    return render(
        request,
        'blog/post/comment/delete_comment.html',
        {'comment': comment}
    )
