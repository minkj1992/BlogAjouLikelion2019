from django.shortcuts import render, get_object_or_404
from .models import Profile
# 로그인 해야 profile이 나오도록 한다.
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'profile/home.html')

def about(request):
    return render(request, 'profile/about.html')

@login_required
def portfolio(request):
    # random하게 셔플해준다.
    profiles = Profile.objects.order_by("?")
    return render(request, 'profile/portfolio.html',{'profiles':profiles})

def detail(request, profile_id):
    profile_detail = get_object_or_404(Profile, pk=profile_id)
    return render(request,'profile/detail.html',{'profile':profile_detail})
