from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone

def task_list(request):
    tasks = Task.objects.filter(completed=False).order_by('due_date')  # 未完了のタスクを期限が近い順に
    completed_tasks = Task.objects.filter(completed=True).order_by('completed_date')  # 完了したタスクを完了日順に取得

    # 完了したタスクが10件を超えている場合、期限の古いものから削除する
    if completed_tasks.count() > 10:
        tasks_to_delete = completed_tasks[10:]  # 10件目以降のタスク
        # 削除対象を特定してから削除
        for task in tasks_to_delete:
            task.delete()
    
    return render(request, "todo/task_list.html", {"tasks": tasks, "completed_tasks": completed_tasks[:10]})  # 完了したタスクは最大10件表示

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "todo/add_task.html", {"form": form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    
    return render(request, "todo/edit_task.html", {"form": form})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("task_list")

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.completed_date = timezone.now()  # 完了日を現在時刻で設定
    task.save()
    return redirect("task_list")

def delete_completed_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")