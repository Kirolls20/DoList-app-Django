from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Task,TaskManager
from .forms import CreateUserForm,CreateTasksForm
from django.urls import reverse,reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # To disable the CSRF token in likeView 
from django.utils.decorators import method_decorator
class TaskManagerView(LoginRequiredMixin,ListView):
   template_name = 'base/task_manager_home.html'
   model= TaskManager
   context_object_name= 'tasks_manager'

class CreateTaskManager(LoginRequiredMixin,TemplateView):
   template_name = 'base/create_task_manager.html'

   def post(self,request,**kwargs):
      user = self.request.user
      if self.request.method == 'POST':
         task = self.request.POST['task']
         if task:
            form = TaskManager(name=task,user=user)
            form.save()
            messages.success(self.request,'New Task Added!')
            return redirect('tasks_manager')
         else:
            messages.error(self.request,'Faild To add the Task try again..')
            return redirect('new')

class DeleteTaskManagerView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
   template_name = 'base/task_manager_home.html'
   model= TaskManager
   success_message = ('Task Deleted!')

   def get_success_url(self):
      return reverse_lazy('tasks_manager')

class EditTaskManagerView(LoginRequiredMixin,SuccessMessageMixin,TemplateView):
   template_name = 'base/edit_task_manager.html'

   def get(self,request,**kwargs):
      user = self.request.user
      task_id = self.kwargs['pk']
      task = TaskManager.objects.get(id=task_id,user=user)
      return render(self.request,self.template_name,{'task':task})

   def post(self,request,**kwargs):
      user = self.request.user
      if self.request.method == 'POST':
         task_id = self.kwargs['pk']
         if task_id:
            try:
               task = TaskManager.objects.get(id=task_id,user=user)
            except TaskManager.DoesNotExist:
               messages.error(self.request, 'Task not found.')
               return redirect('tasks_manager')
            task_name = self.request.POST.get('task')
            task.name= task_name
            task.save()
            messages.success(self.request,'Task Updated!')
            return redirect('tasks_manager')
         else:
            messages.error(self.request,'Faild to Updated the task!')
            return redirect('tasks_manager')

class TaskManagerDetailsView(LoginRequiredMixin,TemplateView):
   template_name = 'base/task_list.html'

   def get_context_data(self,**kwargs):
      context = super().get_context_data(**kwargs)
      task_id= self.kwargs['pk']
      user = self.request.user
      context['task_id'] = task_id
      context['task_list'] = Task.objects.filter(user=user,task_manager=task_id)
      context["count"] = Task.objects.filter(complete=False,user=self.request.user,task_manager=task_id).count()
      search_input=self.request.GET.get('search_txt')
      if search_input:
         context['tasks'] = Task.objects.filter(title__icontains=search_input)
      return context

   def post(self,request,**kwargs):
      task = TaskManager.objects.get(id=self.kwargs['pk'],user=self.request.user)
      tasks= Task.objects.filter(user=self.request.user,task_manager=task)
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

class TaskCreateView(LoginRequiredMixin,CreateView):
   template_name='base/task_create.html'
   form_class = CreateTasksForm

   def form_valid(self,form,**kwargs):
      task_id = self.kwargs['pk']
      form  = form.save(commit = False)
      form.user = self.request.user
      form.task_manager = TaskManager.objects.get(id=self.kwargs['pk'],user=self.request.user)
      form.save()
      messages.success(self.request,'Task Added to the list!')
      return super().form_valid(form)
   
   def get_success_url(self,**kwargs):
      task_id = self.kwargs['pk']
      return reverse('task_list',args=(task_id,))
class EditTaskView(LoginRequiredMixin, UpdateView):
   template_name = 'base/task_update.html'
   model = Task
   form_class = CreateTasksForm
 
   def form_valid(self, form, **kwargs):
      form = form.save(commit=False)
      form.user = self.request.user
      form.save()
      messages.success(self.request, 'Task Updated!')
      return super().form_valid(form, **kwargs)

   def get_success_url(self, **kwargs):
        task_id = self.kwargs['pk']
        task_manager_pk = Task.objects.get(id=task_id).task_manager.id
        return reverse('task_list', kwargs={'pk': task_manager_pk})

class DeleteTaskView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
   template_name= 'base/task_list.html'  
   model = Task
   success_message = ('Task Deleted!')

   def get_success_url(self,**kwargs):
      task_id = self.kwargs['pk']
      task_manager_pk = Task.objects.get(id=task_id).task_manager.id
      return reverse('task_list',kwargs={'pk':task_manager_pk})
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTaskStatusView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        
        # Toggle the completion status
        task.complete = not task.complete
        task.save()

        return JsonResponse({'task_status': task.complete})
class CreateUserView(CreateView):
   template_name='registration/sign-up.html'
   form_class=CreateUserForm

   def get_success_url(self):
      return reverse_lazy('login')



   


class TaskDeleteView(LoginRequiredMixin,DeleteView):
   template_name='base/task_delete.html'
   model=Task

   def get_success_url(self):
      return reverse_lazy('task_list')
