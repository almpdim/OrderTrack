from django.db import models
from django.contrib.auth.models import User
import uuid  # Για αυτόματη παραγωγή μοναδικών Tracking IDs

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    # Σύνδεση 1:1 με τον User του Django για Login/Signup
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Προφίλ: {self.user.username}"

class Order(models.Model):
    # Καταστάσεις Παραγγελίας (Λειτουργία 7)
    PENDING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    
    STATUS_CHOICES = [
        (PENDING, 'Σε Επεξεργασία/Συσκευασία'),
        (SHIPPED, 'Απεστάλη'),
        (DELIVERED, 'Παραδόθηκε'),
    ]

    id = models.AutoField(primary_key=True)
    # Παράγει αυτόματα έναν τυχαίο μοναδικό κωδικό 8 χαρακτήρων για το Tracking (Λειτουργία 9)
    tracking_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)  # Για την ταξινόμηση (Λειτουργία 11)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Σχέση ForeignKey: Ένας χρήστης μπορεί να έχει πολλές παραγγελίες
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.id} - {self.tracking_id} ({self.status})"

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, blank=False)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()  # Τιμή τη στιγμή της αγοράς
    
    # Σύνδεση με την παραγγελία
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"