from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

# from .forms import TaskUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views import View

from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/main.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tasks'] = context['tasks'].filter(user=self.request.user)
        total = context['tasks'].count()
        complete = context['tasks'].filter(complete=True).count()
        remaining = total - complete
        context['stats'] = {
            'total': total,
            'complete':complete,
            'remaining':remaining,
        }


        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


# class TaskUpdate(LoginRequiredMixin, UpdateView):
#     http_method_names = ['post']
#     model = Task
#     success_url = reverse_lazy("todo:task_list")
#     fields = ['complete']



#     def post(self, request, *args, **kwargs):

#         return super().post(request, *args, **kwargs)
    # form_class = TaskUpdateForm
    # template_name = "todo/update_task.html"
    


class TaskUpdate(LoginRequiredMixin, View):
    # http_method_names = ['post']
    model = Task
    success_url = reverse_lazy("todo:task_list")


    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs.get("pk"))
      
        if 'complete' in request.POST.keys() :
            complete = int(request.POST.get('complete'))
            print(complete,type(complete))
            if complete:
                obj.complete = True
            else:
                obj.complete = False
            obj.save()

        if 'title' in request.POST.keys() :
            title = str(request.POST.get('title'))
            obj.title = title
            obj.save()




        return redirect(self.success_url)


class DeleteView(LoginRequiredMixin, DeleteView):
    # http_method_names = ['post']
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task_list")

    # https://stackoverflow.com/questions/17475324/django-deleteview-without-confirmation-template

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)