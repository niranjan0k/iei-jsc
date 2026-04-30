from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import (
    CarouselImage, Announcement, Event, Download,
    Member, LeaderProfile, ContactMessage
)
from .forms import ContactForm


def home(request):
    carousels = CarouselImage.objects.all()
    announcements = Announcement.objects.filter(is_active=True)[:10]
    events = Event.objects.all()[:6]
    chairman = LeaderProfile.objects.filter(role='chairman').first()
    secretary = LeaderProfile.objects.filter(role='secretary').first()
    return render(request, 'website/home.html', {
        'carousels': carousels,
        'announcements': announcements,
        'events': events,
        'chairman': chairman,
        'secretary': secretary,
    })


def about(request):
    chairman = LeaderProfile.objects.filter(role='chairman').first()
    secretary = LeaderProfile.objects.filter(role='secretary').first()
    return render(request, 'website/about.html', {
        'chairman': chairman,
        'secretary': secretary,
    })


def members(request):
    executive = Member.objects.filter(category='executive')
    subcommittee = Member.objects.filter(category='subcommittee')
    senior = Member.objects.filter(category='senior_engineers')
    return render(request, 'website/members.html', {
        'executive': executive,
        'subcommittee': subcommittee,
        'senior': senior,
    })


def events(request):
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 9)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'website/events.html', {'page_obj': page_obj})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    photos = event.photos.all()
    return render(request, 'website/event_detail.html', {
        'event': event,
        'photos': photos,
    })


def downloads(request):
    docs = Download.objects.all()
    return render(request, 'website/downloads.html', {'docs': docs})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been received. We will get back to you shortly.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_portal')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_portal')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'website/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin_portal(request):
    stats = {
        'carousel_count': CarouselImage.objects.count(),
        'announcement_count': Announcement.objects.filter(is_active=True).count(),
        'event_count': Event.objects.count(),
        'member_count': Member.objects.count(),
        'download_count': Download.objects.count(),
        'message_count': ContactMessage.objects.filter(is_read=False).count(),
    }
    recent_messages = ContactMessage.objects.order_by('-received_at')[:5]
    recent_events = Event.objects.all()[:5]
    recent_members = Member.objects.all()[:6]
    return render(request, 'website/admin_portal.html', {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_events': recent_events,
        'recent_members': recent_members,
    })
