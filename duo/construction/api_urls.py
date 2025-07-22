from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvanceViewSet, ProjectListView, ProjectDetailAPIView, OfferViewSet, MaterialViewSet, MaterialTypeViewSet, UnitViewSet, WorkerViewSet

router = DefaultRouter()
router.register(r'advances', AdvanceViewSet, basename='advances')
router.register('offers', OfferViewSet, basename='offer')
router.register(r'materials', MaterialViewSet, basename='materials')
router.register(r'material-types', MaterialTypeViewSet, basename='material-types')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'projects', ProjectListView, basename='projects')
router.register(r'workers', WorkerViewSet, basename='workers')


urlpatterns = [
    path('project/<int:pk>', ProjectDetailAPIView.as_view(), name='project'),
]

urlpatterns += router.urls
