from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
# LOGIN
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# FROM FORMS.PY
from .forms import UserRegisterForm, UserLoginForm, CustomUserForm, InstrumentForm, CategoryForm, RegionForm, MaterialForm, StepForm ,FeedbackForm, TestimonialForm ,TutorialForm, TechniqueForm ,InsMaterialForm, InstructorForm, PrincipleForm, PrincipleCardForm, SoundForm, ContactPageForm, OfferingForm, ImportanceForm, AudienceForm, MemberForm, LinkForm, ViewForm, SignificanceForm, FunFactForm, SocialMediaForm, FootersForm, HomePageForm, TaglineForm, PageForm, SectionForm, PerformanceForm, LessonForm, threeDForm, sitecontentForm, InsLinkForm, UserPerformanceForm, UserLessonForm, PerformanceAppointmentForm, LessonAppointmentForm

# FROM MODELS.PY
from .models import CustomUser, InstrumentCategory, Region, Material, InstrumentMaterial ,Instrument, Sound ,Feedback, Testimonial, UserLogin, VideoTutorial,GuidingPrinciples, PrincipleCard ,DiscoverSection, ContactPage, ContactMessage, Offering, CulturalImportance, TargetAudience, TeamMember, SocialLink, TechniqueStep, ConstructionStep, InstrumentImage, CulturalSignificance, Funfact, HomePage, Tagline, FooterSettings, SocialMediaLink, InstrumentPage, PageSection, PerformanceAppointment, LessonAppointment, InstrumentForum, InstrumentMessage, Instrument3DModel, Site3DContent, InstrumentLink

from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Don't log in, don't redirect
            return JsonResponse({
                'success': True,
                'message': 'Registration successful! You can now log in.'
            })
        else:
            errors = {field: error_list for field, error_list in form.errors.items()}
            return JsonResponse({
                'success': False,
                'error': 'Please correct the errors below.',
                'errors': errors
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)




def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                redirect_url = reverse('admin_main') if user.role == 'admin' else reverse('user_home')
                return JsonResponse({
                    'success': True,
                    'redirect_url': redirect_url
                })
            else:
                form.add_error(None, "Invalid username or password.")
        
        # Prepare error response
        errors = {field: error.get_json_data()[0]['message'] 
                 for field, error in form.errors.items()}
        return JsonResponse({
            'success': False,
            'error': form.errors.get('__all__', ['Invalid credentials'])[0],
            'errors': errors
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)




@csrf_exempt
def check_auth_status(request):
    """Check if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
            'redirect_url': '/user_home/'  # Change to your desired redirect
        })
    return JsonResponse({'authenticated': False})

@login_required
def get_user_info(request):
    """Get current user info"""
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
    })



# Logout view
def logout_view(request):
    logout(request)
    return redirect('frontpage')

    

# ADMIN DASHBOARD# ADMIN DASHBOARD# ADMIN DASHBOARD# ADMIN DASHBOARD# ADMIN DASHBOARD

# Set user as admin
@login_required
def set_user_as_admin(request, user_id):
    if request.user.role != 'admin':  # Check if the logged-in user is admin
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 'admin':  # Check if the user is already an admin
        messages.warning(request, f"{user.username} is already an admin.")
    else:
        user.role = 'admin'  # Set the role to 'admin'
        user.save()
        messages.success(request, f"{user.username} has been promoted to admin.")

    return redirect('admin_main')  # Redirect back to admin dashboard after updating



# Remove user as admin
@login_required
def remove_user_as_admin(request, user_id):
    if request.user.role != 'admin':  # Check if the logged-in user is admin
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 'user':  # If the user is already a regular user, no action is needed
        messages.warning(request, f"{user.username} is already a regular user.")
    else:
        user.role = 'user'  # Set the role to 'user'
        user.save()
        messages.success(request, f"{user.username} has been removed from admin status.")

    return redirect('admin_main')  # Redirect back to admin dashboard after updating


# Delete user
@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':  # Only admins can delete users
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    # Show confirmation form before deletion
    if request.method == 'GET':
        return render(request, 'app/admin/delete_user.html', {'user': user})

    # Handle deletion after form submission
    if request.method == 'POST':
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
        else:
            user.delete()
            messages.success(request, f"{user.username}'s account has been deleted.")
        
        # Redirect after deletion
        return redirect('admin_main')  # Redirect to admin dashboard or another page



# Update user profile (including photo)
@login_required
def update_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user.role != 'admin' and request.user != user:
        return redirect('user_home')  # Ensure that only the user or admin can update the profile

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)  # Ensure to handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}'s profile has been updated.")
            return redirect('admin_main' if request.user.role == 'admin' else 'user_home')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'app/admin/update_user_profile.html', {'form': form, 'user': user})



# CHART FOR DASHBOARD# CHART FOR DASHBOARD# CHART FOR DASHBOARD# CHART FOR DASHBOARD# CHART FOR DASHBOARD

# CHART FOR MOST VIEW INSTRUMENT
def get_chart_data(request):
    # Get the top 5 most viewed instruments
    instruments = Instrument.objects.order_by('-views')[:5]

    # Prepare data for Chart.js
    instrument_names = [inst.name for inst in instruments]
    instrument_views = [inst.views for inst in instruments]

    return JsonResponse({
        "instrument_names": instrument_names,
        "instrument_views": instrument_views
    })

# COUNT HOW MANY INSTRUMENT IN CATEGORY# COUNT HOW MANY INSTRUMENT IN CATEGORY# COUNT HOW MANY INSTRUMENT IN CATEGORY
def get_category_chart_data(request):
    # Get all categories and count the number of instruments in each
    categories = InstrumentCategory.objects.annotate(count=Count('instruments'))

    # Prepare data for Chart.js
    category_labels = [cat.name for cat in categories]
    category_counts = [cat.count for cat in categories]

    return JsonResponse({
        "category_labels": category_labels,
        "category_counts": category_counts
    })

# LOGIN DATA# LOGIN DATA# LOGIN DATA# LOGIN DATA# LOGIN DATA# LOGIN DATA# LOGIN DATA# LOGIN DATA
def get_login_chart_data(request):
    """Return login data for the last 7 days."""
    today = now().date()
    last_week = today - timedelta(days=6)

    # Get logins per day
    logins_per_day = (
        UserLogin.objects.filter(timestamp__date__gte=last_week)
        .values("timestamp__date")
        .annotate(count=Count("id"))
        .order_by("timestamp__date")
    )

    labels = [entry["timestamp__date"].strftime("%b %d") for entry in logins_per_day]
    data = [entry["count"] for entry in logins_per_day]

    return JsonResponse({"labels": labels, "data": data})




# This is For Admin HTML# This is For Admin HTML# This is For Admin HTML# This is For Admin HTML# This is For Admin HTML
@login_required
def admin_main(request):
    if request.user.role != 'admin':  # Check role directly
        return redirect('user_home')
    
    # Chat Management Context
    selected_forum_id = request.GET.get('forum_id')
    if selected_forum_id:
        selected_forum = get_object_or_404(InstrumentForum, id=selected_forum_id)
    else:
        selected_forum = InstrumentForum.objects.first()

    # Get messages for selected forum
    forum_messages = []
    if selected_forum:
        forum_messages = selected_forum.messages.select_related('author').order_by('created_at')

    users = CustomUser.objects.all()
    categorys = InstrumentCategory.objects.all()
    regions = Region.objects.all()
    Materials = Material.objects.all()
    InsMaterials = InstrumentMaterial.objects.all()
    Instruments = Instrument.objects.all()
    Sounds = Sound.objects.all()
    Feedbacks = Feedback.objects.all()
    Tutorials = VideoTutorial.objects.all()
    Testimonials = Testimonial.objects.all()
    Principles = GuidingPrinciples.objects.all()
    PrincipleCards  = PrincipleCard.objects.all()
    Instructor = DiscoverSection.objects.all()
    Offerings = Offering.objects.all()
    Importances = CulturalImportance.objects.all()
    Audiences = TargetAudience.objects.all()
    Members = TeamMember.objects.all()
    SocialLinks = SocialLink.objects.all()
    ContactPages = ContactPage.objects.all()
    ContactMessages = ContactMessage.objects.all()
    technique_steps = TechniqueStep.objects.all()
    ConstructionSteps = ConstructionStep.objects.all()
    InsImage = InstrumentImage.objects.all()
    Significance = CulturalSignificance.objects.all()
    funfacts = Funfact.objects.all() 
    homepages = HomePage.objects.all()
    taglines = Tagline.objects.all()
    footers = FooterSettings.objects.all()
    socialMedia = SocialMediaLink.objects.all()
    pages = InstrumentPage.objects.all()
    sections = PageSection.objects.all()
    Performances = PerformanceAppointment.objects.all()
    Lessons = LessonAppointment.objects.all()
    threeD = Instrument3DModel.objects.all()
    instrument_forums = InstrumentForum.objects.all()
    sitecontent = Site3DContent.objects.all()
    InsLink = InstrumentLink.objects.all()
    # Removed the duplicate messages variable
    
    #Table on forms
    form = CustomUserForm()  
    return render(request, 'app/admin/admin_main.html', 
                {'users': users, 'categorys': categorys, 
                'regions': regions, 'Materials' : Materials, 
                'InsMaterials' : InsMaterials ,'Instruments' : Instruments,
                'Feedbacks' : Feedbacks, 'Testimonials' : Testimonials, 
                'Principles' : Principles, 'PrincipleCards' : PrincipleCards,
                'Instructor' : Instructor,'Tutorials' : Tutorials, 'Sounds' : Sounds,
                'ContactPages' : ContactPages, 'ContactMessages' : ContactMessages,
                'Offerings' : Offerings, 'Importances' : Importances, 'Audiences' : Audiences, 'Members' : Members, 
                'technique_steps' : technique_steps, 'ConstructionSteps' : ConstructionSteps, 'SocialLinks' : SocialLinks,
                'InsImage' : InsImage, 'Significance' : Significance, 'funfacts' : funfacts, 'homepages' : homepages, 'taglines' : taglines,
                'footers' : footers, 'socialMedia' : socialMedia, 'pages' : pages, 'sections' : sections, 'Performances' : Performances,
                'Lessons' : Lessons, 'threeD' : threeD, 'instrument_forums' : instrument_forums, 'InsLink' : InsLink,
                'selected_forum': selected_forum, 'messages': forum_messages, 'sitecontent' : sitecontent })  # Use forum_messages here

@login_required
def toggle_forum_status(request, forum_id):
    if request.user.role != 'admin':
        return redirect('user_home')
        
    forum = get_object_or_404(InstrumentForum, id=forum_id)
    forum.is_active = not forum.is_active
    forum.save()
    
    # Redirect back to admin_main with current forum_id if any
    referer = request.META.get('HTTP_REFERER', '')
    if 'forum_id=' in referer:
        return redirect(referer)
    return redirect('admin_main')

@login_required
def delete_message(request, message_id):
    if request.user.role != 'admin':
        return redirect('user_home')
        
    message = get_object_or_404(InstrumentMessage, id=message_id)
    forum_id = message.forum.id
    message.delete()
    
    # Redirect back to admin_main with the current forum
    return redirect(f'{reverse("admin_main")}?forum_id={forum_id}')

@login_required
def delete_all_forum_messages(request, forum_id):
    if request.user.role != 'admin':
        return redirect('user_home')
        
    forum = get_object_or_404(InstrumentForum, id=forum_id)
    forum.messages.all().delete()
    
    # Redirect back to admin_main with the current forum
    return redirect(f'{reverse("admin_main")}?forum_id={forum_id}')

# PHILIPPINES INSTRUMENT
@login_required
def admin_instrument(request):
    if request.user.role != 'admin':
        return redirect('user_home')

    Instruments = Instrument.objects.all()
    return render(request, 'app/admin/Instrument/admin_Instrument.html', {'Instruments': Instruments})


def provinces_with_instruments(request):
    provinces = (
        Instrument.objects
        .filter(province__isnull=False)
        .exclude(province='')
        .values_list('province', flat=True)
        .distinct()
    )
    return JsonResponse(list(provinces), safe=False)


def instruments_by_province(request):
    province_name = request.GET.get('province_name')

    instruments = Instrument.objects.filter(province__iexact=province_name)

    data = []
    for instrument in instruments:
        image_url = instrument.image.url if instrument.image else None
        full_image_url = request.build_absolute_uri(image_url) if image_url else None

        data.append({
            'id': instrument.pk,   # ⭐ IMPORTANT
            'name': instrument.name,
            'image': full_image_url,
            'region': instrument.region.name if instrument.region else None,
        })

    return JsonResponse(data, safe=False)


class InstrumentDetailView(LoginRequiredMixin, DetailView):
    model = Instrument
    template_name = "app/admin/Instrument/instrument_detail.html"
    context_object_name = "instrument"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = self.get_object()

        # Your existing context data
        ins_materials = InstrumentMaterial.objects.filter(instrument=instrument)
        material_set = set()
        for insmat in ins_materials:
            material_set.update(insmat.materials.all())

        context['insmaterials'] = ins_materials 
        context['materials'] = material_set
        context['tutorials'] = VideoTutorial.objects.filter(instrument=instrument)
        context['video'] = instrument.video_tutorials.first()
        context['region'] = instrument.region
        context['technique_steps'] = TechniqueStep.objects.all()
        context['construction_steps'] = ConstructionStep.objects.filter(instrument=instrument).order_by('order')
        context['cultural_significance'] = CulturalSignificance.objects.all()
        context['funfact'] = Funfact.objects.all()
        context['popular_instruments'] = Instrument.objects.order_by('-views')[:4]
        context['sound_samples'] = instrument.sound_set.all()

        # Chat messages - Check if forum is active
        forum, created = InstrumentForum.objects.get_or_create(instrument=instrument)
        # Get messages in correct order (oldest first)
        messages = forum.messages.select_related('author').order_by('created_at')
        context['chat_messages'] = messages
        context['forum_active'] = forum.is_active  # Add this line
        context['forum'] = forum  # Add forum object to context

        return context

    def post(self, request, *args, **kwargs):
        """Handle chat message posting"""
        instrument = self.get_object()
        
        # Get the forum and check if it's active
        forum, created = InstrumentForum.objects.get_or_create(instrument=instrument)
        
        # Check if forum is inactive
        if not forum.is_active:
            return JsonResponse({
                'success': False,
                'error': 'This forum is currently inactive. You cannot send messages at this time.'
            })
        
        # Get the message content
        content = request.POST.get('content', '').strip()
        
        # Simple validation
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Please type a message'
            })
        
        # Create the message
        message = InstrumentMessage.objects.create(
            forum=forum,
            author=request.user,
            content=content
        )
        
        # Return success response
        return JsonResponse({
            'success': True,
            'username': request.user.username,
            'content': content,
            'timestamp': 'just now',
            'user_initial': request.user.username[0].upper(),
            'profile_picture': request.user.profile_picture.url if request.user.profile_picture else ''
        })

    def get_object(self):
        instrument = super().get_object()
        instrument.views += 1
        instrument.save()
        return instrument

class CreateInstrument(LoginRequiredMixin, CreateView):
    model = Instrument
    fields = ['name', 'description', 'category', 'province', 'region', 'image']
    template_name = 'app/admin/Instrument/CreateInstrument.html'

    def get_success_url(self):
        return reverse('admin_main') + '#admin-Instrument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Categorys'] = InstrumentCategory.objects.all()
        context['regions'] = Region.objects.all()
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    

class UpdateInstrument(LoginRequiredMixin, UpdateView):
    model = Instrument
    form_class = InstrumentForm
    template_name = 'app/admin/Instrument/UpdateInstrument.html'

    def get_success_url(self):
        return reverse('admin_main') + '#admin-Instrument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Categorys'] = InstrumentCategory.objects.all()
        context['regions'] = Region.objects.all()
        return context
    
   

class DeleteInstrument(LoginRequiredMixin, DeleteView):
    model = Instrument
    template_name = 'app/admin/Instrument/DeleteInstrument.html'

    def get_success_url(self):
        return reverse('admin_main') + '#admin-Instrument'

# INSTRUMENT HISTORY
@login_required
def admin_History(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    pages = InstrumentPage.objects.all()
    sections = PageSection.objects.all()
    
    return render(request, 'app/admin/History/admin_History.html', {'pages' : pages, 'sections' : sections })

class CreatePage(LoginRequiredMixin, CreateView):
    model = InstrumentPage
    fields = ['instrument', 'title']   
    template_name = 'app/admin/History/Page/CreatePage.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context   
    
class UpdatePage(LoginRequiredMixin, UpdateView):
    model = InstrumentPage
    form_class = PageForm
    template_name = 'app/admin/History/Page/UpdatePage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "pages"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        
        # Get all instruments for the dropdown
        context['Instruments'] = Instrument.objects.all()
        
        # Get the maximum order value for the current instrument's pages
        context['max_order'] = InstrumentPage.objects.filter(
            instrument=page.instrument
        ).count()
        
        return context

    def form_valid(self, form):
        # Get the original page before update
        original_page = self.get_object()
        
        # Get the new order value from the form
        new_order = form.cleaned_data.get('order', original_page.order)
        
        # Get the new instrument from the form
        new_instrument = form.cleaned_data.get('instrument', original_page.instrument)
        
        # If order or instrument changed, we need to reorder pages
        if new_order != original_page.order or new_instrument != original_page.instrument:
            # First, save with the original order to avoid unique constraint issues
            form.instance.order = 0
            response = super().form_valid(form)
            
            # Now update the order properly
            self.reorder_pages(form.instance, new_instrument, new_order)
            return response
        
        return super().form_valid(form)

    def reorder_pages(self, page, new_instrument, new_order):
        """
        Reorder pages when the order or instrument is changed
        """
        # Get all pages on the new instrument, excluding the current one
        pages = InstrumentPage.objects.filter(instrument=new_instrument).exclude(pk=page.pk)
        
        # Update the current page's instrument and order
        page.instrument = new_instrument
        page.order = new_order
        page.save()
        
        # Reorder all other pages on the instrument
        current_order = 1
        for p in pages.order_by('order'):
            if current_order == new_order:
                current_order += 1  # skip the position we're moving to
            p.order = current_order
            p.save()
            current_order += 1  


class DeletePage(LoginRequiredMixin, DeleteView):
    model = InstrumentPage
    template_name = 'app/admin/History/Page/DeletePage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "pages"


class CreateSection(LoginRequiredMixin, CreateView):
    model = PageSection
    fields = ['page', 'section_type', 'title', 'content', 'image']   
    template_name = 'app/admin/History/CreateSection.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = InstrumentPage.objects.all()
        context['SECTION_TYPE_CHOICES'] = PageSection.SECTION_TYPE_CHOICES
        return context  
    
class UpdateSection(LoginRequiredMixin, UpdateView):
    model = PageSection
    form_class = SectionForm
    template_name = 'app/admin/History/UpdateSection.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "section"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.get_object()
        
        # Get all pages for the dropdown
        context['pages'] = InstrumentPage.objects.all()
        
        # Get the maximum order value for the current page's sections
        context['max_order'] = PageSection.objects.filter(
            page=section.page
        ).count()
        
        # Add section type choices
        context['SECTION_TYPE_CHOICES'] = PageSection.SECTION_TYPE_CHOICES
        
        # Add current page to context
        context['page'] = section.page
        
        return context

    def form_valid(self, form):
        # Get the original section before update
        original_section = self.get_object()
        
        # Get the new order value from the form
        new_order = form.cleaned_data.get('order', original_section.order)
        
        # Get the new page from the form
        new_page = form.cleaned_data.get('page', original_section.page)
        
        # If order or page changed, we need to reorder sections
        if new_order != original_section.order or new_page != original_section.page:
            # First, save with the original order to avoid unique constraint issues
            form.instance.order = 0
            response = super().form_valid(form)
            
            # Now update the order properly
            self.reorder_sections(form.instance, new_page, new_order)
            return response
        
        return super().form_valid(form)

    def reorder_sections(self, section, new_page, new_order):
        """
        Reorder sections when the order or page is changed
        """
        # Get all sections on the new page, excluding the current one
        sections = PageSection.objects.filter(page=new_page).exclude(pk=section.pk)
        
        # Update the current section's page and order
        section.page = new_page
        section.order = new_order
        section.save()
        
        # Reorder all other sections on the page
        current_order = 1
        for sec in sections.order_by('order'):
            if current_order == new_order:
                current_order += 1  # skip the position we're moving to
            sec.order = current_order
            sec.save()
            current_order += 1

class DeleteSection(LoginRequiredMixin, DeleteView):
    model = PageSection
    template_name = 'app/admin/History/DeleteSection.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "sections"

    def get_success_url(self):
        return reverse_lazy('admin_main') + '#admin-Instrument'

# INSTRUMENT CATEGORY

@login_required
def admin_category(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    categorys = InstrumentCategory.objects.all()
    return render(request, 'app/admin/Category/admin_Category.html', {'categorys': categorys})


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = InstrumentCategory
    template_name = "app/admin/Category/CategoryDetail.html"
    context_object_name = "category"



class CreateCategory(LoginRequiredMixin, CreateView):
    model = InstrumentCategory
    fields = ['name', 'description' , 'icon']
    template_name = 'app/admin/Category/CreateCategory.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    

class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = InstrumentCategory
    form_class = CategoryForm
    template_name = 'app/admin/Category/UpdateCategory.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "category"

   
class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = InstrumentCategory
    template_name = 'app/admin/Category/DeleteCategory.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "category"



# regions 
@login_required
def admin_tribe(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    regions = Region.objects.all()
    return render(request, 'app/admin/Tribe/admin_Tribe.html', {'regions': regions})


class TribeDetailView(LoginRequiredMixin, DetailView):
    model = Region
    template_name = "app/admin/Tribe/TribeDetail.html"
    context_object_name = "tribe"



class CreateTribe(LoginRequiredMixin, CreateView):
    model = Region
    fields = ['name', 'description'] 
    template_name = 'app/admin/Tribe/CreateTribe.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    

class UpdateTribe(LoginRequiredMixin, UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'app/admin/Tribe/UpdateTribe.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "tribe"

   
class DeleteTribe(LoginRequiredMixin, DeleteView):
    model = Region
    template_name = 'app/admin/Tribe/DeleteTribe.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "tribe"



# INSTRUMENT MATERIAL
@login_required
def admin_material(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Materials = Material.objects.all()
    InsMaterials = InstrumentMaterial.objects.select_related('instrument').prefetch_related('materials')
    return render(request, 'app/admin/Material/admin_Material.html', {'Materials': Materials, 'InsMaterials' : InsMaterials})


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = "app/admin/Material/MaterialDetail.html"
    context_object_name = "material"



class CreateMaterial(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'description']  
    template_name = 'app/admin/Material/CreateMaterial.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    

class UpdateMaterial(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'app/admin/Material/UpdateMaterial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "material"


   
class DeleteMaterial(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = 'app/admin/Material/DeleteMaterial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "material"


# INSTRUMENT MATERIALS
class CreateInsMaterial(LoginRequiredMixin, CreateView):
    model = InstrumentMaterial
    fields = ['instrument', 'materials' ,'description']  
    template_name = 'app/admin/Material/InstrumentMaterial/CreateMaterials.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Materials'] = Material.objects.all()
        context['Instruments'] = Instrument.objects.all()
        return context    
    

class UpdateInsMaterial(LoginRequiredMixin, UpdateView):
    model = InstrumentMaterial
    form_class = InsMaterialForm
    template_name = 'app/admin/Material/InstrumentMaterial/UpdateMaterials.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "insmaterial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Materials'] = Material.objects.all()
        context['Instruments'] = Instrument.objects.all()
        return context   


class DeleteInsMaterial(LoginRequiredMixin, DeleteView):
    model = InstrumentMaterial
    template_name = 'app/admin/Material/InstrumentMaterial/DeleteMaterials.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "insmaterial"


# INSTRUMENT MATERIAL STEPS
@login_required
def admin_Step(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Steps = ConstructionStep.objects.all()
    return render(request, 'app/admin/Construction/admin_Construction.html', {'Steps': Steps })

class CreateStep(LoginRequiredMixin, CreateView):
    model = ConstructionStep
    fields = ['instrument', 'title' ,'description']  
    template_name = 'app/admin/Construction/CreateStep.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context  
    
class UpdateStep(LoginRequiredMixin, UpdateView):
    model = ConstructionStep
    template_name = 'app/admin/Construction/UpdateStep.html'
    success_url = reverse_lazy('admin_main')
    fields = ['title', 'description', 'order']
    context_object_name = 'step'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.get_object()
        total_steps = ConstructionStep.objects.filter(
            instrument=step.instrument
        ).count()
        context['step_range'] = range(1, total_steps + 1)
        return context

    def form_valid(self, form):
        step = self.get_object()
        new_order = form.cleaned_data['order']
        current_order = step.order
        
        if new_order != current_order:
            # Find and swap with the step that has the new order position
            ConstructionStep.objects.filter(
                instrument=step.instrument,
                order=new_order
            ).update(order=current_order)
            
        return super().form_valid(form)
   
class DeleteStep(LoginRequiredMixin, DeleteView):
    model = ConstructionStep
    template_name = 'app/admin/Construction/DeleteStep.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Step"


# FEEDBACK
@login_required
def admin_feedback(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Feedbacks = Feedback.objects.all()
    return render(request, 'app/admin/Feedback/admin_feedback.html', {'Feedbacks': Feedbacks })

@login_required
def feedback_approval(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.is_suggestion = 'is_suggestion' in request.POST
    feedback.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_feedback'))

class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = "app/admin/Feedback/FeedbackDetail.html"
    context_object_name = "feedback"



class CreateFeedback(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['user', 'instrument', 'message']   
    template_name = 'app/admin/Feedback/CreateFeedback.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        context['Instruments'] = Instrument.objects.all()
        return context
    
class UpdateFeedback(LoginRequiredMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'app/admin/Feedback/UpdateFeedback.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "feedback"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        context['Instruments'] = Instrument.objects.all()
        return context
   
class DeleteFeedback(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'app/admin/Feedback/DeleteFeedback.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "feedback"



# TESTIMONIAL
@login_required
def admin_testimonial(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Testimonials = Testimonial.objects.all()
    return render(request, 'app/admin/Testimonial/admin_testimonial.html', {'Testimonials': Testimonials })

@login_required
def testimonial_approval(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.approved = 'approved' in request.POST
    testimonial.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_testimonial'))


class CreateTestimonial(LoginRequiredMixin, CreateView):
    model = Testimonial
    fields = ['message', 'rating', 'role']  # Removed 'user' from fields
    template_name = 'app/user/CreateTestimonial.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically set the logged-in user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # You can set initial values here if needed
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You might not need all users anymore, but keeping if needed elsewhere
        context['Users'] = CustomUser.objects.all()
        context['current_user'] = self.request.user
        return context
    
class UpdateTestimonial(LoginRequiredMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'app/admin/Testimonial/UpdateTestimonial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "testimonial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        return context
   
class DeleteTestimonial(LoginRequiredMixin, DeleteView):
    model = Testimonial
    template_name = 'app/admin/Testimonial/DeleteTestimonial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "testimonial"



# TUTORIAL
@login_required
def admin_tutorial(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Tutorials = VideoTutorial.objects.all()
    return render(request, 'app/admin/Tutorial/admin_Tutorial.html', {'Tutorials': Tutorials })


class TutorialDetailView(LoginRequiredMixin, DetailView):
    model = VideoTutorial
    template_name = "app/admin/Tutorial/TutorialDetail.html"
    context_object_name = "tutorial"



class CreateTutorial(LoginRequiredMixin, CreateView):
    model = VideoTutorial
    fields = ['instrument', 'title', 'description', 'video_file']   
    template_name = 'app/admin/Tutorial/CreateTutorial.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
    
    

class UpdateTutorial(LoginRequiredMixin, UpdateView):
    model = VideoTutorial
    form_class = TutorialForm
    template_name = 'app/admin/Tutorial/UpdateTutorial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "tutorial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
   
class DeleteTutorial(LoginRequiredMixin, DeleteView):
    model = VideoTutorial
    template_name = 'app/admin/Tutorial/DeleteTutorial.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "tutorial"

# TUTORIAL Technique
@login_required
def admin_Technique(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Technique = TechniqueStep.objects.all()
    return render(request, 'app/admin/PlayingGuide/admin_PlayingGuide.html', {'Technique': Technique })

class CreateTechnique(LoginRequiredMixin, CreateView):
    model = TechniqueStep
    fields = ['video_tutorial', 'title', 'description']   
    template_name = 'app/admin/PlayingGuide/CreateTechnique.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tutorials'] = VideoTutorial.objects.all()
        return context

class UpdateTechnique(LoginRequiredMixin, UpdateView):
    model = TechniqueStep
    form_class = TechniqueForm
    template_name = 'app/admin/PlayingGuide/UpdateTechnique.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Technique"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tutorials'] = VideoTutorial.objects.all()
        return context
   
class DeleteTechnique(LoginRequiredMixin, DeleteView):
    model = TechniqueStep
    template_name = 'app/admin/PlayingGuide/DeleteTechnique.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Technique"
    

# INSTRUCTOR
@login_required
def admin_instructor(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Instructors = DiscoverSection.objects.all()
    return render(request, 'app/admin/Instructor/admin_Instructor.html', {'Instructors': Instructors })


class CreateInstructor(LoginRequiredMixin, CreateView):
    model = DiscoverSection
    fields = ['title', 'description', 'image', 'mastering_title', 'mastering_paragraph1', 'mastering_paragraph2', 'video1', 'video2', 'video_description'] 
    template_name = 'app/admin/Instructor/CreateInstructor.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
        

class UpdateInstructor(LoginRequiredMixin, UpdateView):
    model = DiscoverSection
    form_class = InstructorForm
    template_name = 'app/admin/Instructor/UpdateInstructor.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "instructor"

   
class DeleteInstructor(LoginRequiredMixin, DeleteView):
    model = DiscoverSection
    template_name = 'app/admin/Instructor/DeleteInstructor.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "instructor"


# PRINCIPLE
@login_required
def admin_principle(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    principles = GuidingPrinciples.objects.all()
    principlecards = PrincipleCard.objects.all()
    return render(request, 'app/admin/Principle/admin_Principle.html', {'principles': principles, 'principlecards' : principlecards })


class CreatePrinciple(LoginRequiredMixin, CreateView):
    model = GuidingPrinciples
    fields = ['title', 'description', 'image'] 
    template_name = 'app/admin/Principle/CreatePrinciple.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
        

class UpdatePrinciple(LoginRequiredMixin, UpdateView):
    model = GuidingPrinciples
    form_class = PrincipleForm
    template_name = 'app/admin/Principle/UpdatePrinciple.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "principle"

   
class DeletePrinciple(LoginRequiredMixin, DeleteView):
    model = GuidingPrinciples
    template_name = 'app/admin/Principle/DeletePrinciple.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "principle"

# PRINCIPLE CARD
class CreatePrincipleCard(LoginRequiredMixin, CreateView):
    model = PrincipleCard
    fields = ['guiding_principles', 'card_type', 'icon', 'accent_color', 'description', 'bullet_points'] 
    template_name = 'app/admin/Principle/PrincipleCard/CreatePrincipleCard.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['principles'] = GuidingPrinciples.objects.all()
        return context
        

class UpdatePrincipleCard(LoginRequiredMixin, UpdateView):
    model = PrincipleCard
    form_class = PrincipleCardForm
    template_name = 'app/admin/Principle/PrincipleCard/UpdatePrincipleCard.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['principles'] = GuidingPrinciples.objects.all()
        return context

   
class DeletePrincipleCard(LoginRequiredMixin, DeleteView):
    model = PrincipleCard
    template_name = 'app/admin/Principle/PrincipleCard/DeletePrincipleCard.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "card"


 
# INSTRUMENT SOUND
@login_required
def admin_Sound(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Sounds = Sound.objects.all()
    return render(request, 'app/admin/Sound/admin_sound.html', {'Sounds': Sounds })

class CreateSound(LoginRequiredMixin, CreateView):
    model = Sound
    fields = ['instrument', 'title',  'sound_sample']   
    template_name = 'app/admin/Sound/CreateSound.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
    
    

class UpdateSound(LoginRequiredMixin, UpdateView):
    model = Sound
    form_class = SoundForm
    template_name = 'app/admin/Sound/UpdateSound.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "sound"

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
   
class DeleteSound(LoginRequiredMixin, DeleteView):
    model = Sound
    template_name = 'app/admin/Sound/DeleteSound.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "sound"


# INSTRUMENT CONTACT PAGE
@login_required
def admin_ContactPage(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    ContactPages = ContactPage.objects.all()
    return render(request, 'app/admin/ContactPage/admin_contactPage.html', {'ContactPages': ContactPages })

class CreateContactPage(LoginRequiredMixin, CreateView):
    model = ContactPage
    fields = ['header_title', 'header_description',  'location_address', 'landline_phone', 'mobile_phone', 'primary_email', 'secondary_email', 'weekdays_hours', 'saturday_hours', 'sunday_hours']   
    template_name = 'app/admin/ContactPage/CreateContactPage.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
      

class UpdateContactPage(LoginRequiredMixin, UpdateView):
    model = ContactPage
    form_class = ContactPageForm
    template_name = 'app/admin/ContactPage/UpdateContactPage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "page"

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)

   
class DeleteContactPage(LoginRequiredMixin, DeleteView):
    model = ContactPage
    template_name = 'app/admin/ContactPage/DeleteContactPage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "page"

# ABOUT PAGE OFFERING
@login_required
def admin_Offering(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Offerings = Offering.objects.all()
    
    return render(request, 'app/admin/Offering/admin_Offering.html', {'Offerings' : Offerings})


class CreateOffering(LoginRequiredMixin, CreateView):
    model = Offering
    fields = ['icon', 'title' ,'description']  
    template_name = 'app/admin/Offering/CreateOffering.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    

class UpdateOffering(LoginRequiredMixin, UpdateView):
    model = Offering
    form_class = OfferingForm
    template_name = 'app/admin/Offering/UpdateOffering.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Offering"


   
class DeleteOffering(LoginRequiredMixin, DeleteView):
    model = Offering
    template_name = 'app/admin/Offering/DeleteOffering.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Offering"

# ABOUT PAGE CULTURAL IMPORTANCE
@login_required
def admin_Importance(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Importance = CulturalImportance.objects.all()
    
    return render(request, 'app/admin/CulturalImportance/admin_CulturalImportance.html', {'Importance' : Importance})


class CreateImportance(LoginRequiredMixin, CreateView):
    model = CulturalImportance
    fields = ['icon', 'title' ,'description']  
    template_name = 'app/admin/CulturalImportance/CreateImportance.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    

class UpdateImportance(LoginRequiredMixin, UpdateView):
    model = CulturalImportance
    form_class = ImportanceForm
    template_name = 'app/admin/CulturalImportance/UpdateImportance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Importance"


   
class DeleteImportance(LoginRequiredMixin, DeleteView):
    model = CulturalImportance
    template_name = 'app/admin/CulturalImportance/DeleteImportance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Importance"
   

# ABOUT PAGE TARGET AUDIENCE
@login_required
def admin_Audience(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Audience = TargetAudience.objects.all()
    
    return render(request, 'app/admin/TargetAudience/admin_TargetAudience.html', {'Audience' : Audience})


class CreateAudience(LoginRequiredMixin, CreateView):
    model = TargetAudience
    fields = ['icon', 'title' ,'description']  
    template_name = 'app/admin/TargetAudience/CreateAudience.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    

class UpdateAudience(LoginRequiredMixin, UpdateView):
    model = TargetAudience
    form_class = AudienceForm
    template_name = 'app/admin/TargetAudience/UpdateAudience.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Audience"


   
class DeleteAudience(LoginRequiredMixin, DeleteView):
    model = TargetAudience
    template_name = 'app/admin/TargetAudience/DeleteAudience.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Audience"

# ABOUT PAGE TEAM MEMBER
@login_required
def admin_Member(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Members = TeamMember.objects.all()
    
    return render(request, 'app/admin/TeamMember/admin_TeamMember.html', {'Members' : Members})


class CreateMember(LoginRequiredMixin, CreateView):
    model = TeamMember
    fields = ['name', 'title' ,'back_description', 'image']  
    template_name = 'app/admin/TeamMember/CreateMember.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    

class UpdateMember(LoginRequiredMixin, UpdateView):
    model = TeamMember
    form_class = MemberForm
    template_name = 'app/admin/TeamMember/UpdateMember.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Member"


   
class DeleteMember(LoginRequiredMixin, DeleteView):
    model = TeamMember
    template_name = 'app/admin/TeamMember/DeleteMember.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Member"

# ABOUT PAGE MEMBER SOCIAL LINKS
class CreateLink(LoginRequiredMixin, CreateView):
    model = SocialLink
    fields = ['member', 'platform' ,'url']  
    template_name = 'app/admin/TeamMember/Link/CreateLink.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Member'] = TeamMember.objects.all()
        return context
    

class UpdateLink(LoginRequiredMixin, UpdateView):
    model = SocialLink
    form_class = LinkForm  # Use the simplified form
    template_name = 'app/admin/TeamMember/Link/UpdateLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Link"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Member'] = TeamMember.objects.all()
        context['PLATFORM_CHOICES'] = SocialLink.PLATFORM_CHOICES
        return context


class DeleteLink(LoginRequiredMixin, DeleteView):
    model = SocialLink
    template_name = 'app/admin/TeamMember/Link/DeleteLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Link"

 
# INSTRUMENT Image
@login_required
def admin_View(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    InsImage = InstrumentImage.objects.all()
    return render(request, 'app/admin/InstrumentImage/admin_InstrumentImage.html', {'InsImage': InsImage })

class CreateInsView(LoginRequiredMixin, CreateView):
    model = InstrumentImage
    fields = ['instrument', 'view_type',  'image', 'caption']   
    template_name = 'app/admin/InstrumentImage/CreateView.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
    
    

class UpdateInsView(LoginRequiredMixin, UpdateView):
    model = InstrumentImage
    form_class = ViewForm
    template_name = 'app/admin/InstrumentImage/UpdateView.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "View"

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
   
class DeleteInsView(LoginRequiredMixin, DeleteView):
    model = InstrumentImage
    template_name = 'app/admin/InstrumentImage/DeleteView.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "View"

# SIGNIFICANCE
@login_required
def admin_Significance(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Significance = CulturalSignificance.objects.all()
    
    return render(request, 'app/admin/Significance/admin_Significance.html', {'Significance' : Significance })


class CreateSignificance(LoginRequiredMixin, CreateView):
    model = CulturalSignificance
    fields = ['instrument', 'description']   
    template_name = 'app/admin/Significance/CreateSignificance.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
    
    
class UpdateSignificance(LoginRequiredMixin, UpdateView):
    model = CulturalSignificance
    form_class = SignificanceForm
    template_name = 'app/admin/Significance/UpdateSignificance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Significance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context


class DeleteSignificance(LoginRequiredMixin, DeleteView):
    model = CulturalSignificance
    template_name = 'app/admin/Significance/DeleteSignificance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Significance"


# FUN FACT
@login_required
def admin_FunFact(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    FunFact = Funfact.objects.all()
    
    return render(request, 'app/admin/FunFact/admin_FunFact.html', {'FunFact' : FunFact })


class CreateFunFact(LoginRequiredMixin, CreateView):
    model = Funfact
    fields = ['instrument', 'description']   
    template_name = 'app/admin/FunFact/CreateFunfact.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
    
    
class UpdateFunFact(LoginRequiredMixin, UpdateView):
    model = Funfact
    form_class = FunFactForm
    template_name = 'app/admin/FunFact/UpdateFunfact.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "FunFact"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context


class DeleteFunFact(LoginRequiredMixin, DeleteView):
    model = Funfact
    template_name = 'app/admin/FunFact/DeleteFunfact.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "FunFact"


# HOMEPAGE
@login_required
def admin_HomePage(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    HomePages = HomePage.objects.all()
    
    return render(request, 'app/admin/HomePage/admin_HomePage.html', {'HomePages' : HomePages })

class CreateTagline(LoginRequiredMixin, CreateView):
    model = Tagline
    fields = ['icon', 'title']   
    template_name = 'app/admin/HomePage/Tagline/CreateTagline.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
class UpdateTagline(LoginRequiredMixin, UpdateView):
    model = Tagline
    form_class = TaglineForm
    template_name = 'app/admin/HomePage/Tagline/UpdateTagline.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "tagline"


class DeleteTagline(LoginRequiredMixin, DeleteView):
    model = Tagline
    template_name = 'app/admin/HomePage/Tagline/DeleteTagline.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Tagline"


class CreateHomePage(LoginRequiredMixin, CreateView):
    model = HomePage
    fields = ['main_heading', 'highlight_word', 'description']   
    template_name = 'app/admin/HomePage/CreateHomePage.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
class UpdateHomePage(LoginRequiredMixin, UpdateView):
    model = HomePage
    form_class = HomePageForm
    template_name = 'app/admin/HomePage/UpdateHomePage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "HomePage"


class DeleteHomePage(LoginRequiredMixin, DeleteView):
    model = HomePage
    template_name = 'app/admin/HomePage/DeleteHomePage.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "HomePage"






# FOOTERS
@login_required
def admin_Footers(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    socialMedia = SocialMediaLink.objects.all()
    footers = FooterSettings.objects.all()
    return render(request, 'app/admin/Footers/admin_Footer.html', {'socialMedia': socialMedia, 'footers' : footers })

class CreateFooters(LoginRequiredMixin, CreateView):
    model = FooterSettings
    fields = ['follow_us_title', 'follow_us_description']    
    template_name = 'app/admin/Footers/CreateFooters.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)

    
class UpdateFooters(LoginRequiredMixin, UpdateView):
    model = FooterSettings
    form_class = FootersForm
    template_name = 'app/admin/Footers/UpdateFooters.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Footers"

   
class DeleteFooters(LoginRequiredMixin, DeleteView):
    model = FooterSettings
    template_name = 'app/admin/Footers/DeleteFooters.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Footers"


@login_required
def socialmedia_approval(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    socialMedia = get_object_or_404(SocialMediaLink, pk=pk)
    socialMedia.is_active = 'is_active' in request.POST
    socialMedia.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_Footer'))


class CreatesocialMedia(LoginRequiredMixin, CreateView):
    model = SocialMediaLink
    fields = ['platform', 'url']    
    template_name = 'app/admin/Footers/Link/CreateLink.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)

    
class UpdatesocialMedia(LoginRequiredMixin, UpdateView):
    model = SocialMediaLink
    form_class = SocialMediaForm
    template_name = 'app/admin/Footers/Link/UpdateLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "socialMedia"

   
class DeletesocialMedia(LoginRequiredMixin, DeleteView):
    model = SocialMediaLink
    template_name = 'app/admin/Footers/Link/DeleteLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "socialMedia"



# Performances Appointment
@login_required
def admin_performance(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    Performances = PerformanceAppointment.objects.all()
    Lessons = LessonAppointment.objects.all()
    return render(request, 'app/admin/Appointment/admin_Appointment.html', {'Performances': Performances, 'Lessons': Lessons })

class CreatePerformance(LoginRequiredMixin, CreateView):
    model = PerformanceAppointment
    fields = ['event_name', 'event_type', 'event_location', 'event_date', 'event_time', 'message']  # Removed 'user' from fields
    template_name = 'app/admin/Appointment/Performance/CreatePerformance.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically set the logged-in user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # You can set initial values here if needed
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You might not need all users anymore, but keeping if needed elsewhere
        context['Users'] = CustomUser.objects.all()
        context['current_user'] = self.request.user
        return context
    
class UpdatePerformance(LoginRequiredMixin, UpdateView):
    model = PerformanceAppointment
    form_class = PerformanceForm
    template_name = 'app/admin/Appointment/Performance/UpdatePerformance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "performances"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        return context
 
@login_required
def performance_Status(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    Performance = get_object_or_404(PerformanceAppointment, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        decline_reason = request.POST.get('decline_reason', '').strip()
        
        if status in ['Pending', 'Accepted', 'Declined', 'Completed']:
            # Only update decline_reason if status is being set to Declined
            if status == 'Declined':
                PerformanceAppointment.objects.filter(pk=pk).update(
                    status=status, 
                    decline_reason=decline_reason
                )
                messages.success(request, f'Performance has been declined. Reason: {decline_reason}')
            else:
                # Clear decline reason if status is changed from Declined to something else
                PerformanceAppointment.objects.filter(pk=pk).update(
                    status=status, 
                    decline_reason=''
                )
                messages.success(request, f'Performance status has been updated to {status}.')
        else:
            messages.error(request, 'Invalid status.')
        return redirect('admin_main')  # Redirect back to the admin dashboard
    
    return render(request, 'app/admin/Appointment/Performance/PerformanceStatus.html', {'Performance': Performance})

class DeletePerformance(LoginRequiredMixin, DeleteView):
    model = PerformanceAppointment
    template_name = 'app/admin/Appointment/Performance/DeletePerformance.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Performance"


class CreateLesson(LoginRequiredMixin, CreateView):
    model = LessonAppointment
    fields = ['school_name', 'class_size', 'lesson_date', 'lesson_time', 'location' , 'message']  # Removed 'user' from fields
    template_name = 'app/admin/Appointment/Lesson/CreateLesson.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically set the logged-in user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # You can set initial values here if needed
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You might not need all users anymore, but keeping if needed elsewhere
        context['Users'] = CustomUser.objects.all()
        context['current_user'] = self.request.user
        return context
    
class UpdateLesson(LoginRequiredMixin, UpdateView):
    model = LessonAppointment
    form_class = LessonForm
    template_name = 'app/admin/Appointment/Lesson/UpdateLesson.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        return context
   
@login_required
def Lesson_Status(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    Lesson = get_object_or_404(LessonAppointment, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        decline_reason = request.POST.get('decline_reason', '').strip()
        
        if status in ['Pending', 'Accepted', 'Declined', 'Completed']:
            # Only update decline_reason if status is being set to Declined
            if status == 'Declined':
                LessonAppointment.objects.filter(pk=pk).update(
                    status=status, 
                    decline_reason=decline_reason
                )
                messages.success(request, f'Lesson has been declined. Reason: {decline_reason}')
            else:
                # Clear decline reason if status is changed from Declined to something else
                LessonAppointment.objects.filter(pk=pk).update(
                    status=status, 
                    decline_reason=''
                )
                messages.success(request, f'Lesson status has been updated to {status}.')
        else:
            messages.error(request, 'Invalid status.')
        return redirect('admin_main')  # Redirect back to the admin dashboard
    
    return render(request, 'app/admin/Appointment/Lesson/LessonStatus.html', {'Lesson': Lesson})

class DeleteLesson(LoginRequiredMixin, DeleteView):
    model = LessonAppointment
    template_name = 'app/admin/Appointment/Lesson/DeleteLesson.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "Lesson"

# INSTRUMENT 3D MODELS
@login_required
def admin_threeD(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    threeD = Instrument3DModel.objects.all()
    return render(request, 'app/admin/3D Model/admin_3DModel.html', {'threeD': threeD })

class CreatethreeD(LoginRequiredMixin, CreateView):
    model = Instrument3DModel
    fields = ['instrument', 'file']  
    template_name = 'app/admin/3D Model/Create3D.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            # Check if instrument already has a 3D model
            instrument = form.cleaned_data['instrument']
            if Instrument3DModel.objects.filter(instrument=instrument).exists():
                form.add_error('instrument', 'This instrument already has a 3D model. Please update the existing one instead.')
                return self.form_invalid(form)
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get instruments that don't have 3D models yet
        instruments_with_3d = Instrument3DModel.objects.values_list('instrument_id', flat=True)
        context['Instruments'] = Instrument.objects.exclude(id__in=instruments_with_3d)
        return context
    

class UpdatethreeD(LoginRequiredMixin, UpdateView):
    model = Instrument3DModel
    form_class = threeDForm
    template_name = 'app/admin/3D Model/Update3D.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = 'threeD'

    def form_valid(self, form):
        if form.is_valid():
            # For update, we need to handle the case where instrument is changed
            # but check if the new instrument already has a 3D model
            new_instrument = form.cleaned_data['instrument']
            current_3d_model = self.get_object()
            
            # If instrument is being changed to one that already has a 3D model
            if new_instrument != current_3d_model.instrument:
                if Instrument3DModel.objects.filter(instrument=new_instrument).exists():
                    form.add_error('instrument', 'This instrument already has a 3D model. Please choose a different instrument.')
                    return self.form_invalid(form)
            
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get instruments that don't have 3D models yet, plus the current instrument
        current_3d_model = self.get_object()
        instruments_with_3d = Instrument3DModel.objects.exclude(
            instrument=current_3d_model.instrument
        ).values_list('instrument_id', flat=True)
        
        context['Instruments'] = Instrument.objects.exclude(id__in=instruments_with_3d)
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Set the initial queryset for the instrument field
        current_3d_model = self.get_object()
        instruments_with_3d = Instrument3DModel.objects.exclude(
            instrument=current_3d_model.instrument
        ).values_list('instrument_id', flat=True)
        
        form.fields['instrument'].queryset = Instrument.objects.exclude(id__in=instruments_with_3d)
        return form
    
class DeletethreeD(LoginRequiredMixin, DeleteView):
    model = Instrument3DModel
    template_name = 'app/admin/3D Model/Delete3D.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "threeD"


# PRINCIPLE
@login_required
def admin_3dContent(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    sitecontent = Site3DContent.objects.all()
    return render(request, 'app/admin/3D Content/admin_3dContent.html', {'sitecontent': sitecontent })


class Create3dContent(LoginRequiredMixin, CreateView):
    model = Site3DContent
    fields = ['hero_title', 'hero_description', 'about_title', 'about_content', 'about_image'] 
    template_name = 'app/admin/3D Content/Create3dContent.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
        

class Update3dContent(LoginRequiredMixin, UpdateView):
    model = Site3DContent
    form_class = sitecontentForm
    template_name = 'app/admin/3D Content/Update3dContent.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "sitecontent"

   
class Delete3dContent(LoginRequiredMixin, DeleteView):
    model = Site3DContent
    template_name = 'app/admin/3D Content/Delete3dContent.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "sitecontent"

# INSTRUMENT LINKS
@login_required
def admin_InsLink(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    InsLink = InstrumentLink.objects.all()
    return render(request, 'app/admin/InstrumentLinks/admin_InsLink.html', {'InsLink': InsLink })


class CreateInsLink(LoginRequiredMixin, CreateView):
    model = InstrumentLink
    fields = ['instrument', 'title', 'url', 'link_type'] 
    template_name = 'app/admin/InstrumentLinks/CreateInsLink.html'
    success_url = reverse_lazy('admin_main')
   
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context
     
@login_required
def primary_source_approve(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    primary_source = get_object_or_404(InstrumentLink, pk=pk)
    
    # Check if the checkbox was checked or unchecked
    if request.method == 'POST':
        is_primary = 'is_primary_source' in request.POST
        primary_source.is_primary_source = is_primary
        primary_source.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'admin_InsLink'))

class UpdateInsLink(LoginRequiredMixin, UpdateView):
    model = InstrumentLink
    form_class = InsLinkForm
    template_name = 'app/admin/InstrumentLinks/UpdateInsLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "link"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Instruments'] = Instrument.objects.all()
        return context

   
class DeleteInsLink(LoginRequiredMixin, DeleteView):
    model = InstrumentLink
    template_name = 'app/admin/InstrumentLinks/DeleteInsLink.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "link"












@login_required
def user_main(request):
    if request.user.role != 'user':
        return redirect('admin_main')

    try:
        users = CustomUser.objects.all()
        categorys = InstrumentCategory.objects.all()
        regions = Region.objects.all()
        Materials = Material.objects.all()
        Instruments = Instrument.objects.all()
        Feedbacks = Feedback.objects.all()
        testimonials = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
        Tutorials = VideoTutorial.objects.all()
        popular_instruments = Instrument.objects.order_by('-views')[:4]
        
        # Use get_or_create to ensure these exist
        contact, _ = ContactPage.objects.get_or_create(
            pk=1,
            defaults={'title': 'Contact Us', 'content': 'Default contact information'}
        )
        
        taglines, _ = Tagline.objects.get_or_create(
            pk=1, 
            defaults={'text': 'Welcome to Philharmonia'}
        )
        
        homepages, _ = HomePage.objects.get_or_create(
            pk=1,
            defaults={'title': 'Home', 'content': 'Welcome to our site'}
        )
        
        footer_settings, _ = FooterSettings.objects.get_or_create(
            pk=1,
            defaults={'copyright_text': '© 2024 Philharmonia'}
        )
        
        social_links = SocialMediaLink.objects.all()
        Performances = PerformanceAppointment.objects.all()
        Lesson = LessonAppointment.objects.all()
        section = DiscoverSection.objects.all()
        
        # Guiding principle might not exist
        guiding_principle = GuidingPrinciples.objects.prefetch_related('cards').first()

        return render(request, 'app/user/home.html', {
            'users': users,
            'categorys': categorys,
            'regions': regions,
            'Materials': Materials,
            'Instruments': Instruments,
            'Feedbacks': Feedbacks,
            'testimonials': testimonials,
            'Tutorials': Tutorials,
            'popular_instruments': popular_instruments,
            'guiding_principle': guiding_principle,
            'section': section,
            'contact': contact,
            'taglines': taglines, 
            'homepages': homepages,
            'social_links': social_links,
            'footer_settings': footer_settings,
            'Performances': Performances,
            'Lesson': Lesson
        })
        
    except Exception as e:
        # Log the error and show a simple page
        print(f"Error in user_main: {e}")
        import traceback
        traceback.print_exc()
        
        # Return a simple error page or redirect
        from django.http import HttpResponse
        return HttpResponse(f"Error loading page: {str(e)}. Please contact admin.")

class AppointmentView(LoginRequiredMixin, CreateView):
    template_name = 'app/user/appointment/Appointment.html'

    def get_form_class(self):
        if self.request.method == 'POST':
            if 'event_name' in self.request.POST:
                return PerformanceAppointmentForm
            elif 'school_name' in self.request.POST:
                return LessonAppointmentForm
        return PerformanceAppointmentForm

    def get_model(self):
        form_class = self.get_form_class()
        return PerformanceAppointment if form_class == PerformanceAppointmentForm else LessonAppointment

    def form_valid(self, form):
        form.instance.user = self.request.user
        appointment = form.save()
        
        # Return JSON for AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': ''
            })
        
        # For non-AJAX, you might want to handle differently
        messages.success(self.request, 'Appointment submitted successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Return JSON for AJAX errors
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {field: [str(e) for e in error] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False, 
                'errors': errors
            }, status=400)
        
        # Show validation errors in normal POST
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # This won't be used for AJAX requests
        return reverse('user_home')
    
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def check_date_availability(request):
    """API endpoint to check if a date is already booked"""
    try:
        data = json.loads(request.body)
        date_str = data.get('date')
        appointment_type = data.get('appointment_type', 'performance')
        
        if not date_str:
            return JsonResponse({'available': True})  # Default to available if no date provided
        
        from datetime import datetime
        from django.utils import timezone
        check_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check for existing appointments on the same date
        existing_performance = False
        existing_lesson = False
        
        if appointment_type == 'performance':
            # For performance form, check both performance and lesson appointments
            existing_performance = PerformanceAppointment.objects.filter(
                event_date=check_date,
                status='Accepted'
            ).exists()
            
            existing_lesson = LessonAppointment.objects.filter(
                lesson_date=check_date,
                status='Accepted'
            ).exists()
        else:
            # For lesson form, check both performance and lesson appointments
            existing_performance = PerformanceAppointment.objects.filter(
                event_date=check_date,
                status='Accepted'
            ).exists()
            
            existing_lesson = LessonAppointment.objects.filter(
                lesson_date=check_date,
                status='Accepted'
            ).exists()
        
        if existing_performance:
            return JsonResponse({
                'available': False,
                'message': f"We already have an accepted performance appointment on {check_date}. Please choose a different date."
            })
        
        if existing_lesson:
            return JsonResponse({
                'available': False,
                'message': f"We already have an accepted lesson appointment on {check_date}. Please choose a different date."
            })
        
        return JsonResponse({'available': True})
        
    except Exception as e:
        print(f"Error checking date availability: {e}")
        return JsonResponse({'available': True})  # Default to available on error
# Update user profile (including photo)
@login_required
def update_profile(request, user_id):
    try:
        # Get the user object
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Ensure users can only see their own profile
        if request.user != user:
            return redirect('user_home' if request.user.role == 'user' else 'admin_main')

        # Get the logged-in user's appointments
        try:
            from .models import PerformanceAppointment, LessonAppointment
            
            # Get performance appointments for the logged-in user
            performance_appointments = PerformanceAppointment.objects.filter(
                user=request.user  # Use request.user instead of user parameter
            ).order_by('-created_at')[:5]  # Show latest 5 appointments
            
            # Get lesson appointments for the logged-in user
            lesson_appointments = LessonAppointment.objects.filter(
                user=request.user  # Use request.user instead of user parameter
            ).order_by('-created_at')[:5]  # Show latest 5 appointments
            
            has_appointments = performance_appointments.exists() or lesson_appointments.exists()
            
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            import traceback
            traceback.print_exc()
            performance_appointments = None
            lesson_appointments = None
            has_appointments = False

        if request.method == 'POST':
            form = CustomUserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('user_home')
        else:
            form = CustomUserForm(instance=user)

        context = {
            'form': form,
            'user': user,
            'performance_appointments': performance_appointments,
            'lesson_appointments': lesson_appointments,
            'has_appointments': has_appointments,
        }
        
        return render(request, 'app/user/update-profile.html', context)
        
    except Exception as e:
        # Log the error and show a simple page
        print(f"Error in update_profile: {e}")
        import traceback
        traceback.print_exc()
        
        # Return a simple error page or redirect with message
        messages.error(request, f"Error loading profile: {str(e)}. Please try again.")
        return redirect('user_home' if request.user.role == 'user' else 'admin_main')


@login_required
def update_performance(request, pk):
    """Update a performance appointment (user only)"""
    appointment = get_object_or_404(PerformanceAppointment, pk=pk)
    
    # Ensure only the owner can update their appointment
    if appointment.user != request.user:
        messages.error(request, 'You can only update your own appointments.')
        return redirect('user_home')
    
    # Ensure only pending appointments can be updated
    if appointment.status != 'Pending':
        messages.error(request, 'Only pending appointments can be updated.')
        return redirect('user_home')
    
    if request.method == 'POST':
        # Get form data
        event_name = request.POST.get('event_name', '').strip()
        event_type = request.POST.get('event_type', '').strip()
        event_location = request.POST.get('event_location', '').strip()
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not all([event_name, event_location, event_date, event_time]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('user_home')
        
        try:
            # Update appointment
            appointment.event_name = event_name
            appointment.event_type = event_type if event_type else None
            appointment.event_location = event_location
            appointment.event_date = event_date
            appointment.event_time = event_time
            appointment.message = message if message else None
            appointment.save()
            
            messages.success(request, 'Performance appointment updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating appointment: {str(e)}')
        
        return redirect('user_home')
    
    # If GET request, redirect to home
    return redirect('user_home')

@login_required
def update_lesson(request, pk):
    """Update a lesson appointment (user only)"""
    appointment = get_object_or_404(LessonAppointment, pk=pk)
    
    # Ensure only the owner can update their appointment
    if appointment.user != request.user:
        messages.error(request, 'You can only update your own appointments.')
        return redirect('user_home')
    
    # Ensure only pending appointments can be updated
    if appointment.status != 'Pending':
        messages.error(request, 'Only pending appointments can be updated.')
        return redirect('user_home')
    
    if request.method == 'POST':
        # Get form data
        school_name = request.POST.get('school_name', '').strip()
        class_size = request.POST.get('class_size', '1')
        location = request.POST.get('location', '').strip()
        lesson_date = request.POST.get('lesson_date')
        lesson_time = request.POST.get('lesson_time')
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not all([school_name, location, lesson_date, lesson_time]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('user_home')
        
        try:
            # Update appointment
            appointment.school_name = school_name
            appointment.class_size = int(class_size)
            appointment.location = location
            appointment.lesson_date = lesson_date
            appointment.lesson_time = lesson_time
            appointment.message = message if message else None
            appointment.save()
            
            messages.success(request, 'Lesson appointment updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating appointment: {str(e)}')
        
        return redirect('user_home')
    
    # If GET request, redirect to home
    return redirect('user_home')

@login_required
def cancel_performance(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(PerformanceAppointment, id=appointment_id, user=request.user)
        appointment.delete()
        messages.success(request, "Performance appointment canceled successfully.")
    return redirect('user_home')

@login_required
def cancel_lesson(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(LessonAppointment, id=appointment_id, user=request.user)
        appointment.delete()
        messages.success(request, "Lesson appointment canceled successfully.")
    return redirect('user_home')

    
class UserUpdatePerformance(LoginRequiredMixin, UpdateView):
    model = PerformanceAppointment
    form_class = UserPerformanceForm
    template_name = 'app/user/appointment/UpdatePerformance.html'
    success_url = reverse_lazy('user_home')
    context_object_name = "performance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        return context

class UserDeletePerformance(LoginRequiredMixin, DeleteView):
    model = PerformanceAppointment
    template_name = 'app/user/appointment/DeletePerformance.html'
    success_url = reverse_lazy('user_home')
    context_object_name = "Performance"

    
class UserUpdateLesson(LoginRequiredMixin, UpdateView):
    model = LessonAppointment
    form_class = UserLessonForm
    template_name = 'app/user/appointment/UpdateLesson.html'
    success_url = reverse_lazy('user_home')
    context_object_name = "Lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Users'] = CustomUser.objects.all()
        return context

class UserDeleteLesson(LoginRequiredMixin, DeleteView):
    model = LessonAppointment
    template_name = 'app/user/appointment/DeleteLesson.html'
    success_url = reverse_lazy('user_home')
    context_object_name = "Lesson"










class UserVideoTutorialPageView(TemplateView):
    template_name = 'app/user/VideoTutorial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['categories'] = InstrumentCategory.objects.all()
        context['featured_videos'] = VideoTutorial.objects.all().order_by('-uploaded_at')

        return context
    
@csrf_exempt
def increment_video_view(request, video_id):
    if request.method == 'POST':
        try:
            video = VideoTutorial.objects.get(id=video_id)
            video.views += 1
            video.save()
            return JsonResponse({'status': 'success', 'views': video.views})
        except VideoTutorial.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Video not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

class UserAboutPageView(TemplateView):
    template_name = 'app/user/user_About.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the GuidingPrinciples instance (assuming you have one)
        guiding_principles = GuidingPrinciples.objects.first()
        
        # Add to template context
        context['guiding_principles'] = guiding_principles
        context['Offerings'] = Offering.objects.all()
        context['CulturalImportances'] = CulturalImportance.objects.all()
        context['Instruments'] = Instrument.objects.all()
        context['TargetAudiences'] = TargetAudience.objects.all()
        context['TeamMembers'] = TeamMember.objects.all()
        context['SocialLinks'] = SocialLink.objects.all()
        context['contact'] = ContactPage.objects.first()
        context['taglines'] = Tagline.objects.first()
        context['homepages'] = HomePage.objects.first()
        context['testimonials'] = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
        context['social_links'] = SocialMediaLink.objects.all()
        context['footer_settings'] = FooterSettings.objects.first()
        
        # Alternatively, if you want to get Mission and Vision cards directly:
        mission = PrincipleCard.objects.filter(card_type='Mission').first()
        vision = PrincipleCard.objects.filter(card_type='Vision').first()
        
        context['mission'] = mission
        context['vision'] = vision
        
        return context
    
class UserContactPageView(TemplateView):
    template_name = 'app/user/user_Contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create the contact page configuration
        contact_config, created = ContactPage.objects.get_or_create(pk=1)
        
        # Add instruments and contact configuration to context
        context['Instruments'] = Instrument.objects.all()
        context['contact_config'] = contact_config
        context['subject_choices'] = ContactMessage.Subject  # Add subject choices to context
        
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request handling
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Create and save the message - FIXED VERSION
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,  # THIS IS THE FIX!
                name=name,
                email=email,
                subject=subject,
                message=message,
                submitted_at=timezone.now()
            )
            
            return JsonResponse({
                'success': True,
                'name': name,
                'email': email,
                'subject': dict(ContactMessage.Subject).get(subject, subject)
            })
        
        # Regular form submission (fallback)
        return super().post(request, *args, **kwargs)
    
# FUN FACT
@login_required
def admin_ContactMessage(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    ContactMessages = ContactMessage.objects.all()
    
    return render(request, 'app/admin/ContactMessages/admin_ContactMessages.html', {'ContactMessages' : ContactMessages })

class DeleteContactMessage(LoginRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = 'app/admin/ContactMessage/DeleteContact.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "contact"

class ViewContactMessage(LoginRequiredMixin, UpdateView):
    model = ContactMessage
    fields = ['name','email', 'subject', 'message', 'submitted_at' ]
    template_name = 'app/admin/ContactMessage/VIewContact.html'
    success_url = reverse_lazy('admin_main')
    context_object_name = "message"


class UserModels3d(TemplateView):
    template_name = 'app/user/3dModel.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Get the GuidingPrinciples instance (assuming you have one)
            guiding_principles = GuidingPrinciples.objects.first()
            
            # Add to template context
            context['guiding_principles'] = guiding_principles
            context['Offerings'] = Offering.objects.all()
            context['CulturalImportances'] = CulturalImportance.objects.all()
            context['TargetAudiences'] = TargetAudience.objects.all()
            context['Instruments'] = Instrument.objects.all()
            context['three_d'] = Instrument3DModel.objects.all()
            context['TeamMembers'] = TeamMember.objects.all()
            context['SocialLinks'] = SocialLink.objects.all()
            context['contact'] = ContactPage.objects.first()
            context['taglines'] = Tagline.objects.first()
            context['homepages'] = HomePage.objects.first()
            context['testimonials'] = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
            context['social_links'] = SocialMediaLink.objects.all()
            context['footer_settings'] = FooterSettings.objects.first()
            context['3dContent'] = Site3DContent.objects.first()
            
            # Alternatively, if you want to get Mission and Vision cards directly:
            mission = PrincipleCard.objects.filter(card_type='Mission').first()
            vision = PrincipleCard.objects.filter(card_type='Vision').first()
            
            context['mission'] = mission
            context['vision'] = vision
            
            return context






# FrontPageView (for login and register modals)
class FrontPageView(TemplateView):
    template_name = 'app/login/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = UserLoginForm()
        context['register_form'] = UserRegisterForm()

        # Add public data from database
        context['categorys'] = InstrumentCategory.objects.all()
        context['regions'] = Region.objects.all()
        context['Materials'] = Material.objects.all()
        context['Instruments'] = Instrument.objects.all()
        context['Feedbacks'] = Feedback.objects.all()
        context['testimonials'] = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
        context['Tutorials'] = VideoTutorial.objects.all()
        context['popular_instruments'] = Instrument.objects.order_by('-views')[:4]
        context['section'] = DiscoverSection.objects.all()
        context['guiding_principle'] = GuidingPrinciples.objects.prefetch_related('cards').first()
        context['Offerings'] = Offering.objects.all()
        context['CulturalImportances'] = CulturalImportance.objects.all()
        context['TargetAudiences'] = TargetAudience.objects.all()
        context['TeamMembers'] = TeamMember.objects.all()
        context['SocialLinks'] = SocialLink.objects.all()
        context['contact'] = ContactPage.objects.first()
        context['taglines'] = Tagline.objects.first()
        context['homepages'] = HomePage.objects.first()
        context['social_links'] = SocialMediaLink.objects.all()
        context['footer_settings'] = FooterSettings.objects.first()


        return context

class VideoTutorialPageView(TemplateView):
    template_name = 'app/login/VideoTutorial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['categories'] = InstrumentCategory.objects.all()
        context['featured_videos'] = VideoTutorial.objects.all().order_by('-uploaded_at')

        return context
    
class AboutPageView(TemplateView):
    template_name = 'app/login/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the GuidingPrinciples instance (assuming you have one)
        guiding_principles = GuidingPrinciples.objects.first()
        
        # Add to template context
        context['guiding_principles'] = guiding_principles
        context['Offerings'] = Offering.objects.all()
        context['CulturalImportances'] = CulturalImportance.objects.all()
        context['TargetAudiences'] = TargetAudience.objects.all()
        context['Instruments'] = Instrument.objects.all()
        context['TeamMembers'] = TeamMember.objects.all()
        context['SocialLinks'] = SocialLink.objects.all()
        context['contact'] = ContactPage.objects.first()
        context['taglines'] = Tagline.objects.first()
        context['homepages'] = HomePage.objects.first()
        context['testimonials'] = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
        context['social_links'] = SocialMediaLink.objects.all()
        context['footer_settings'] = FooterSettings.objects.first()
        
        # Alternatively, if you want to get Mission and Vision cards directly:
        mission = PrincipleCard.objects.filter(card_type='Mission').first()
        vision = PrincipleCard.objects.filter(card_type='Vision').first()
        
        context['mission'] = mission
        context['vision'] = vision
        
        return context
    
class ContactPageView(TemplateView):
    template_name = 'app/login/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create the contact page configuration
        contact_config, created = ContactPage.objects.get_or_create(pk=1)
        
        # Add instruments and contact configuration to context
        context['Instruments'] = Instrument.objects.all()
        context['contact_config'] = contact_config
        context['subject_choices'] = ContactMessage.Subject  # Add subject choices to context
        
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request handling
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Create and save the message
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                submitted_at=timezone.now()
            )
            
            return JsonResponse({
                'success': True,
                'name': name,
                'email': email,
                'subject': dict(ContactMessage.Subject).get(subject, subject)
            })
        
        # Regular form submission (fallback)
        return super().post(request, *args, **kwargs)
    
class Models3d(TemplateView):
    template_name = 'app/login/3dModel.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Get the GuidingPrinciples instance (assuming you have one)
            guiding_principles = GuidingPrinciples.objects.first()
            
            # Add to template context
            context['guiding_principles'] = guiding_principles
            context['Offerings'] = Offering.objects.all()
            context['CulturalImportances'] = CulturalImportance.objects.all()
            context['TargetAudiences'] = TargetAudience.objects.all()
            context['Instruments'] = Instrument.objects.all()
            context['three_d'] = Instrument3DModel.objects.all()
            context['TeamMembers'] = TeamMember.objects.all()
            context['SocialLinks'] = SocialLink.objects.all()
            context['contact'] = ContactPage.objects.first()
            context['taglines'] = Tagline.objects.first()
            context['homepages'] = HomePage.objects.first()
            context['testimonials'] = Testimonial.objects.filter(approved=True).order_by('-date_submitted')[:5]
            context['social_links'] = SocialMediaLink.objects.all()
            context['footer_settings'] = FooterSettings.objects.first()
            context['3dContent'] = Site3DContent.objects.first()
            
            # Alternatively, if you want to get Mission and Vision cards directly:
            mission = PrincipleCard.objects.filter(card_type='Mission').first()
            vision = PrincipleCard.objects.filter(card_type='Vision').first()
            
            context['mission'] = mission
            context['vision'] = vision
            
            return context
    

# =====================
# HEALTH CHECK (for Render)
# =====================
import time
import os
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    """Simple health check endpoint for Render"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'philharmonia',
        'timestamp': time.time(),
        'environment': 'production' if os.environ.get('RENDER') else 'development'
    })