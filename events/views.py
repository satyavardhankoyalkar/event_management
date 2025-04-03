from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from .models import Event, Registration
from .forms import EventForm
import uuid
import qrcode
from io import BytesIO

# 🛠️ Utility Function: Filter Events by Status
def filter_events():
    """Filters events into upcoming, ongoing, and past based on the current date."""
    now = timezone.now().date()
    return {
        "Upcoming": Event.objects.filter(date__gt=now),
        "Ongoing": Event.objects.filter(date=now),
        "Past": Event.objects.filter(date__lt=now),
    }

# 🎯 Event List View
def event_list(request):
    events_by_status = filter_events()

    registered_events = set()
    if request.user.is_authenticated:
        registered_events = set(Registration.objects.filter(user=request.user).values_list('event_id', flat=True))

    context = {
        "events_by_status": events_by_status,
        "registered_events": registered_events,
    }
    return render(request, "events/event_list.html", context)

# 📌 Event Detail View
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = request.user.is_authenticated and Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, "events/event_detail.html", {"event": event, "is_registered": is_registered})

# ✅ Event Creation View
@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/create_event.html", {"form": form})

# 📝 Edit Event
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.organizer:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect("event_list")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, "events/edit_event.html", {"form": form, "event": event})

# ❌ Delete Event
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.organizer:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect("event_list")

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect("event_list")

    return render(request, "events/delete_event.html", {"event": event})

# 🔑 User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("event_list")
    else:
        form = UserCreationForm()

    return render(request, "events/register.html", {"form": form})

# 📝 Register for Event + QR Code Generation
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, f"You are already registered for {event.name}.")
        return redirect("event_detail", event_id=event.id)

    # Generate unique registration ID & QR Code
    registration_id = str(uuid.uuid4())
    qr = qrcode.make(f"Event: {event.name}\nUser: {request.user.username}\nReg ID: {registration_id}")
    qr_io = BytesIO()
    qr.save(qr_io, format="PNG")

    # Save QR Code in Registration Model
    registration = Registration.objects.create(user=request.user, event=event, registration_id=registration_id)
    registration.qr_code.save(f"qr_{registration_id}.png", ContentFile(qr_io.getvalue()), save=True)

    messages.success(request, f"You have successfully registered for {event.name}. Your Registration ID: {registration_id}")
    return redirect("event_detail", event_id=event.id)

# ❌ Unregister from Event
@login_required
def unregister_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration = Registration.objects.filter(user=request.user, event=event).first()

    if registration:
        registration.delete()
        messages.success(request, f"You have successfully unregistered from {event.name}.")
    else:
        messages.info(request, "You are not registered for this event.")

    return redirect("event_detail", event_id=event.id)

# 👥 Event Participants (Organizer Only)
@login_required
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.user != event.organizer:
        messages.error(request, "You are not authorized to view participants for this event.")
        return redirect("event_list")

    participants = Registration.objects.filter(event=event)
    return render(request, "events/participants_list.html", {"event": event, "participants": participants})

# 🚪 User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("event_list")

# 📜 Show User's Registered Events
@login_required
def event_registrations(request):
    status = request.GET.get("status", "all")
    registrations = Registration.objects.filter(user=request.user).select_related("event")

    if status == "upcoming":
        registrations = registrations.filter(event__date__gt=timezone.now().date())
    elif status == "ongoing":
        registrations = registrations.filter(event__date=timezone.now().date())
    elif status == "past":
        registrations = registrations.filter(event__date__lt=timezone.now().date())

    return render(request, "events/event_registrations.html", {"registrations": registrations, "selected_status": status})
