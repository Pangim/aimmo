from django.urls import path

from postings.views import CommentView

urlpatterns =[
    path('/comments/<int:posting_id>', CommentView.as_view()),
    path('/comments', CommentView.as_view())
]