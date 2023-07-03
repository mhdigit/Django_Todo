from rest_framework.routers import DefaultRouter
from .views import TodoListView

app_name = "api-v1"
router = DefaultRouter()
router.register("task", TodoListView, basename="task")


urlpatterns = []

urlpatterns += router.urls
