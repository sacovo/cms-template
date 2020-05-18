from django.urls import path

from cms import views

app_name = "pages"

urlpatterns = (
    path('<path:path>/', views.page_detail, name="page"),
    path('', views.page_detail, name="root"),
)
