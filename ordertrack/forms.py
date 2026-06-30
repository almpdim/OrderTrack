from django import forms
from .models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        # Τα πεδία που θέλουμε να συμπληρώνει ο χρήστης στη φόρμα
        fields = ['product_name', 'quantity', 'price']
        
        # Τα labels στα ελληνικά 
        labels = {
            'product_name': 'Όνομα Προϊόντος',
            'quantity': 'Ποσότητα',
            'price': 'Τιμή (€)',
        }
    # Αυτό το κομμάτι βάζει αυτόματα το στυλ του Bootstrap σε όλα τα πεδία!
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})