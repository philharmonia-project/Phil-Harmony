from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Instrument, InstrumentCategory, Region, Material, Feedback, VideoTutorial, TechniqueStep ,Testimonial, InstrumentMaterial, ConstructionStep ,DiscoverSection, GuidingPrinciples, PrincipleCard, Sound, ContactPage, ContactMessage, Offering, CulturalImportance, TargetAudience, TeamMember, SocialLink, InstrumentImage, CulturalSignificance, Funfact, Tagline, HomePage, SocialMediaLink, FooterSettings, InstrumentPage, PageSection, PerformanceAppointment, LessonAppointment, Instrument3DModel, Site3DContent, InstrumentLink

# User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email


# User login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
    )

    # Override the default method to customize the error message
    def confirm_login_allowed(self, user):
        # Check the username and password manually to customize the error message
        if not user.is_active:
            raise forms.ValidationError(
                "Please enter a correct username and password.",
                code='invalid_login'
            )
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(
                "Please enter a correct username and password.",
                code='invalid_login'
            )
        return super().confirm_login_allowed(user)  # Call the original method



# CustomUser form for updating user profile (including profile picture)
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']  # Include the profile_picture field
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        # Add validation if necessary (e.g., file size, type)
        if profile_picture:
            if not profile_picture.name.endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only image files (jpg, jpeg, png) are allowed.")
        return profile_picture

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['message', 'rating', 'role']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=Testimonial.RATING_CHOICES),
        }    

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['name', 'description', 'category', 'region', "province", 'image']    

class PageForm(forms.ModelForm):
    class Meta:
        model = InstrumentPage
        fields = ['instrument', 'title', 'order']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make order field optional since we'll handle it in the view
        self.fields['order'].required = False
        # You can add any additional field customization here

class SectionForm(forms.ModelForm):
    class Meta:
        model = PageSection
        fields = ['page', 'section_type', 'title', 'content', 'image', 'order']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make order field optional since we'll handle it in the view
        self.fields['order'].required = False
        # You can add any additional field customization here

class CategoryForm(forms.ModelForm):
    class Meta:
        model = InstrumentCategory
        fields = ['name', 'description', 'icon']   


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'description']   

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description']   

class InsMaterialForm(forms.ModelForm):
    class Meta:
        model = InstrumentMaterial
        fields = ['instrument', 'materials' ,'description']   

class StepForm(forms.ModelForm):
    class Meta:
        model = ConstructionStep
        fields = ['instrument', 'title', 'description', 'order']
        widgets = {
            'instrument': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.Select(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['user', 'instrument', 'message']   

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['user', 'message', 'rating', 'role']         

class TutorialForm(forms.ModelForm):
    class Meta:
        model = VideoTutorial
        fields = ['instrument', 'title', 'description', 'video_file'] 

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = TechniqueStep
        fields = ['video_tutorial', 'title', 'description']    

class InstructorForm(forms.ModelForm):
    class Meta:
        model = DiscoverSection
        fields = ['title', 'description', 'image', 'mastering_title', 'mastering_paragraph1', 'mastering_paragraph2', 'video1', 'video2', 'video_description'] 

class PrincipleForm(forms.ModelForm):
    class Meta:
        model = GuidingPrinciples
        fields = ['title', 'description', 'image'] 

class PrincipleCardForm(forms.ModelForm):
    class Meta:
        model = PrincipleCard
        fields = ['guiding_principles', 'card_type', 'icon', 'accent_color', 'description', 'bullet_points'] 

class SoundForm(forms.ModelForm):
    class Meta:
        model = Sound
        fields = ['instrument', 'title', 'sound_sample'] 

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class ContactPageForm(forms.ModelForm):
    class Meta:
        model = ContactPage
        fields = ['header_title', 'header_description',  'location_address', 'landline_phone', 'mobile_phone', 'primary_email', 'secondary_email', 'weekdays_hours', 'saturday_hours', 'sunday_hours']   

class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['icon', 'title' ,'description']  

class ImportanceForm(forms.ModelForm):
    class Meta:
        model = CulturalImportance
        fields = ['icon', 'title' ,'description'] 

class AudienceForm(forms.ModelForm):
    class Meta:
        model = TargetAudience
        fields = ['icon', 'title' ,'description']   

class MemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'title' ,'back_description', 'image']   

class LinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['member', 'platform' ,'url']     

class ViewForm(forms.ModelForm):
    class Meta:
        model = InstrumentImage
        fields = ['instrument', 'view_type',  'image', 'caption']      

class SignificanceForm(forms.ModelForm):
    class Meta:
        model = CulturalSignificance
        fields = ['instrument', 'description']  

class FunFactForm(forms.ModelForm):
    class Meta:
        model = Funfact
        fields = ['instrument', 'description']  

class TaglineForm(forms.ModelForm):
    class Meta:
        model = Tagline
        fields = ['icon', 'title']  

class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = ['main_heading', 'highlight_word', 'description']   

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url']

class FootersForm(forms.ModelForm):
    class Meta:
        model = FooterSettings
        fields = ['follow_us_title', 'follow_us_description']  

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = PerformanceAppointment
        fields = ['event_name', 'event_type', 'event_location', 'event_date', 'event_time', 'message']  

class LessonForm(forms.ModelForm):
    class Meta:
        model = LessonAppointment
        fields = ['school_name', 'class_size', 'lesson_date', 'lesson_time', 'location' , 'message']  

class threeDForm(forms.ModelForm):
    class Meta:
        model = Instrument3DModel
        fields = ['instrument', 'file']     

class sitecontentForm(forms.ModelForm):
    class Meta:
        model = Site3DContent
        fields = ['hero_title', 'hero_description', 'about_title', 'about_content', 'about_image']  
        
class InsLinkForm(forms.ModelForm):
    class Meta:
        model = InstrumentLink
        fields = ['instrument', 'title', 'url', 'link_type'] 

class UserPerformanceForm(forms.ModelForm):
    class Meta:
        model = PerformanceAppointment
        fields = ['event_name', 'event_type', 'event_location', 'event_date', 'event_time', 'message']  

class UserLessonForm(forms.ModelForm):
    class Meta:
        model = LessonAppointment
        fields = ['school_name', 'class_size', 'lesson_date', 'lesson_time', 'location' , 'message']  









# USER HOME PAGE VALIDATIONS
class PerformanceAppointmentForm(forms.ModelForm):
    class Meta:
        model = PerformanceAppointment
        fields = ['event_name', 'event_type', 'event_location', 'event_date', 'event_time', 'message']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise ValidationError("Cannot book appointments for past dates.")
        return event_date
    
    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        event_time = cleaned_data.get('event_time')
        
        # Additional validation: if both date and time are provided, check if it's in the past
        if event_date and event_time:
            from datetime import datetime
            event_datetime = datetime.combine(event_date, event_time)
            current_naive = timezone.now().replace(tzinfo=None)
            
            if event_datetime < current_naive:
                raise ValidationError("Cannot book appointments for past date and time.")
        
        # Check for existing appointments on the same date
        if event_date:
            # Check for existing performance appointments on the same date
            existing_performance = PerformanceAppointment.objects.filter(
                event_date=event_date,
                status='Accepted'
            ).exists()
            
            # Check for existing lesson appointments on the same date
            existing_lesson = LessonAppointment.objects.filter(
                lesson_date=event_date,
                status='Accepted'
            ).exists()
            
            if existing_performance:
                self.add_error('event_date', f"We already have an accepted performance appointment on {event_date}. Please choose a different date.")
            
            if existing_lesson:
                self.add_error('event_date', f"We already have an accepted lesson appointment on {event_date}. Please choose a different date.")
        
        return cleaned_data

class LessonAppointmentForm(forms.ModelForm):
    class Meta:
        model = LessonAppointment
        fields = ['school_name', 'class_size', 'lesson_date', 'lesson_time', 'location', 'message']
        widgets = {
            'lesson_date': forms.DateInput(attrs={'type': 'date'}),
            'lesson_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_lesson_date(self):
        lesson_date = self.cleaned_data.get('lesson_date')
        if lesson_date and lesson_date < timezone.now().date():
            raise ValidationError("Cannot book appointments for past dates.")
        return lesson_date
    
    def clean(self):
        cleaned_data = super().clean()
        lesson_date = cleaned_data.get('lesson_date')
        lesson_time = cleaned_data.get('lesson_time')
        
        # Additional validation: if both date and time are provided, check if it's in the past
        if lesson_date and lesson_time:
            from datetime import datetime
            lesson_datetime = datetime.combine(lesson_date, lesson_time)
            current_naive = timezone.now().replace(tzinfo=None)
            
            if lesson_datetime < current_naive:
                raise ValidationError("Cannot book appointments for past date and time.")
        
        # Check for existing appointments on the same date
        if lesson_date:
            # Check for existing performance appointments on the same date
            existing_performance = PerformanceAppointment.objects.filter(
                event_date=lesson_date,
                status='Accepted'
            ).exists()
            
            # Check for existing lesson appointments on the same date
            existing_lesson = LessonAppointment.objects.filter(
                lesson_date=lesson_date,
                status='Accepted'
            ).exists()
            
            if existing_performance:
                self.add_error('lesson_date', f"We already have an accepted performance appointment on {lesson_date}. Please choose a different date.")
            
            if existing_lesson:
                self.add_error('lesson_date', f"We already have an accepted lesson appointment on {lesson_date}. Please choose a different date.")
        
        return cleaned_data