from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from .models import (
    CarouselImage, Announcement, Event, Download,
    Member, LeaderProfile, ContactMessage, Vacancy, Room, GuestBooking
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
            return redirect('/django-admin')
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


def careers(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'website/careers.html', {'vacancies': vacancies})


def guest_house(request):
    rooms = Room.objects.all()
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    num_people = request.GET.get('num_people', '')

    room_availability = []
    searched = False

    if check_in and check_out:
        searched = True
        from datetime import date
        try:
            ci = date.fromisoformat(check_in)
            co = date.fromisoformat(check_out)
            for room in rooms:
                # Check if any booking overlaps with requested dates
                conflicting = room.bookings.filter(
                    check_in__lt=co,
                    check_out__gt=ci,
                )
                room_availability.append({
                    'room': room,
                    'available': not conflicting.exists(),
                })
        except ValueError:
            messages.error(request, 'Invalid date format. Please use the date picker.')
            for room in rooms:
                room_availability.append({'room': room, 'available': None})
    else:
        for room in rooms:
            room_availability.append({'room': room, 'available': None})

    return render(request, 'website/guest_house.html', {
        'room_availability': room_availability,
        'check_in': check_in,
        'check_out': check_out,
        'num_people': num_people,
        'searched': searched,
    })


# ── Careers admin ──────────────────────────────────────────────────────────────

@login_required
def admin_vacancies(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'website/admin_vacancies.html', {'vacancies': vacancies})


@login_required
def admin_vacancy_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        department = request.POST.get('department', '').strip()
        description = request.POST.get('description', '').strip()
        qualifications = request.POST.get('qualifications', '').strip()
        last_date = request.POST.get('last_date') or None
        if title and description:
            Vacancy.objects.create(
                title=title, department=department,
                description=description, qualifications=qualifications,
                last_date=last_date,
            )
            messages.success(request, f'Vacancy "{title}" created successfully.')
            return redirect('admin_vacancies')
        else:
            messages.error(request, 'Title and description are required.')
    return render(request, 'website/admin_vacancy_form.html')


@login_required
def admin_vacancy_delete(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST':
        title = vacancy.title
        vacancy.delete()
        messages.success(request, f'Vacancy "{title}" deleted.')
    return redirect('admin_vacancies')


@login_required
def admin_vacancy_toggle(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    vacancy.is_active = not vacancy.is_active
    vacancy.save()
    return redirect('admin_vacancies')


# ── Guest House admin ──────────────────────────────────────────────────────────

@login_required
def admin_guesthouse(request):
    rooms = Room.objects.prefetch_related('bookings').all()
    bookings = GuestBooking.objects.select_related('room').order_by('-check_in')
    today = timezone.now().date()
    return render(request, 'website/admin_guesthouse.html', {
        'rooms': rooms,
        'bookings': bookings,
        'today': today,
    })


@login_required
def admin_booking_add(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        room_id = request.POST.get('room')
        guest_name = request.POST.get('guest_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        num_people = request.POST.get('num_people', 1)
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        notes = request.POST.get('notes', '').strip()
        if room_id and guest_name and check_in and check_out:
            room = get_object_or_404(Room, pk=room_id)
            GuestBooking.objects.create(
                room=room, guest_name=guest_name,
                contact_number=contact_number, num_people=num_people,
                check_in=check_in, check_out=check_out, notes=notes,
            )
            messages.success(request, f'Booking for {guest_name} added.')
            return redirect('admin_guesthouse')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'website/admin_booking_form.html', {'rooms': rooms})


@login_required
def admin_booking_delete(request, pk):
    booking = get_object_or_404(GuestBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted.')
    return redirect('admin_guesthouse')
