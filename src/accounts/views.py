from django.contrib.auth.forms import UserCreationForm
from .forms import AuthForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect


# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = AuthForm
    fields = "username", "password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["msg"] = context["form"].errors
        context["form"] = AuthForm()
        return context


class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["msg"] = context["form"].errors
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:task_list")
        return super(RegisterPage, self).get(*args, **kwargs)
