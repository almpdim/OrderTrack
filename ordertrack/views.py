from django.shortcuts import render
from .models import Order

def order_list_view(request):
    # 1. Αρχική ανάκτηση όλων των παραγγελιών
    orders = Order.objects.prefetch_related('items').all()
    
    # 2. Διαχείριση Φιλτραρίσματος (Λειτουργία 10)
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        status_mapping = {
            'pending': 'Processing',
            'shipped': 'Shipped',
            'delivered': 'Delivered',
        }
        django_status = status_mapping.get(status_filter)
        if django_status:
            orders = orders.filter(status=django_status)
            
    # 3. Διαχείριση Ταξινόμησης (Λειτουργία 11)
    sort_by = request.GET.get('sort', 'desc') # Αν δεν επιλεγεί κάτι, προεπιλογή είναι η φθίνουσα (desc)
    if sort_by == 'asc':
        orders = orders.order_by('created_at')  # Από την παλαιότερη στην πιο πρόσφατη
    else:
        orders = orders.order_by('-created_at') # Από την πιο πρόσφατη στην παλαιότερη (το μείον σημαίνει φθίνουσα)

    # 4. Αποστολή όλων των μεταβλητών στο template
    context = {
        'orders': orders,
        'current_filter': status_filter,
        'current_sort': sort_by
    }
    return render(request, 'order_list.html', context)


def track_order_view(request):
    order = None
    error_message = None
    
    # Αν ο χρήστης πάτησε "Αναζήτηση" (Υποβολή της φόρμας)
    if request.method == 'GET' and 'tracking_id' in request.GET:
        tracking_id = request.GET.get('tracking_id').strip()
        
        if tracking_id:
            try:
                # Αναζήτηση της παραγγελίας στη βάση με βάση το tracking_id
                order = Order.objects.get(tracking_id=tracking_id)
            except Order.DoesNotExist:
                # Αν δεν βρεθεί, εμφανίζουμε μήνυμα σφάλματος
                error_message = f"Δεν βρέθηκε παραγγελία με τον κωδικό: {tracking_id}"
        else:
            error_message = "Παρακαλώ εισάγετε έναν έγκυρο κωδικό tracking."

    context = {
        'order': order,
        'error_message': error_message
    }
    return render(request, 'track.html', context)