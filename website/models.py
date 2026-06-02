from django.db import models
from django.utils import timezone


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/', verbose_name='Image')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Caption')
    sort_order = models.IntegerField(default=0, verbose_name='Sort Order')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['sort_order', 'created_at']
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'

    def __str__(self):
        return self.caption or f'Image #{self.id}'


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    link = models.URLField(blank=True, null=True, verbose_name='Link URL')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name='Event Name')
    description = models.TextField(verbose_name='Description')
    event_date = models.DateField(verbose_name='Event Date')
    cover_image = models.ImageField(upload_to='events/covers/', blank=True, null=True, verbose_name='Cover Image')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name

    def photo_count(self):
        return self.photos.count()


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='events/photos/', verbose_name='Photo')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Caption')

    class Meta:
        verbose_name = 'Event Photo'
        verbose_name_plural = 'Event Photos'

    def __str__(self):
        return f'{self.event.name} - Photo {self.id}'


class Download(models.Model):
    name = models.CharField(max_length=255, verbose_name='Document Name')
    file = models.FileField(upload_to='downloads/', verbose_name='File')
    file_type = models.CharField(max_length=50, blank=True, verbose_name='File Type')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file and not self.file_type:
            ext = self.file.name.split('.')[-1].upper()
            self.file_type = ext
        super().save(*args, **kwargs)


class Member(models.Model):
    CATEGORY_CHOICES = [
        ('executive', 'Executive Committee'),
        ('subcommittee', 'Sub Committee'),
        ('senior_members', 'Senior Members'),
    ]
    SUB_COMMITTEE_CHOICES = [
        ('advisory', 'Advisory Committee'),
        ('website_edisha', 'Website & e-Disha Committee'),
        ('infrastructure', 'Infrastructure Committee'),
        ('finance', 'Finance Committee'),
        ('technical_chapter', 'Technical Chapter Committee'),
        ('technical_program_award', 'Technical Program Award Committee'),
        ('senior_engineer_committee', 'Senior Engineer Committee'),
    ]
    name = models.CharField(max_length=255, verbose_name='Name')
    designation = models.CharField(max_length=255, verbose_name='Designation')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category')
    sub_committee_type = models.CharField(
        max_length=50, choices=SUB_COMMITTEE_CHOICES,
        blank=True, null=True, verbose_name='Sub Committee Type',
        help_text='Only applicable when Category is "Sub Committee"'
    )
    photo = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=20, blank=True, verbose_name='Mobile No')
    membership_no = models.CharField(max_length=50, blank=True, verbose_name='Membership No')
    sort_order = models.IntegerField(default=0, verbose_name='Sort Order')

    class Meta:
        ordering = ['category', 'sort_order', 'name', 'mobile_no', 'membership_no']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'


class LeaderProfile(models.Model):
    ROLE_CHOICES = [
        ('chairman', 'Chairman'),
        ('secretary', 'Secretary'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True, verbose_name='Role')
    name = models.CharField(max_length=255, verbose_name='Name')
    title = models.CharField(max_length=255, verbose_name='Official Title')
    bio = models.TextField(verbose_name='Short Profile / Bio')
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True, verbose_name='Photograph')

    class Meta:
        verbose_name = 'Leadership Profile'
        verbose_name_plural = 'Leadership Profiles'

    def __str__(self):
        return f'{self.get_role_display()} - {self.name}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    received_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-received_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Vacancy(models.Model):
    title = models.CharField(max_length=255, verbose_name='Job Title')
    department = models.CharField(max_length=255, blank=True, verbose_name='Department')
    description = models.TextField(verbose_name='Job Description')
    qualifications = models.TextField(blank=True, verbose_name='Qualifications Required')
    last_date = models.DateField(blank=True, null=True, verbose_name='Application Last Date')
    is_active = models.BooleanField(default=True, verbose_name='Active / Visible')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name='Room Name')
    description = models.TextField(blank=True, verbose_name='Description')
    room_number = models.CharField(max_length=10, verbose_name='Room Number')

    class Meta:
        ordering = ['room_number']
        verbose_name = 'Guest Room'
        verbose_name_plural = 'Guest Rooms'

    def __str__(self):
        return f'{self.name} (Room {self.room_number})'


class GuestBooking(models.Model):
    STATUS_CHOICES = [
        ('occupied', 'Occupied'),
        ('free', 'Free / Available'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', verbose_name='Room')
    guest_name = models.CharField(max_length=255, verbose_name='Guest Name')
    contact_number = models.CharField(max_length=20, verbose_name='Contact Number')
    num_people = models.PositiveIntegerField(default=1, verbose_name='Number of Guests')
    check_in = models.DateField(verbose_name='Check-In Date')
    check_out = models.DateField(verbose_name='Check-Out Date')
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-check_in']
        verbose_name = 'Guest Booking'
        verbose_name_plural = 'Guest Bookings'

    def __str__(self):
        return f'{self.guest_name} — {self.room.name} ({self.check_in} to {self.check_out})'