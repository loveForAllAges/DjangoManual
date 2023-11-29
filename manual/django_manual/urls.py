from django.urls import path, include
from .views import *


views_urlpatterns = [
    path('View', CustomView.as_view(), name='class-view'),
    path('TemplateView', CustomTemplateView.as_view(), name='class-template-view'),
    path('RedirectView', CustomRedirectView.as_view(), name='class-redirect-view'),
    path('DetailView/<int:pk>', CustomDetailView.as_view(), name='class-detail-view'),
    path('ListView', CustomListView.as_view(), name='class-list-view'),
    path('FormView', CustomFormView.as_view(), name='class-form-view'),
    path('CreateView', CustomCreateView.as_view(), name='class-create-view'),
    path('UpdateView/<int:pk>', CustomUpdateView.as_view(), name='class-update-view'),
    path('DeleteView/<int:pk>', CustomDeleteView.as_view(), name='class-delete-view'),
    path('ArchiveIndexView', CustomArchiveIndexView.as_view(), name='class-archive-index-view'),
    path('YearArchiveView/<int:year>', CustomYearArchiveView.as_view(), name='class-year-archive-view'),
    path('MonthArchiveView/<int:year>/<int:month>', CustomMonthArchiveView.as_view(), name='class-month-archive-view'),
    path('WeekArchiveView/<int:year>/week/<int:week>', CustomWeekArchiveView.as_view(), name='class-week-archive-view'),
    path('CustomTodayArchiveView/<int:year>/<str:month>/<int:day>', CustomDayArchiveView.as_view(), name='class-day-archive-view'),
    path('TodayArchiveView/today', CustomTodayArchiveView.as_view(), name='class-today-archive-view'),
    path('DateDetailView/<int:year>/<str:month>/<int:day>/<int:pk>', CustomDateDetailView.as_view(), name='class-date-archive-view'),
]


urlpatterns = [
    path('', upload_file),
    path('2', FileFieldFormView.as_view()),
    path('views/', include(views_urlpatterns)),
]
