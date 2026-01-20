from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Max, Count
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Custom User Model
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )
    profile_picture = models.ImageField(
        upload_to='images/profile_pics',
        null=True,
        blank=True,
    )

    def is_admin(self):
        """Returns True if the user is an admin."""
        return self.role == 'admin'

    def is_user(self):
        """Returns True if the user is a regular user."""
        return self.role == 'user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class UserLogin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


# Instrument Category Model
class InstrumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='fa-music') 
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Indigenous Region Model
class Region(models.Model):
    REGION_CHOICES = [
        # Luzon
        ('Ilocos Region', 'Ilocos Region (Region I)'),
        ('Cagayan Valley', 'Cagayan Valley (Region II)'),
        ('Central Luzon', 'Central Luzon (Region III)'),
        ('CALABARZON', 'CALABARZON (Region IV-A)'),
        ('MIMAROPA', 'MIMAROPA (Region IV-B)'),
        ('Bicol Region', 'Bicol Region (Region V)'),

        # Visayas
        ('Western Visayas', 'Western Visayas (Region VI)'),
        ('Central Visayas', 'Central Visayas (Region VII)'),
        ('Eastern Visayas', 'Eastern Visayas (Region VIII)'),

        # Mindanao
        ('Zamboanga Peninsula', 'Zamboanga Peninsula (Region IX)'),
        ('Northern Mindanao', 'Northern Mindanao (Region X)'),
        ('Davao Region', 'Davao Region (Region XI)'),
        ('SOCCSKSARGEN', 'SOCCSKSARGEN (Region XII)'),
        ('Caraga', 'Caraga (Region XIII)'),

        # Special/Autonomous
        ('Cordillera Administrative Region', 'Cordillera Administrative Region (CAR)'),
        ('Bangsamoro', 'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)'),
    ]

    name = models.CharField(
        max_length=100,
        choices=REGION_CHOICES,
        unique=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Material Model
class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


from django.db import models
from django.urls import reverse

PH_PROVINCES = (
    ('Abra', 'Abra'),
    ('Agusan del Norte', 'Agusan del Norte'),
    ('Agusan del Sur', 'Agusan del Sur'),
    ('Aklan', 'Aklan'),
    ('Albay', 'Albay'),
    ('Antique', 'Antique'),
    ('Apayao', 'Apayao'),
    ('Aurora', 'Aurora'),
    ('Basilan', 'Basilan'),
    ('Bataan', 'Bataan'),
    ('Batanes', 'Batanes'),
    ('Batangas', 'Batangas'),
    ('Biliran', 'Biliran'),
    ('Benguet', 'Benguet'),
    ('Bohol', 'Bohol'),
    ('Bukidnon', 'Bukidnon'),
    ('Bulacan', 'Bulacan'),
    ('Cagayan', 'Cagayan'),
    ('Camarines Norte', 'Camarines Norte'),
    ('Camarines Sur', 'Camarines Sur'),
    ('Camiguin', 'Camiguin'),
    ('Capiz', 'Capiz'),
    ('Catanduanes', 'Catanduanes'),
    ('Cavite', 'Cavite'),
    ('Cebu', 'Cebu'),
    ('Compostela Valley', 'Compostela Valley'),
    ('Cotabato', 'Cotabato'),
    ('Davao de Oro', 'Davao de Oro'),
    ('Davao del Norte', 'Davao del Norte'),
    ('Davao del Sur', 'Davao del Sur'),
    ('Davao Occidental', 'Davao Occidental'),
    ('Davao Oriental', 'Davao Oriental'),
    ('Dinagat Islands', 'Dinagat Islands'),
    ('Eastern Samar', 'Eastern Samar'),
    ('Guimaras', 'Guimaras'),
    ('Ifugao', 'Ifugao'),
    ('Ilocos Norte', 'Ilocos Norte'),
    ('Ilocos Sur', 'Ilocos Sur'),
    ('Iloilo', 'Iloilo'),
    ('Isabela', 'Isabela'),
    ('Kalinga', 'Kalinga'),
    ('La Union', 'La Union'),
    ('Laguna', 'Laguna'),
    ('Lanao del Norte', 'Lanao del Norte'),
    ('Lanao del Sur', 'Lanao del Sur'),
    ('Leyte', 'Leyte'),
    ('Maguindanao', 'Maguindanao'),
    ('Marinduque', 'Marinduque'),
    ('Masbate', 'Masbate'),
    ('Misamis Occidental', 'Misamis Occidental'),
    ('Misamis Oriental', 'Misamis Oriental'),
    ('Mountain Province', 'Mountain Province'),
    ('Negros Occidental', 'Negros Occidental'),
    ('Negros Oriental', 'Negros Oriental'),
    ('Northern Samar', 'Northern Samar'),
    ('Nueva Ecija', 'Nueva Ecija'),
    ('Nueva Vizcaya', 'Nueva Vizcaya'),
    ('Occidental Mindoro', 'Occidental Mindoro'),
    ('Oriental Mindoro', 'Oriental Mindoro'),
    ('Palawan', 'Palawan'),
    ('Pampanga', 'Pampanga'),
    ('Pangasinan', 'Pangasinan'),
    ('Quezon', 'Quezon'),
    ('Quirino', 'Quirino'),
    ('Rizal', 'Rizal'),
    ('Romblon', 'Romblon'),
    ('Samar', 'Samar'),
    ('Sarangani', 'Sarangani'),
    ('Siquijor', 'Siquijor'),
    ('Sorsogon', 'Sorsogon'),
    ('South Cotabato', 'South Cotabato'),
    ('Southern Leyte', 'Southern Leyte'),
    ('Sultan Kudarat', 'Sultan Kudarat'),
    ('Sulu', 'Sulu'),
    ('Surigao del Norte', 'Surigao del Norte'),
    ('Surigao del Sur', 'Surigao del Sur'),
    ('Tarlac', 'Tarlac'),
    ('Tawi-Tawi', 'Tawi-Tawi'),
    ('Zambales', 'Zambales'),
    ('Zamboanga del Norte', 'Zamboanga del Norte'),
    ('Zamboanga del Sur', 'Zamboanga del Sur'),
    ('Zamboanga Sibugay', 'Zamboanga Sibugay'),
)

class Instrument(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.ForeignKey('InstrumentCategory', on_delete=models.CASCADE, related_name='instruments')
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True, related_name='instruments')
    province = models.CharField(max_length=50, choices=PH_PROVINCES, blank=True, null=True)
    image = models.ImageField(upload_to='images/instruments/images/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("admin_main")

class InstrumentLink(models.Model):
    LINK_TYPES = [
        ('info', 'Information Source'),
        ('video', 'Video'),
        ('audio', 'Audio Sample'),
        ('image', 'Image Source'),
        ('research', 'Research Paper'),
        ('museum', 'Museum Link'),
        ('other', 'Other'),
    ]
    
    instrument = models.ForeignKey(
        'Instrument', 
        on_delete=models.CASCADE, 
        related_name='links'
    )
    title = models.CharField(max_length=200, help_text="Link title or description")
    url = models.URLField(max_length=500)
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='info')
    is_primary_source = models.BooleanField(default=False, help_text="Mark as main information source")
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary_source', 'link_type', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.instrument.name}"

class Instrument3DModel(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        related_name='three_d'
    )
    file = models.FileField(
        upload_to='images/instruments/3d_models/',
        blank=True,
        null=True,
        help_text="Upload a 3D model file (.glb, .gltf)"
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"3D Model for {self.instrument.name}"
    
class Site3DContent(models.Model):
    hero_title = models.CharField(max_length=200, default="Discover Philippine Traditional Instruments")
    hero_description = models.TextField(default="Explore our gallery of authentic Filipino musical heritage with sound samples")
    about_title = models.CharField(max_length=200, default="Preserving Philippine Musical Heritage")
    about_content = models.TextField(default="This project aims to digitally preserve and showcase the rich variety of traditional Philippine musical instruments through images and authentic sound recordings.")
    about_image = models.ImageField(upload_to='images/site_content/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Site Content"
    
    def __str__(self):
        return "Site Content Configuration"


class InstrumentPage(models.Model):
    instrument = models.ForeignKey(Instrument, related_name='pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Get the highest order number for this instrument's pages
            last_page = InstrumentPage.objects.filter(
                instrument=self.instrument
            ).order_by('-order').first()
            self.order = (last_page.order + 1) if last_page else 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.instrument.name} - {self.title}"

class PageSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ('description', 'Description'),
        ('bullet_points', 'Bullet Points'),
        ('image', 'Image'),
        ('quote', 'Quote'),
    ]
    
    page = models.ForeignKey(InstrumentPage, related_name='sections', on_delete=models.CASCADE)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/page_sections/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Get the highest order number for this page's sections
            last_section = PageSection.objects.filter(
                page=self.page
            ).order_by('-order').first()
            self.order = (last_section.order + 1) if last_section else 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.page.title} - {self.get_section_type_display()} - {self.title or 'No Title'}"

class Sound(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    sound_sample = models.FileField(upload_to='images/instruments/sounds/', blank=True, null=True)
    # date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Instrument Material Model
class InstrumentMaterial(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, related_name='instruments')  # Many-to-Many Relationship
    description = models.TextField(blank=True)

    def __str__(self):
        return self.instrument.name
    

class Tagline(models.Model):
    icon = models.CharField(max_length=50, default='music')
    title = models.CharField(max_length=100, default="PHILHARMONIA MUSIC")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure there's only one instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class HomePage(models.Model):
    main_heading = models.CharField(max_length=200, default="Experience Traditional Filipino")
    highlight_word = models.CharField(max_length=50, default="Music")
    description = models.TextField(default="Explore our web-based platform featuring an interactive map, visual galleries, educational tutorials, and 3D models all dedicated to preserving and promoting traditional Filipino music and heritage.")
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.main_heading
    
class ConstructionStep(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  # Now editable
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ['instrument', 'order']  # Prevent duplicate orders
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 0:  # Only for new instances with no order specified
            last_order = ConstructionStep.objects.filter(
                instrument=self.instrument
            ).aggregate(Max('order'))['order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

    @classmethod
    def fix_order_gaps(cls, instrument):
        """Ensure order numbers are sequential without gaps"""
        steps = cls.objects.filter(instrument=instrument).order_by('order')
        for index, step in enumerate(steps, start=1):
            if step.order != index:
                step.order = index
                step.save()
    
class InstrumentImage(models.Model):
    VIEW_TYPE_CHOICES = [
        ('front', 'Front View'),
        ('side', 'Side View'),
        ('detail', 'Detail View'),
    ]

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='images'
    )
    view_type = models.CharField(
        max_length=10,
        choices=VIEW_TYPE_CHOICES,
        default='other'
    )
    image = models.ImageField(upload_to='images/instruments/detailed/images/', blank=True, null=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Instrument Images'

    def __str__(self):
        return f"{self.get_view_type_display()} of {self.instrument.name}"
    
# Feedback & Suggestions Model
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    message = models.TextField()
    is_suggestion = models.BooleanField(default=False)  # True = Suggestion, False = General Feedback
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} ({'Suggestion' if self.is_suggestion else 'Feedback'})"
    
class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='testimonials')
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    date_submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    role = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.duration and self.user and self.user.date_joined:
            delta = now() - self.user.date_joined
            # Convert timedelta to human-readable duration
            if delta.days >= 365:
                years = delta.days // 365
                self.duration = f"{years} year{'s' if years > 1 else ''}"
            elif delta.days >= 30:
                months = delta.days // 30
                self.duration = f"{months} month{'s' if months > 1 else ''}"
            else:
                self.duration = f"{delta.days} day{'s' if delta.days != 1 else ''}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback from {self.user.username} ({self.rating} stars)"

    class Meta:
        ordering = ['-date_submitted']
        verbose_name_plural = "Testimonials"


class VideoTutorial(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='video_tutorials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='images/videos/tutorials/', help_text="Upload an MP4 video file")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.instrument.name}"
    

class TechniqueStep(models.Model):
    video_tutorial = models.ForeignKey(
        VideoTutorial, 
        on_delete=models.CASCADE, 
        related_name='technique_steps'
    )
    step_number = models.PositiveIntegerField(editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['video_tutorial', 'step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title} - {self.video_tutorial.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            # Get the maximum step_number for this video_tutorial
            max_step = TechniqueStep.objects.filter(
                video_tutorial=self.video_tutorial
            ).aggregate(Max('step_number'))['step_number__max'] or 0
            self.step_number = max_step + 1
        
        # Ensure the order matches the step_number if not explicitly set
        if self.order == 0:
            self.order = self.step_number
            
        super().save(*args, **kwargs)

    @classmethod
    def reorder_steps(cls, video_tutorial):
        """Reassign step numbers based on current order"""
        steps = cls.objects.filter(video_tutorial=video_tutorial).order_by('order')
        for index, step in enumerate(steps, start=1):
            step.step_number = index
            step.save()
    

class GuidingPrinciples(models.Model):
    title = models.CharField(max_length=255, default="Our Guiding Principles")
    description = models.TextField(
        default="We believe in the transformative power of music education to enrich lives and build communities."
    )
    image = models.ImageField(upload_to='images/images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
        
    def save(self, *args, **kwargs):
        # Ensure there's only one instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class PrincipleCard(models.Model):
    CARD_TYPES = [
        ('Mission', 'Mission'),
        ('Vision', 'Vision'),
        ('Objective', 'Objective'),
        ('Advocacy', 'Advocacy'),
    ]

    guiding_principles = models.ForeignKey(GuidingPrinciples, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    icon = models.CharField(max_length=50, default='fa-music') 
    accent_color = models.CharField(max_length=7, help_text="Enter a hex color code, e.g. #FF6B6B")
    description = models.TextField(blank=True, null=True)
    bullet_points = models.TextField(blank=True, null=True, help_text="If card has a list (like Objective), separate items with a new line.")

    def get_bullet_list(self):
        return self.bullet_points.splitlines() if self.bullet_points else []

    def __str__(self):
        return f"{self.card_type}"
    
    

# models.py
class DiscoverSection(models.Model):
    title = models.CharField(max_length=255, default="Discover Traditional Instruments")
    description = models.TextField()
    image = models.ImageField(upload_to='images/images/', blank=True, null=True)
    mastering_title = models.CharField(max_length=255, default="Mastering")
    mastering_paragraph1 = models.TextField()
    mastering_paragraph2 = models.TextField()
    video1 = models.FileField(upload_to='images/videos/', blank=True, null=True)
    video2 = models.FileField(upload_to='images/videos/', blank=True, null=True)
    video_description = models.TextField(default="Listen to the mesmerizing tones of traditional sitar music")

    def __str__(self):
        return self.title
    
class ContactPage(models.Model):
    # Header Section
    header_title = models.CharField(
        max_length=200, 
        default="Contact Philharmonia",
        help_text="Main title for the contact page header"
    )
    header_description = models.TextField(
        default="Have questions about Philippine traditional instruments? Want to collaborate or share your knowledge? Reach out to us!",
        help_text="Subtitle text under the main header title"
    )

    location_address = models.TextField(
        default="National Music Museum\nManila, Philippines 1000",
        help_text="Full address with line breaks (use Shift+Enter for new lines)"
    )
    
    landline_phone = models.CharField(
        max_length=20, 
        default="+63 2 8123 4567",
        help_text="Format: +63 2 8123 4567"
    )
    mobile_phone = models.CharField(
        max_length=20, 
        default="+63 917 123 4567",
        help_text="Format: +63 917 123 4567"
    )
    
    primary_email = models.EmailField(
        default="info@philharmonia.ph",
        help_text="Primary contact email"
    )
    secondary_email = models.EmailField(
        default="support@philharmonia.ph",
        help_text="Secondary contact email"
    )
    
    weekdays_hours = models.CharField(
        max_length=100, 
        default="Monday to Friday: 9:00 AM - 6:00 PM",
        help_text="Weekday hours format"
    )
    saturday_hours = models.CharField(
        max_length=100, 
        default="Saturday: 10:00 AM - 4:00 PM",
        help_text="Saturday hours format"
    )
    sunday_hours = models.CharField(
        max_length=100, 
        default="Sunday: Closed",
        help_text="Sunday hours format"
    )

    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"
    
    def __str__(self):
        return "Contact Page Configuration"
    
class ContactMessage(models.Model):
    Subject = [
        ('General Inquiry', 'General Inquiry'),
        ('Instrument Information', 'Instrument Information'),
        ('Workshop Registration', 'Workshop Registration'),
        ('Collaboration','Collaboration'),
        ('Feedback/Suggestions', 'Feedback/Suggestions'),
    ]
     
    user = models.ForeignKey(
        'CustomUser', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contact_messages'
    )
    name = models.CharField(max_length=100)  # For guest users
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=Subject)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.user:
            return f"Message from {self.user.username}"
        else:
            return f"Message from {self.name} (Guest)"


class Offering(models.Model):
    icon = models.CharField(max_length=50, default='fa-music')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Offering"
        verbose_name_plural = "Offerings"

    def __str__(self):
        return self.title

    def get_full_icon_class(self):
        """Helper method to get the full Font Awesome class"""
        if not self.icon.startswith('fa-'):
            return f'fa fa-{self.icon}'
        return f'fa {self.icon}'
    
class CulturalImportance(models.Model):
    icon = models.CharField(max_length=50, default='fa-history')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Cultural Importance Item"
        verbose_name_plural = "Cultural Importance Items"

    def __str__(self):
        return self.title

    def get_full_icon_class(self):
        """Helper method to get the full Font Awesome class"""
        if not self.icon.startswith('fa-'):
            return f'fa fa-{self.icon}'
        return f'fa {self.icon}'
    
class TargetAudience(models.Model):
    icon = models.CharField(max_length=50, default='fa-graduation-cap')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
   
    class Meta:
        verbose_name = "Target Audience"
        verbose_name_plural = "Target Audiences"

    def __str__(self):
        return self.title

    def get_full_icon_class(self):
        """Helper method to get the full Font Awesome class"""
        if not self.icon.startswith('fa-'):
            return f'fa fa-{self.icon}'
        return f'fa {self.icon}'
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/team/', default='team/phil.png')
    back_description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.title}"
    


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('email', 'Email'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
    ]
    
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        # Always update icon_class based on platform, regardless of existing value
        self.icon_class = {
            'facebook': 'fab fa-facebook-f',
            'twitter': 'fab fa-twitter',
            'linkedin': 'fab fa-linkedin-in',
            'github': 'fab fa-github',
            'email': 'fas fa-envelope',
            'instagram': 'fab fa-instagram',
            'youtube': 'fab fa-youtube',
        }.get(self.platform, 'fas fa-link')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name}'s {self.platform}"
    
class CulturalSignificance(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        related_name='cultural_significance',
        primary_key=True
    )
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Cultural Significance"
        verbose_name_plural = "Cultural Significance Records"
        
    def __str__(self):
        return f"Cultural significance of {self.instrument.name}"
    
class Funfact(models.Model):
    instrument = models.OneToOneField(
        Instrument, 
        on_delete=models.CASCADE,
        related_name='funfact',
        primary_key=True
    )
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Fun Fact"
        verbose_name_plural = "Fun Facts"
        
    def __str__(self):
        return f"Fun Fact of {self.instrument.name}"
    
class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
    ]
    
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        unique=True,
        verbose_name=("Social Media Platform")
    )
    
    url = models.URLField(
        verbose_name=("Profile URL"),
        help_text=("Enter the full URL to your social media profile")
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=("Is Active"),
        help_text=("Whether to display this social media link")
    )
    
    class Meta:
        verbose_name =("Social Media Link")
        verbose_name_plural =("Social Media Links")
        
    
    def __str__(self):
        return f"{self.get_platform_display()} Link"
    
    def icon_class(self):
        """Returns the appropriate Font Awesome icon class for the platform"""
        icon_map = {
            'facebook': 'fab fa-facebook-f',
            'twitter': 'fab fa-twitter',
            'instagram': 'fab fa-instagram',
            'linkedin': 'fab fa-linkedin-in',
            'youtube': 'fab fa-youtube',
        }
        return icon_map.get(self.platform, 'fas fa-share-alt')


class FooterSettings(models.Model):
    follow_us_title = models.CharField(
        max_length=100,
        default="Follow Us",
        verbose_name=("Follow Us Title")
    )
    
    follow_us_description = models.TextField(
        default="Stay connected and follow us on our social media platforms",
        verbose_name=("Follow Us Description"),
        max_length=200
    )
    
    class Meta:
        verbose_name =("Footer Settings")
        verbose_name_plural =("Footer Settings")
    
    def __str__(self):
        return "Footer Social Media Settings"
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
        


# Performance Appointment (for events)
class PerformanceAppointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
    ]

    EVENT_TYPE_CHOICES = [
        ('Cultural Program', 'Cultural Program'),
        ('School Program', 'School Program'),
        ('Festival', 'Festival'),
        ('Community Event', 'Community Event'),
        ('Traditional Ceremony', 'Traditional Ceremony'),
        ('Workshop', 'Workshop'),
        ('Lecture-Demonstration', 'Lecture-Demonstration'),
        ('Music Lesson', 'Music Lesson'),
        ('Private Event', 'Private Event'),
        ('Other', 'Other'),
    ]

    # Connect appointment to the logged-in user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='performance_appointments'
    )

    event_name = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=100,
        choices=EVENT_TYPE_CHOICES,
        default='Concert'
    )
    event_location = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    decline_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for declining the appointment"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


# Lesson Appointment (for group classes)
class LessonAppointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_appointments'
    )

    school_name = models.CharField(max_length=200)
    class_size = models.PositiveIntegerField(help_text="Number of students in the class")
    lesson_date = models.DateField()
    lesson_time = models.TimeField()
    location = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    decline_reason = models.TextField(blank=True, null=True, help_text="Reason for declining the appointment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lesson for {self.school_name} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class InstrumentForum(models.Model):
    """Each instrument gets its own forum/chat room"""
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        related_name='forum'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Forum for {self.instrument.name}"

class InstrumentMessage(models.Model):
    """Messages in each instrument's forum"""
    forum = models.ForeignKey(
        InstrumentForum,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='instrument_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message by {self.author} in {self.forum.instrument.name}"
    
