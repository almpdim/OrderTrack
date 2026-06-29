from django.contrib import admin
# Εισάγουμε τα μοντέλα που έφτιαξες στην Ενότητα 4
from .models import UserProfile, Order, OrderItem

# Τα κάνουμε register για να εμφανιστούν στο Admin Panel
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)