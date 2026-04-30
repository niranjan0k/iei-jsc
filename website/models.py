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
        ('senior_engineers', 'Senior Engineers Forum'),
    ]

    name = models.CharField(max_length=255, verbose_name='Name')
    designation = models.CharField(max_length=255, verbose_name='Designation')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category')
    photo = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name='Photo')
    sort_order = models.IntegerField(default=0, verbose_name='Sort Order')

    class Meta:
        ordering = ['category', 'sort_order', 'name']
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
