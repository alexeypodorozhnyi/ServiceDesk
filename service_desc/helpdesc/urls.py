from django.urls import path

from .views import RequestCreate,RequestList,RequestUpdate,CommentCreate,StatusUpdate,RequestDetail,ResolutionUpdate


urlpatterns = [
    path('', RequestList.as_view(), name='request_list_url'),
    path('request_create/',  RequestCreate.as_view(), name='request_create_url'),
    path('request_update/<int:pk>/',  RequestUpdate.as_view(), name='request_update_url'),
    path('request_detail/<int:pk>/',  RequestDetail.as_view(), name='request_detail_url'),
    path('comment_create/',  CommentCreate.as_view(), name='comment_create_url'),
    path('status_update/<int:pk>/',StatusUpdate.as_view(),name='status_update_url'),
    path('resolution_update/<int:pk>/',ResolutionUpdate.as_view(),name='resolution_update_url'),
]
