from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Job, JobApply
from accounts.models import Account



#  - BASIC
@login_required
def create_job(request: HttpRequest):
    user = request.user
    account = Account.objects.get(user=user)
    if account.account_type != "employer":
        messages.error(request, "Only employers can create job posts!")
        return redirect("dashboard_view")
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        tags = request.POST.getlist("tags")
        image = request.FILES.get("image")

        print(f"Tags creating job: {tags}")

        job = Job.objects.create(
            title=title, 
            description=description, 
            tags=tags, 
            image=image, 
            author=request.user
        )
        job.save()
        messages.success(request, "Job created successfully!")
        return redirect("dashboard_view")
    else:
        return render(request, "create_job.html")
    

@login_required
def dashboard_view(request: HttpRequest):
    user = request.user
    account = Account.objects.get(user=user)
    if account.account_type == "employer":
        jobs = Job.objects.filter(author=request.user).order_by("created_at")
        context = {
            "jobs": jobs
        }
        print(request.user.account)
        return render(request, "dashboard_employer.html", context)
    else:
        applies = JobApply.objects.filter(user=request.user).order_by("created_at")
        context = {
            "applies": applies
        }
        return render(request, "dashboard_job_seeker.html", context)
    
@login_required
def all_jobs(request: HttpRequest):
    jobs = Job.objects.all().order_by("created_at")
    context = {
        "jobs": jobs
    }
    return render(request, "all_jobs.html", context)

#  - EDIT
@login_required
def edit_job_view(request: HttpRequest, job_id: int):
    job = get_object_or_404(Job, id=job_id)
    if job.author != request.user:
        messages.error(request, "You do not have permission to edit this job!")
        return redirect("dashboard_view")
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        tags = request.POST.getlist("tags")
        image = request.FILES.get("image")

        # TODO: Remove old image before saving
        job.title = title
        job.description = description
        job.tags = tags
        job.image = image
        job.save()

        messages.success(request, "Job updated successfully!")
        return redirect("dashboard_view")
    else:
        return render(request, "edit_job_post.html")


#  - SEARCH | FILTER | SORT
@login_required
def search_view(request:HttpRequest):
    query = request.GET.get("query")
    if not query:
        return redirect("dashboard_view")
    jobs = Job.objects.filter(
        title__icontains=query, 
        description__icontains=query, 
        tags__icontains=query
    )
    context = {
        "jobs": jobs,
        "query": query,
    }
    return render(request, "search_results.html", context)

@login_required
def filter_view(request: HttpRequest, filter: str):
    supported_filters = [
        ""
    ]


@login_required
def sort_view(request: HttpRequest, query: str):
    supported_sorts = [
        "created_at", "updated_at", "accepted_users", "name"
    ]
    if query not in supported_sorts:
        messages.warning(request, "Invalid sort option!")
        return redirect("dashboard_view")
    sorted_jobs = Job.objects.all().order_by(query)
    context = {
        "sorted_jobs": sorted_jobs,
        "sort_query": query,
    }
    return render(request, "sorted_jobs.html", context)


#  - APPLICATIONS
@login_required
def job_post_view(request: HttpRequest, job_id: int):
    job = get_object_or_404(Job, id=job_id)
    context = {
        "job": job,
    }
    return render(request, "job_post.html", context)


@login_required
def apply_job(request: HttpRequest, job_id=int):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        apply = JobApply.objects.create(
            job=job,
            comment=comment,
            status="pending",
            user=request.user
        )
        apply.save()
        messages.success(request, "Application submitted successfully!")
        return redirect("job_post_view", job_id=job_id)
    else:
        context = {
            "job": job,
        }
        return render(request, "apply_job.html", context)
    
@login_required
def job_post_applies(request: HttpRequest, job_id: int):
    query = request.GET.get("query")
    job = get_object_or_404(Job, id=job_id)
    if query == "approved":
        applies = job.applications.filter(status="approved").order_by("created_at")
    elif query == "declined":
        applies = job.applications.filter(status="declined").order_by("created_at")
    elif query == "pending":
        applies = job.applications.filter(status="pending").order_by("created_at")
    else:
        applies = job.applications.all().order_by("created_at")
    context = {
        "job": job,
        "applies": applies
    }
    return render(request, "job_post_applies.html", context)

@login_required
@require_http_methods(["PATCH"])
def accept_apply(request: HttpRequest, job_id: int):
    pass

@login_required
@require_http_methods(["PATCH"])
def decline_apply(request: HttpRequest, job_id: int):
    pass


