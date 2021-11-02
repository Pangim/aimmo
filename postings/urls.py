from django.urls import path

from postings.views import PostingView, PostingListView, CommentView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:posting_id>', PostingView.as_view()),
    path('/list', PostingListView.as_view()),
    path('/comments/<int:posting_id>', CommentView.as_view()),
    path('/comments', CommentView.as_view())
]