from rest_framework.routers import DefaultRouter
from .views import TodoListView

router = DefaultRouter()
router.register("task", TodoListView, basename="task_list")


urlpatterns = []

urlpatterns += router.urls
