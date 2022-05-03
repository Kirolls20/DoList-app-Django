from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from .forms import CreateUserForm
from django.urls import reverse,reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



class CreateUserView(CreateView):
   template_name='registration/sign-up.html'
   form_class=CreateUserForm

   def get_success_url(self):
      return reverse_lazy('login')

class TaskList(LoginRequiredMixin,ListView):
   model=Task
   template_name='base/task_list.html'
   context_object_name='tasks'

   def post(self,request):
      tasks= Task.objects.filter(user=self.request.user)
      #item_id= Task.objects.get(pk=id)
      if request.method == 'POST':
         if request.POST.get('save'):
            for task in tasks:
               if request.POST.get("c" + str(task.id)) == "clicked":
                  task.complete=True
               else:
                  task.complete=False
               task.save()
      return render(request,'base/task_list.html',{'tasks':tasks})

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tasks'] = Task.objects.filter(user=self.request.user)
      context["count"] = Task.objects.filter(complete=False,user=self.request.user).count()
      search_input=self.request.GET.get('search_txt')
      if search_input:
         context['tasks'] = Task.objects.filter(title__icontains=search_input)
      return context



class TaskCreateView(LoginRequiredMixin,CreateView):
   template_name='base/task_create.html'
   model=Task
   fields=['title','description','complete']

   def form_valid(self, form):
      obj= form.save(commit=False)
      obj.user = self.request.user
      obj.save()
      return super(TaskCreateView,self).form_valid(form)
   
   def get_success_url(self):
      return reverse_lazy('task_list')


class TaskEditView(LoginRequiredMixin,UpdateView):
   template_name='base/task_update.html'
   model=Task
   fields=['title','description','complete']

   def get_success_url(self):
      return reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin,DeleteView):
   template_name='base/task_delete.html'
   model=Task

   def get_success_url(self):
      return reverse_lazy('task_list')
