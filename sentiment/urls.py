from django.urls import path, include
from . import views
from .views import (
    fileListView,
    fileDetailView,
    fileCreateView,
    fileDeleteView,
    UserFileListView,
    PocessingDetail,
    fileoverallListView,
    fileoverallDeleteView,
    fileoverallDetailView,
    individualListView,
    filenameListView,
    individualDeleteView,
    indListView
)

urlpatterns = [
    path('',fileListView.as_view(),name='home'),
    path('about/',views.about,name='about'),
    path('fileupload/',fileCreateView.as_view(),name='fileupload'),
    path('filelist/user/<str:username>',UserFileListView.as_view(),name='user-fileupload'),
    path('file/<int:pk>/delete/',fileDeleteView.as_view(),name='file-delete'),
    path('search/',PocessingDetail.as_view(),name='search'),
    path('email/',views.mail,name="mail"),
    
    path('filehome/',fileoverallListView.as_view(),name='filehome'),
    path('overallfile/<int:pk>/delete/',fileoverallDeleteView.as_view(),name='overallfile-delete'),
    path('overallfile/<int:pk>/',fileoverallDetailView.as_view(),name='overallfile-detail'),

    path('individualhome/',individualListView.as_view(),name='individualhome'),
    path('rating/file/<str:filename>',filenameListView.as_view(),name='filename'),
    path('individual/<int:pk>/delete/',individualDeleteView.as_view(),name='individual-delete'),
    path('piechart/',views.piechart,name='piechart'),
    path('piechart1/',views.piechart1,name='piechart1'),
    path('piechart2/',views.piechart2,name='piechart2'),
    path('product_pie/<str:product_name>/',views.avg_piedetail,name='product_pie'),

    path('ov_detail/<int:ov_id>/',views.piedetail,name='ov-detail'),
    path('ind_detail/<int:ind_id>/',views.pieinddetail,name='ind-detail'),
    path('ind_detail1/<int:ind_id>/',views.pieinddetail1,name='ind-detail1'),
    path('indhome1/',indListView.as_view(),name='indhome'),

    path('filename/<str:filename>/',views.filedetail,name='filedetail'),
    path('productname/<str:product_name>/',views.productdetail,name='product-detail'),


    path('email/',views.mail,name="mail"),
    path('email/<int:id>/',views.mailid,name="mailid"),
    path('product_mail/<str:product_name>/',views.product_mail,name="product-mail"),
]