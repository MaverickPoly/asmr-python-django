from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from accounts.models import Account
from accounts.views import get_list_data



@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    account = Account.objects.get(user=user)

    context = {
        'current_user': user,
        'account': account,
    }
    return render(request, "profile.html", context=context)


@login_required
def edit_profile_view(request: HttpRequest):
    user = request.user
    account = Account.objects.get(user=user)
    """
    Editable Fields:
    - First, Last Names
    - Bio
    - Profile Image
    - Location
    - Social Links
    - Skills | Organizaion depending on account type
    """

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")
        profileImage = request.FILES.get("profileImage")
        location = request.POST.get("location")
        links = request.POST.getlist("social_links")
        skills = None
        organization = None

        if account.account_type == "job_seeker":
            skills = get_list_data(request, "skill_")
        else:
            organization = request.POST.get("organization")
        
        account.user.first_name = first_name
        account.user.last_name = last_name
        account.bio = bio

        if profileImage:
            # TODO: Implement Old Profile Image Deletion!
            account.profileImage = profileImage
        account.location = location
        account.links = links
        account.skills = skills
        account.organization = organization
        account.save()
        account.user.save()

        messages.success(request, "Profile Updated successfully!")
        return redirect("profile_view", user_id=user.id)
    else:
        context = {
            'current_user': user,
            'account': account,
        }
        return render(request, "edit_profile.html", context=context) 


@login_required
def current_profile(request: HttpRequest):
    return redirect("profile_view", user_id=request.user.id)
