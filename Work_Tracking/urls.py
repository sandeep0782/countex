from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from track.views import *

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('custom_report.urls')),
  path('', Home, name='home'),
  path('admin_home', Admin_Home, name='admin_home'),
  path('user_home', User_Home, name='user_home'),
  path('gmt_home', GMT_Home, name='gmt_home'),
  path('supplier_home', Supplier_Home, name='supplier_home'),
  path('Pending_Del', Pending_Del, name='pendel'),
  path('pendelad', Pending_Del_Admin, name='pendelad'),
  path('pend_app_buyer', Pending_app_buyer, name='pend_app_buyer'),

  path('about', About, name='about'),
  path('contact', Contact, name='contact'),
  path('login', Login_User, name='login'),
  path('admin_login', Login_admin, name='admin_login'),
  path('signup', Signup_User, name='signup'),
  path('logout/', Logout, name='logout'),
  path('add_buyer', Register_Buyer, name='add_buyer'),
  path('add_rm', Register_RM, name='add_rm'),
  path('add_supplier', Register_Supplier, name='add_supplier'),
  
  
  path('latest_greige', latest_greige, name='latest_greige'),
  path('latest_print', latest_printed, name='latest_print'),
  path('latest_dispatch', latest_dispatch, name='latest_dispatch'),
  path('latest_checking', latest_checking, name='latest_checking'),
  
  path('pending_greige', pending_greige, name='pending_greige'),
  path('pending_print', pending_printed, name='pending_print'),
  path('pending_dispatch', pending_dispatch, name='pending_dispatch'),
  path('pending_checking', pending_checking, name='pending_checking'),
  
  
  path('sampling_status', sampling_status, name='sampling_status'),
  
  
  path('supplier_summary', supplier_summary, name='supplier_summary'),
  path('buyer_summary', buyer_summary, name='buyer_summary'),
  path('multiple_set_delivery_date', multiple_set_delivery_date, name='multiple_set_delivery_date'),
  path('Update_multiple_Sample_supplier', Update_multiple_Sample_supplier, name='Update_multiple_Sample_supplier'),
  
  path('Running_Sampling_Supplier', Running_Sampling_Supplier, name='Running_Sampling_Supplier'),
  path('running_supplier_bulk_order', Running_Supplier_Bulk_Order, name='running_supplier_bulk_order'),
  
  path('add_sampling', Add_Sampling, name='add_sampling'),
  path('dispatch_dash_admin/<int:season>/<int:buyer>/', dispatch_dash_admin, name='dispatch_dash_admin'),
  path('packed_dash_admin/<int:season>/<int:buyer>/', packed_dash_admin, name='packed_dash_admin'),
  path('under_prodn_dash_admin/<int:season>/<int:buyer>/', under_prodn_dash_admin, name='under_prodn_dash_admin'),
  path('Ontime_dash_admin/<int:season>/<int:buyer>/', Ontime_dash_admin, name='Ontime_dash_admin'),
  path('total_qty_dash_admin/<int:season>/<int:buyer>/', total_qty_dash_admin, name='total_qty_dash_admin'),
  path('Delay_dash_admin/<int:season>/<int:buyer>/', Delay_dash_admin, name='Delay_dash_admin'),
  path('update_sampling/<int:id>', Update_Sampling, name='update_sampling'),
  path('update_sampling_admin/<int:id>', Update_Sampling_Admin, name='update_sampling_admin'),
  
  path('approved_sample_dash_admin/<int:season>/<int:buyer>/', approved_sample_dash_admin, name='approved_sample_dash_admin'),
  path('under_dev_sample_dash_admin/<int:season>/<int:buyer>/', under_dev_sample_dash_admin, name='under_dev_sample_dash_admin'),
  path('under_app_sample_dash_admin/<int:season>/<int:buyer>/', under_app_sample_dash_admin, name='under_app_sample_dash_admin'),
  path('drop_sample_dash_admin/<int:season>/<int:buyer>/', drop_sample_dash_admin, name='drop_sample_dash_admin'),
  path('all_sample_dash_admin/', all_sample_dash_admin, name='all_sample_dash_admin'),
  path('under_redo_sample_dash_admin/<int:season>/<int:buyer>/', under_redo_sample_dash_admin, name='under_redo_sample_dash_admin'),
  
  path('add_season', Add_Season, name='add_season'),
  path('add_drop', Add_Drop, name='add_drop'),
  path('sampling_accuracy', Sampling_accuracy, name='sampling_accuracy'),
  
  path('add_item', Add_Product, name='add_item'),
  path('view_item', View_Product, name='view_item'),
  path('update_product<int:id>', Update_Product, name='update_product'),
  
  path('view_buyer', View_Buyer, name='view_buyer'),
  path('view_supplier', View_Supplier, name='view_supplier'),
  path('view_season', View_Season, name='view_season'),
  path('view_drop', View_Drop, name='view_drop'),
  path('view_rm', View_RM, name='view_rm'),
  
  
  path('view_sampling', All_Sampling, name='view_sampling'),
  path('all_sampling', All_Sampling, name='all_sampling'),
  path('Create_Order_Manually', Create_Order_Manually, name='Create_Order_Manually'),
  path('update_order_manually<int:pid>', update_order_manually, name='update_order_manually'),
  
  path('view_vendor', View_Vendor, name='view_vendor'),
  path('add_sampling_buyer', Add_Sampling_Buyer, name='add_sampling_buyer'),
  path('Sampling_Supplier', Sampling_Supplier, name='sample_supplier'),
  path('sample_buyer', Sampling_Buyer, name='sample_buyer'),
  path('sampling_history', History_Sampling, name='sampling_history'),
  path('view_bulk_admin', View_Bulk_Admin, name='view_bulk_admin'),
  path('gmt_bulk_order', GMT_Bulk_Order, name='gmt_bulk_order'),
  path('current_gmt_bulk_order', Current_GMT_Bulk_Order, name='current_gmt_bulk_order'),
  path('update_disptch_admin<int:id>', Update_Disptch_Admin, name='update_disptch_admin'),
  
  path('view_courier_latest', View_Courier_latest, name='view_courier_latest'),
  path('view_courier_update', View_Courier_update, name='view_courier_update'),
  path('view_pending_bulk', View_Pending_Bulk, name='view_pending_bulk'),
  path('supplier_bulk_order', Supplier_Bulk_Order, name='supplier_bulk_order'),
  path('under_develope_sample_supplier', under_develope_sample_supplier,name='under_develope_sample_supplier'),
  path('under_develop_bulk_supplier', under_develop_bulk_supplier, name='under_develop_bulk_supplier'),
  path('buyer_bulk_order', Buyer_Bulk_Order, name='buyer_bulk_order'),
  path('under_develop_bulk_buyer', under_develop_bulk_buyer, name='under_develop_bulk_buyer'),
  path('under_develope_sample_buyer', under_develope_sample_buyer, name='under_develope_sample_buyer'),
  path('bulk_end_report', View_End_Bulk_Admin, name='bulk_end_report'),
  path('bulk_start_report', View_Start_Bulk_Admin, name='bulk_start_report'),
  path('view_sampling_ontime', View_Sampling_ontime, name='view_sampling_ontime'),
  path('view_sampling_Approved', View_Sampling_Approved, name='view_sampling_Approved'),
  path('view_sampling_underdevel', View_Sampling_Underdevel, name='view_sampling_underdevel'),
  path('view_sampling_underapproval', View_Sampling_Underapp, name='view_sampling_underapproval'),
  path('view_sampling_underedevelopment', View_Sampling_Redevelopment, name='view_sampling_underedevelopment'),
  path('view_sampling_uncomplete', View_Sampling_uncomplete, name='view_sampling_uncomplete'),
  path('view_sampling_before', View_Sampling_before, name='view_sampling_before'),
  path('edit_buyer<int:pid>', Update_Buyer, name='edit_buyer'),
  path('Update_Permission<int:pid>', Update_Permission, name='Update_Permission'),
  
  
  
  path('edit_rm<int:pid>', Update_RM, name='edit_rm'),
  path('edit_supplier<int:pid>', Update_Supplier, name='edit_supplier'),
  path('delete_buyer<int:pid>', delete_buyer, name='delete_buyer'),
  path('delete_rm<int:pid>', delete_rm, name='delete_rm'),
  path('delete_supplier<int:pid>', delete_supplier, name='delete_supplier'),
  path('delete_season<int:pid>', delete_season, name='delete_season'),
  path('delete_drop<int:pid>', delete_drop, name='delete_drop'),
  path('delete_bulk<int:pid>', delete_bulk, name='delete_bulk'),
  path('delete_item<int:pid>', delete_item, name='delete_item'),
  path('delete_sampling<int:pid>', delete_sampling, name='delete_sampling'),
  path('update_sample<int:pid>', Update_Sample_supplier, name='update_sample'),
  path('view_comment<int:pid>', Sampling_Comment, name='view_comment'),
  path('sent_update<int:pid>', Sent_Update_Buyer, name='sent_update'),
  path('history1<int:pid>', History1, name='history1'),
  path('view_comment_admin<int:pid>', View_Comment_Admin, name='view_comment_admin'),
  path('update_bulk_admin<int:pid>', Update_Bulk_Admin, name='update_bulk_admin'),
  path('update_bulk_order<int:pid>', Update_Bulk_Order, name='update_bulk_order'),
  path('admin_bulk_status<int:pid>', admin_bulk_status, name='admin_bulk_status'),
  path('sup_bulk_status<int:pid>', Supplier_Bulk_Status, name='sup_bulk_status'),
  path('update_griege<int:pid>', Update_Griege, name='update_griege'),
  path('update_griege_admin<int:pid>', Update_Griege_Admin, name='update_griege_admin'),
  
  path('update_print<int:pid>', Update_Printed, name='update_print'),
  path('update_print_admin<int:pid>', Update_Printed_Admin, name='update_print_admin'),
  path('update_firstofbulk_admin<int:pid>', Update_FirstOfBulk_Admin, name='update_firstofbulk_admin'),
  path('update_fpt_status_admin<int:pid>', Update_FPT_Status_Admin, name='update_fpt_status_admin'),
  path('Update_Fabric_Cheking_Admin<int:pid>', Update_Fabric_Cheking_Admin, name='Update_Fabric_Cheking_Admin'),
  path('Update_Dispatch_Detail_Admin<int:pid>', Update_Dispatch_Detail_Admin, name='Update_Dispatch_Detail_Admin'),
  path('update_payment_status_admin<int:pid>', Update_Payment_Status_Admin, name='update_payment_status_admin'),
  
  path('buyer_bulk_status<int:pid>', Buyer_Bulk_Status, name='buyer_bulk_status'),
  path('update_first_bulk<int:pid>', Update_FirstOfBulk, name='update_first_bulk'),
  path('update_fpt_status<int:pid>', Update_FPT_Status, name='update_fpt_status'),
  path('update_fabric_checking<int:pid>', Update_Fabric_Cheking, name='update_fabric_checking'),
  path('update_dispatch_detail<int:pid>', Update_Dispatch_Detail, name='update_dispatch_detail'),
  path('update_payment_status<int:pid>', Update_Payment_Status, name='update_payment_status'),
  path('assign_status<int:pid>', Assign_Status, name='assign_status'),
  path('assign2_status<int:pid>', Assign_Status2, name='assign2_status'),
  path('delete_vendor<int:pid>', delete_vendor, name='delete_vendor'),
  path('brand_with_sample<int:pid>', View_brand_Sampling, name='brand_with_sample'),
  path('season_with_sample<int:pid>', View_Season_Sampling, name='season_with_sample'),
  path('supplier_with_sample<int:pid>', View_Supplier_Sampling, name='supplier_with_sample'),
  path('copy_of_bulk<int:pid>', Copies_Of_Bulk, name='copy_of_bulk'),
  path('set_delivery_date<int:pid>', set_delivery_date, name='set_delivery_date'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
