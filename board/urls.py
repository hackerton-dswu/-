from django.urls import path, include
from . import views
from .views import (board_list, board_detail, board_upload, board_edit, board_delete, page_view, like
)    # 현재 패키지(.)에서 views.py 파일을 가져와 모든 함수와 클래스를 import함

urlpatterns = [
    path('api/board/',board_list,name='board'),    #views.board를 썼더니 from .views import *를 안씀
    path('api/board/<int:pk>/',board_detail,name='detail'),
    path('api/board/post/', board_upload, name='upload'),
    path('api/board/<int:pk>/edit/',board_edit,name='edit'),
    path('api/board/<int:pk>/delete/',board_delete,name='delete'),
    path('board/',page_view,name='page_view'),
    path('api/board/<int:pk>/like/',like,name='like'),
]

app_name='board'