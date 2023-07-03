from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from ..models import Task

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="usertest", password="m@123123", is_active=True
    )
    return user


@pytest.fixture
def common_task(common_user):
    task = Task.objects.create(
        user=common_user, title="test_title", complete=True
    )
    return task


@pytest.mark.django_db
class TestTaskApi:

    # ========================== Read =========================================

    def test_get_task_response_200_status(self, api_client, common_user, common_task):

        url = reverse("todo:api-v1:task-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert common_task.title in response.json()[0].values()
        assert response.status_code == 200

    def test_get_task_detail_response_200_status(self, api_client, common_user, common_task):

        url = reverse("todo:api-v1:task-detail", kwargs={'pk': common_task.id})
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert common_task.title in response.json().values()
        assert response.status_code == 200

    # ========================= create ========================================

    def test_create_task_response_403_status(self, api_client, common_task):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
            "complete": True,

        }
        response = api_client.post(url, data)
        assert response.status_code == 403

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "user": common_user,
            "title": "test",
            "complete": True,

        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert data['title'] == response.json()['title']
        assert response.status_code == 201

    def test_create_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "test",
            "complete": 'test',

        }
        user = common_user

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    #  =================== update ==========================================

    def test_update_task_response_200_status(self, api_client, common_user, common_task):

        url = reverse("todo:api-v1:task-detail", kwargs={'pk': common_task.id})
        user = common_user
        api_client.force_authenticate(user=user)
        data = {'title': 'title_edited'}

        response = api_client.patch(url, data)
        assert data['title'] == response.json()['title']
        assert response.status_code == 200

    # =================== delete ==========================================
    def test_update_task_response_204_status(self, api_client, common_user, common_task):
        assert Task.objects.count() == 1
        url = reverse("todo:api-v1:task-detail", kwargs={'pk': common_task.id})
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert Task.objects.count() == 0
        assert response.status_code == 204
