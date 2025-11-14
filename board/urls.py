from django.urls import path, include
from . import views
from .views import *    # 현재 패키지(.)에서 views.py 파일을 가져와 모든 함수와 클래스를 import함

urlpatterns = [
    path('api/board/',board_list,name='board'),    #views.board를 썼더니 from .views import *를 안씀
    path('api/board/<int:pk>/',board_detail,name='detail'),
    path('api/board/post/', board_upload, name='upload'),
    path('api/board/<int:pk>/edit/',board_edit,name='edit'),
    path('api/board/<int:pk>/delete/',board_delete,name='delete'),
    path('api/board/',page_view,name='page_view'),
]

app_name='board'