from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig

from .views import (
    CategoryProductsView,
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductModerationListView,
    ProductPublishView,
    ProductUnpublishView,
    ProductUpdateView,
)

app_name = CatalogConfig.name

urlpatterns = [
    # Основные страницы
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    # CRUD для продуктов
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', cache_page(60 * 2)(ProductDetailView.as_view()), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    # Модерация продуктов (НОВЫЕ URL)
    path('products/<int:pk>/publish/', ProductPublishView.as_view(), name='product_publish'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('moderation/', ProductModerationListView.as_view(), name='product_moderation'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
