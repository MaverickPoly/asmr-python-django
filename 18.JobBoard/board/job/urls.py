from django.urls import path
from . import views


urlpatterns = [
   path("create/", views.create_job, name="create_job"), # Create a new job posting
   path("dashboard/", views.dashboard_view, name="dashboard_view"),
   path("postings/all/", views.all_jobs, name="all_jobs"),

   path("posting/<int:job_id>/edit/", views.edit_job_view, name="edit_job_view"),

   path("search/query/", views.search_view, name="search_view"),
   path("search/filter/<str:filter>/", views.filter_view, name="filter_view"),
   path("sort/<str:query>/", views.sort_view, name="sort_view"),
   
   path("posting/<int:job_id>/", views.job_post_view, name="job_post_view"),
   path("posting/<int:job_id>/apply/", views.apply_job, name="apply_job"),
   
   path("posting/<int:job_id>/applies/", views.job_post_applies, name="job_post_applies"),
   path("posting/<int:job_id>/apply/<int:id>/accept/", views.accept_apply, name="accept_apply"),
   path("posting/<int:job_id>/apply/<int:id>/decline/", views.decline_apply, name="decline_apply"),
]
