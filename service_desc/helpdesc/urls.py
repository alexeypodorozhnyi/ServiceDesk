from django.urls import path

from .views import RequestCreate,RequestList,RequestUpdate,CommentCreate,StatusUpdate


urlpatterns = [
    path('', RequestList.as_view(), name='request_list_url'),
    path('request_create/',  RequestCreate.as_view(), name='request_create_url'),
    path('request_update/<int:pk>/',  RequestUpdate.as_view(), name='request_update_url'),
    path('comment_create/',  CommentCreate.as_view(), name='comment_create_url'),
    path('status_update/<int:pk>/',StatusUpdate.as_view(),name='status_update_url'),
]
