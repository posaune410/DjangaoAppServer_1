from django.urls import path

from . import views
from . import initSetData

urlpatterns = [
    path("regist/", views.regist_attendance, name="regist"),
    path("status/", views.return_status, name="status"),
    path("children/", views.return_children, name="children"),
    path("updatereply/", views.update_reply, name="updatereply"),
    # path('api/', apis.api.as_view(), name = "api")
]