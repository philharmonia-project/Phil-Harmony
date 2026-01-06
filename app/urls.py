from django.urls import path, include
from app.views import health_check  # ADD THIS LINE
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (user_main, AboutPageView, Models3d ,ContactPageView ,VideoTutorialPageView,
                    UserAboutPageView, UserContactPageView, UserVideoTutorialPageView, UserModels3d,
                    register, login_view, logout_view, FrontPageView, increment_video_view,
                    admin_main, set_user_as_admin, remove_user_as_admin, delete_user,  
                    admin_instrument, InstrumentDetailView, UpdateInstrument, DeleteInstrument, CreateInstrument,
                    admin_History, CreatePage, UpdatePage, DeletePage,
                    CreateSection, UpdateSection, DeleteSection,
                    admin_category, CreateCategory, UpdateCategory, DeleteCategory, CategoryDetailView,
                    admin_tribe, CreateTribe, UpdateTribe, DeleteTribe, TribeDetailView,
                    admin_material, CreateMaterial, UpdateMaterial, DeleteMaterial, MaterialDetailView,
                    CreateInsMaterial, UpdateInsMaterial, DeleteInsMaterial,
                    admin_Step, CreateStep, UpdateStep, DeleteStep,
                    admin_feedback, CreateFeedback, UpdateFeedback, DeleteFeedback, FeedbackDetailView,
                    admin_testimonial, CreateTestimonial, UpdateTestimonial, DeleteTestimonial,
                    admin_tutorial, CreateTutorial, UpdateTutorial, DeleteTutorial, TutorialDetailView,
                    admin_Technique, CreateTechnique, UpdateTechnique, DeleteTechnique,
                    admin_instructor, CreateInstructor, UpdateInstructor, DeleteInstructor,
                    admin_principle, CreatePrinciple, UpdatePrinciple, DeletePrinciple,
                    CreatePrincipleCard, UpdatePrincipleCard, DeletePrincipleCard,
                    admin_ContactPage, CreateContactPage, UpdateContactPage, DeleteContactPage, 
                    admin_ContactMessage, DeleteContactMessage,ViewContactMessage,
                    admin_Sound, CreateSound, UpdateSound, DeleteSound,
                    admin_Offering, CreateOffering, UpdateOffering, DeleteOffering,
                    admin_Importance, CreateImportance, UpdateImportance, DeleteImportance,
                    admin_Audience, CreateAudience, UpdateAudience, DeleteAudience,
                    admin_Member, CreateMember, UpdateMember, DeleteMember,
                    CreateLink, UpdateLink, DeleteLink,
                    admin_View, CreateInsView, UpdateInsView, DeleteInsView,
                    admin_Significance, CreateSignificance, UpdateSignificance, DeleteSignificance,
                    admin_FunFact, CreateFunFact, UpdateFunFact, DeleteFunFact,
                    admin_Footers, CreateFooters, UpdateFooters, DeleteFooters,
                    CreatesocialMedia, UpdatesocialMedia, DeletesocialMedia,
                    admin_HomePage, CreateHomePage, UpdateHomePage, DeleteHomePage,
                    CreateTagline, UpdateTagline, DeleteTagline,
                    admin_performance, CreatePerformance, UpdatePerformance, DeletePerformance,
                    CreateLesson, UpdateLesson, DeleteLesson, AppointmentView,
                    admin_threeD, CreatethreeD, UpdatethreeD, DeletethreeD,
                    admin_3dContent, Create3dContent, Update3dContent, Delete3dContent,
                    admin_InsLink, CreateInsLink, UpdateInsLink, DeleteInsLink,
                    UserDeleteLesson, UserDeletePerformance, UserUpdateLesson, UserUpdatePerformance,
                    get_chart_data, get_category_chart_data, get_login_chart_data, check_auth_status, get_user_info)



urlpatterns = [
# GOOGLE ACCOUNT
    path('accounts/', include('allauth.urls')),
    path('health/', health_check, name='health_check'),  # ADD THIS LINE
    path('check-auth-status/', check_auth_status, name='check_auth_status'),
    path('get-user-info/', get_user_info, name='get_user_info'),

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-management/forums/<int:forum_id>/toggle-status/', views.toggle_forum_status, name='toggle_forum_status'),
    path('admin-management/messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('admin-management/forums/<int:forum_id>/delete-all-messages/', views.delete_all_forum_messages, name='delete_all_forum_messages'),
    path('admin-management/main/', views.admin_main, name='admin_main'),
    # ADMIN
    path('admin_main/', admin_main, name='admin_main'),


      # For admin interface
    path('set-admin/<int:user_id>/', set_user_as_admin, name='set_admin'),  # set new admin
    path('remove-admin/<int:user_id>/', remove_user_as_admin, name='remove_admin'),  # remove-admin URL
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),     # delete admin/user
    path('update_profile/<int:user_id>/', views.update_user_profile, name='update_user_profile'),

    # FOR USER
    path('update_Profile/<int:user_id>/', views.update_profile, name='update_Profile'),

    path('api/instruments/provinces-with-instruments/', views.provinces_with_instruments, name='provinces_with_instruments'),
    path('api/instruments/province/', views.instruments_by_province, name='instruments_by_province'),
    

# For FrontPage
    path('', FrontPageView.as_view(), name='frontpage'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/create/', ContactPageView.as_view(), name='contact'),
    path('video/', VideoTutorialPageView.as_view(), name='video'),
    path('3dModel/', Models3d.as_view(), name='3dModel'),

# For User 
    path('user_home/', user_main, name='user_home'),
    path('User_about/', UserAboutPageView.as_view(), name='User_about'),
    path('User_contact/create/', UserContactPageView.as_view(), name='User_contact'),
    path('User_video/', UserVideoTutorialPageView.as_view(), name='User_video'),
    path('video/<int:video_id>/view/', increment_video_view, name='increment_video_view'),
    path('User_3dModel/', UserModels3d.as_view(), name='User_3dModel'),

    # Philippine Instrument Html
    path('admin_instrument/', admin_instrument, name='admin_instrument'),
    path('admin_instrument/<int:pk>/', InstrumentDetailView.as_view(), name='detail'),
    path('admin_instrument/create/', CreateInstrument.as_view(), name='CreateInstrument'),
    path('admin_instrument/<int:pk>/edit/', UpdateInstrument.as_view(), name='updateInstrument'),
    path('admin_instrument/<int:pk>/delete/', DeleteInstrument.as_view(), name='deleteInstrument'),
    path('api/instruments/province/', views.instruments_by_province, name='instruments_by_province'),
    path('api/instruments/provinces-with-instruments/', views.provinces_with_instruments, name='provinces_with_instruments'),

# HISTORY
    path('admin_History/', admin_History, name='admin_History'),
    path('admin_Page/create/', CreatePage.as_view(), name='CreatePage'),
    path('admin_Page/<int:pk>/edit/', UpdatePage.as_view(), name='UpdatePage'),
    path('admin_Page/<int:pk>/delete/', DeletePage.as_view(), name='DeletePage'),

    path('admin_Section/create/', CreateSection.as_view(), name='CreateSection'),
    path('admin_Section/<int:pk>/edit/', UpdateSection.as_view(), name='UpdateSection'),
    path('admin_Section/<int:pk>/delete/', DeleteSection.as_view(), name='DeleteSection'),

    # Instrument Category Html
    path('admin_category/', admin_category, name='admin_category'),
    path('admin_category/<int:pk>/', CategoryDetailView.as_view(), name='detailCategory'),
    path('admin_category/create/', CreateCategory.as_view(), name='CreateCategory'),
    path('admin_category/<int:pk>/edit/', UpdateCategory.as_view(), name='UpdateCategory'),
    path('admin_category/<int:pk>/delete/', DeleteCategory.as_view(), name='DeleteCategory'),


     # Instrument TRIBE Html
    path('admin_tribe/', admin_tribe, name='admin_tribe'),
    path('admin_tribe/<int:pk>/', TribeDetailView.as_view(), name='detailTribe'),
    path('admin_tribe/create/', CreateTribe.as_view(), name='CreateTribe'),
    path('admin_tribe/<int:pk>/edit/', UpdateTribe.as_view(), name='UpdateTribe'),
    path('admin_tribe/<int:pk>/delete/', DeleteTribe.as_view(), name='DeleteTribe'),

    # MATERIAL Html
    path('admin_material/', admin_material, name='admin_material'),
    path('admin_material/<int:pk>/', MaterialDetailView.as_view(), name='detailMaterial'),
    path('admin_material/create/', CreateMaterial.as_view(), name='CreateMaterial'),
    path('admin_material/<int:pk>/edit/', UpdateMaterial.as_view(), name='UpdateMaterial'),
    path('admin_material/<int:pk>/delete/', DeleteMaterial.as_view(), name='DeleteMaterial'),

    # Instrument MATERIAL Html
    path('admin_insMaterials/create/', CreateInsMaterial.as_view(), name='CreateInsMaterial'),
    path('admin_insMaterials/<int:pk>/edit/', UpdateInsMaterial.as_view(), name='UpdateInsMaterial'),
    path('admin_insMaterials/<int:pk>/delete/', DeleteInsMaterial.as_view(), name='DeleteInsMaterial'),

    # MATERIAL STEPS Html
    path('admin_Step/', admin_Step, name='admin_Step'),
    path('admin_Step/create/', CreateStep.as_view(), name='CreateStep'),
    path('admin_Step/<int:pk>/edit/', UpdateStep.as_view(), name='UpdateStep'),
    path('admin_Step/<int:pk>/delete/', DeleteStep.as_view(), name='DeleteStep'),

    # FEEDBACK  Html
    path('admin_feedback/', admin_feedback, name='admin_feedback'),
    path('admin_feedback/<int:pk>/', FeedbackDetailView.as_view(), name='detailFeedback'),
    path('admin_feedback/create/', CreateFeedback.as_view(), name='CreateFeedback'),
    path('admin_feedback/<int:pk>/edit/', UpdateFeedback.as_view(), name='UpdateFeedback'),
    path('admin_feedback/<int:pk>/delete/', DeleteFeedback.as_view(), name='DeleteFeedback'),
    path('admin_feedback/approve/<int:pk>/', views.feedback_approval, name='feedback_approval'),

    # TESTIMONIAL  Html
    path('admin_testimonial/', admin_testimonial, name='admin_testimonial'),
    path('admin_testimonial/create/', CreateTestimonial.as_view(), name='CreateTestimonial'),
    path('admin_testimonial/<int:pk>/edit/', UpdateTestimonial.as_view(), name='UpdateTestimonial'),
    path('admin_testimonial/<int:pk>/delete/', DeleteTestimonial.as_view(), name='DeleteTestimonial'),
    path('admin_testimonial/approve/<int:pk>/', views.testimonial_approval, name='testimonial_approval'),


    # TURORIAL  Html
    path('admin_tutorial/', admin_tutorial, name='admin_tutorial'),
    path('admin_tutorial/<int:pk>/', TutorialDetailView.as_view(), name='detailTutorial'),
    path('admin_tutorial/create/', CreateTutorial.as_view(), name='CreateTutorial'),
    path('admin_tutorial/<int:pk>/edit/', UpdateTutorial.as_view(), name='UpdateTutorial'),
    path('admin_tutorial/<int:pk>/delete/', DeleteTutorial.as_view(), name='DeleteTutorial'),

    # TURORIAL TECHNIQUE  Html
    path('admin_Technique/', admin_Technique, name='admin_Technique'),
    path('admin_Technique/create/', CreateTechnique.as_view(), name='CreateTechnique'),
    path('admin_Technique/<int:pk>/edit/', UpdateTechnique.as_view(), name='UpdateTechnique'),
    path('admin_Technique/<int:pk>/delete/', DeleteTechnique.as_view(), name='DeleteTechnique'),

    # Instructor Html
    path('admin_instructor/', admin_instructor, name='admin_instructor'),
    path('admin_instructor/create/', CreateInstructor.as_view(), name='CreateInstructor'),
    path('admin_instructor/<int:pk>/edit/', UpdateInstructor.as_view(), name='UpdateInstructor'),
    path('admin_instructor/<int:pk>/delete/', DeleteInstructor.as_view(), name='DeleteInstructor'),

    # Principle Html
    path('admin_principle/', admin_principle, name='admin_principle'),
    path('admin_principle/create/', CreatePrinciple.as_view(), name='CreatePrinciple'),
    path('admin_principle/<int:pk>/edit/', UpdatePrinciple.as_view(), name='UpdatePrinciple'),
    path('admin_principle/<int:pk>/delete/', DeletePrinciple.as_view(), name='DeletePrinciple'),

    # Principle Card Html
    path('admin_principlecard/create/', CreatePrincipleCard.as_view(), name='CreatePrincipleCard'),
    path('admin_principlecard/<int:pk>/edit/', UpdatePrincipleCard.as_view(), name='UpdatePrincipleCard'),
    path('admin_principlecard/<int:pk>/delete/', DeletePrincipleCard.as_view(), name='DeletePrincipleCard'),

    # TURORIAL  Html
    path('admin_Sound/', admin_Sound, name='admin_Sound'),
    path('admin_Sound/create/', CreateSound.as_view(), name='CreateSound'),
    path('admin_Sound/<int:pk>/edit/', UpdateSound.as_view(), name='UpdateSound'),
    path('admin_Sound/<int:pk>/delete/', DeleteSound.as_view(), name='DeleteSound'),

    # admin_ContactPage  Html
    path('admin_ContactPage/', admin_ContactPage, name='admin_ContactPage'),
    path('admin_ContactPage/create/', CreateContactPage.as_view(), name='CreateContactPage'),
    path('admin_ContactPage/<int:pk>/edit/', UpdateContactPage.as_view(), name='UpdateContactPage'),
    path('admin_ContactPage/<int:pk>/delete/', DeleteContactPage.as_view(), name='DeleteContactPage'),

    # admin contact message
    path('admin_ContactMessage/', admin_ContactMessage, name='admin_ContactMessage'),
    path('admin_ContactMessage/<int:pk>/delete/', DeleteContactMessage.as_view(), name='DeleteContact'),
    path('admin_ContactMessage/<int:pk>/edit/', ViewContactMessage.as_view(), name='ViewContact'),

    # admin_Offering  Html
    path('admin_Offering/', admin_Offering, name='admin_Offering'),
    path('admin_Offering/create/', CreateOffering.as_view(), name='CreateOffering'),
    path('admin_Offering/<int:pk>/edit/', UpdateOffering.as_view(), name='UpdateOffering'),
    path('admin_Offering/<int:pk>/delete/', DeleteOffering.as_view(), name='DeleteOffering'),

    # admin Importance  Html
    path('admin_Importance/', admin_Importance, name='admin_Importance'),
    path('admin_Importance/create/', CreateImportance.as_view(), name='CreateImportance'),
    path('admin_Importance/<int:pk>/edit/', UpdateImportance.as_view(), name='UpdateImportance'),
    path('admin_Importance/<int:pk>/delete/', DeleteImportance.as_view(), name='DeleteImportance'),

    # admin Audience  Html
    path('admin_Audience/', admin_Audience, name='admin_Audience'),
    path('admin_Audience/create/', CreateAudience.as_view(), name='CreateAudience'),
    path('admin_Audience/<int:pk>/edit/', UpdateAudience.as_view(), name='UpdateAudience'),
    path('admin_Audience/<int:pk>/delete/', DeleteAudience.as_view(), name='DeleteAudience'),

    # admin Member  Html
    path('admin_Member/', admin_Member, name='admin_Member'),
    path('admin_Member/create/', CreateMember.as_view(), name='CreateMember'),
    path('admin_Member/<int:pk>/edit/', UpdateMember.as_view(), name='UpdateMember'),
    path('admin_Member/<int:pk>/delete/', DeleteMember.as_view(), name='DeleteMember'),

    # admin_Offering  Html
    path('admin_Link/create/', CreateLink.as_view(), name='CreateLink'),
    path('admin_Link/<int:pk>/edit/', UpdateLink.as_view(), name='UpdateLink'),
    path('admin_Link/<int:pk>/delete/', DeleteLink.as_view(), name='DeleteLink'),

    # admin_Offering  Html
    path('admin_View/', admin_View, name='admin_View'),
    path('admin_View/create/', CreateInsView.as_view(), name='CreateView'),
    path('admin_View/<int:pk>/edit/', UpdateInsView.as_view(), name='UpdateView'),
    path('admin_View/<int:pk>/delete/', DeleteInsView.as_view(), name='DeleteView'),

    # admin_Significance  Html
    path('admin_Significance/', admin_Significance, name='admin_Significance'),
    path('admin_Significance/create/', CreateSignificance.as_view(), name='CreateSignificance'),
    path('admin_Significance/<int:pk>/edit/', UpdateSignificance.as_view(), name='UpdateSignificance'),
    path('admin_Significance/<int:pk>/delete/', DeleteSignificance.as_view(), name='DeleteSignificance'),

    # admin_Offering  Html
    path('admin_Funfact/', admin_FunFact, name='admin_Funfact'),
    path('admin_Funfact/create/', CreateFunFact.as_view(), name='CreateFunFact'),
    path('admin_Funfact/<int:pk>/edit/', UpdateFunFact.as_view(), name='UpdateFunFact'),
    path('admin_Funfact/<int:pk>/delete/', DeleteFunFact.as_view(), name='DeleteFunFact'),

    # HOMEPAGE
    path('admin_HomePage/', admin_HomePage, name='admin_HomePage'),
    path('admin_HomePage/create/', CreateHomePage.as_view(), name='CreateHomePage'),
    path('admin_HomePage/<int:pk>/edit/', UpdateHomePage.as_view(), name='UpdateHomePage'),
    path('admin_HomePage/<int:pk>/delete/', DeleteHomePage.as_view(), name='DeleteHomePage'),

    path('admin_Tagline/create/', CreateTagline.as_view(), name='CreateTagline'),
    path('admin_Tagline/<int:pk>/edit/', UpdateTagline.as_view(), name='UpdateTagline'),
    path('admin_Tagline/<int:pk>/delete/', DeleteTagline.as_view(), name='DeleteTagline'),

    # FOOTERS
    path('admin_Footers/', admin_Footers, name='admin_Footers'),
    path('admin_Footers/create/', CreateFooters.as_view(), name='CreateFooters'),
    path('admin_Footers/<int:pk>/edit/', UpdateFooters.as_view(), name='UpdateFooters'),
    path('admin_Footers/<int:pk>/delete/', DeleteFooters.as_view(), name='DeleteFooters'),
    
    # FOOTER SOCIAL MEDIA
    path('admin_SocialMedia/create/', CreatesocialMedia.as_view(), name='CreatesocialMedia'),
    path('admin_SocialMedia/<int:pk>/edit/', UpdatesocialMedia.as_view(), name='UpdatesocialMedia'),
    path('admin_SocialMedia/<int:pk>/delete/', DeletesocialMedia.as_view(), name='DeletesocialMedia'),
    path('admin_SocialMedia/approve/<int:pk>/', views.socialmedia_approval, name='socialmedia_approval'),

    # Performance
    path('admin_Performance/', admin_performance, name='admin_Performance'),
    path('admin_Performance/create/', CreatePerformance.as_view(), name='CreatePerformance'),
    path('admin_Performance/<int:pk>/edit/', UpdatePerformance.as_view(), name='UpdatePerformance'),
    path('admin_Performance/status/<int:pk>/', views.performance_Status, name='performance_Status'),
    path('admin_Performance/<int:pk>/delete/', DeletePerformance.as_view(), name='DeletePerformance'),

    path('Appointment/create/', AppointmentView.as_view(), name='Appointment'),
    path('api/check-date-availability/', views.check_date_availability, name='check_date_availability'),
    # Lesson
    path('admin_Lesson/create/', CreateLesson.as_view(), name='CreateLesson'),
    path('admin_Lesson/<int:pk>/edit/', UpdateLesson.as_view(), name='UpdateLesson'),
    path('admin_Lesson/status/<int:pk>/', views.Lesson_Status, name='Lesson_Status'),
    path('admin_Lesson/<int:pk>/delete/', DeleteLesson.as_view(), name='DeleteLesson'),

    # 3D Model  Html
    path('admin_threeD/', admin_threeD, name='admin_threeD'),
    path('admin_threeD/create/', CreatethreeD.as_view(), name='CreatethreeD'),
    path('admin_threeD/<int:pk>/edit/', UpdatethreeD.as_view(), name='UpdatethreeD'),
    path('admin_threeD/<int:pk>/delete/', DeletethreeD.as_view(), name='DeletethreeD'),

    # 3d Content  Html
    path('admin_3dContent/', admin_3dContent, name='admin_3dContent'),
    path('admin_3dContent/create/', Create3dContent.as_view(), name='Create3dContent'),
    path('admin_3dContent/<int:pk>/edit/', Update3dContent.as_view(), name='Update3dContent'),
    path('admin_3dContent/<int:pk>/delete/', Delete3dContent.as_view(), name='Delete3dContent'),

    
    # Instrument Link  Html
    path('admin_InsLink/', admin_InsLink, name='admin_InsLink'),
    path('admin_InsLink/create/', CreateInsLink.as_view(), name='CreateInsLink'),
    path('admin_InsLink/<int:pk>/edit/', UpdateInsLink.as_view(), name='UpdateInsLink'),
    path('admin_InsLink/<int:pk>/delete/', DeleteInsLink.as_view(), name='DeleteInsLink'),
    path('admin_InsLink/approve/<int:pk>/', views.primary_source_approve, name='primary_source_approve'),


    # FOR CHART
    # path('instrument/<int:pk>/', InstrumentDetailView.as_view(), name='instrument_detail'),
    path('get_chart_data/', get_chart_data, name='get_chart_data'),
    path('get_category_chart_data/', get_category_chart_data, name='get_category_chart_data'),
    path("get_login_chart_data/", get_login_chart_data, name="get_login_chart_data"),

    path('update-performance/<int:pk>/', views.update_performance, name='update_performance'),
    path('update-lesson/<int:pk>/', views.update_lesson, name='update_lesson'),
    # Performance
    path('user_Performance/<int:pk>/edit/', UserUpdatePerformance.as_view(), name='UserUpdatePerformance'),
    path('user_Performance/<int:pk>/delete/', UserDeletePerformance.as_view(), name='UserDeletePerformance'),

    # Lesson
    path('user_Lesson/<int:pk>/edit/', UserUpdateLesson.as_view(), name='UserUpdateLesson'),
    path('user_Lesson/<int:pk>/delete/', UserDeleteLesson.as_view(), name='UserDeleteLesson'),
      # ... other URLs ...
    path('cancel/performance/<int:appointment_id>/', views.cancel_performance, name='cancel_performance'),
    path('cancel/lesson/<int:appointment_id>/', views.cancel_lesson, name='cancel_lesson'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)