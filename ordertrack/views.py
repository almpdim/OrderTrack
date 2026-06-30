from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from .models import Order
from .forms import OrderItemForm

@login_required(login_url='login') # Αν κάποιος δεν είναι συνδεδεμένος, τον πετάει στο Login
def order_list_view(request):
    # Παίρνουμε ΜΟΝΟ τις παραγγελίες που ανήκουν στον συγκεκριμένο συνδεδεμένο χρήστη
    orders = Order.objects.filter(user=request.user) 
    
    return render(request, 'order_list.html', {'orders': orders})
            
    # 3. Διαχείριση Ταξινόμησης (Λειτουργία 11)
    sort_by = request.GET.get('sort', 'desc') # Αν δεν επιλεγεί κάτι, προεπιλογή είναι η φθίνουσα 
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


def order_detail_view(request, order_id):
    # Αν δεν βρει την παραγγελία με αυτό το ID, θα βγάλει αυτόματα σελίδα 404 (Not Found)
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order
    }
    return render(request, 'order_detail.html', context)

def login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Έλεγχος αν ο χρήστης υπάρχει στη βάση και αν ο κωδικός είναι σωστός
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            login(request, user) # Σύνδεση του χρήστη
            return redirect('order_list') # Ανακατεύθυνση στη λίστα παραγγελιών
        else:
            # Αν τα στοιχεία είναι λάθος, επιστρέφει μήνυμα σφάλματος
            return render(request, 'login.html', {'error_message': 'Λάθος όνομα χρήστη ή κωδικός πρόσβασης.'})
            
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        password_confirm_input = request.POST.get('password_confirm')

        # 1. Έλεγχος αν οι κωδικοί ταιριάζουν
        if password_input != password_confirm_input:
            return render(request, 'signup.html', {'error_message': 'Οι κωδικοί πρόσβασης δεν ταιριάζουν.'})

        # 2. Έλεγχος αν το username υπάρχει ήδη
        if User.objects.filter(username=username_input).exists():
            return render(request, 'signup.html', {'error_message': 'Το όνομα χρήστη χρησιμοποιείται ήδη.'})

        # 3. Δημιουργία του χρήστη και αυτόματη σύνδεση
        user = User.objects.create_user(username=username_input, email=email_input, password=password_input)
        login(request, user)

        return redirect('order_list') # Ανακατεύθυνση στο ιστορικό παραγγελιών

    return render(request, 'signup.html')

def profile_view(request):
    return render(request, 'profile.html') 

@login_required(login_url='login')
def order_form_view(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST) # Δεσμευμένη φόρμα με τα δεδομένα του χρήστη
        if form.is_valid(): # Αυτόματος έλεγχος επικύρωσης του Django 
            # 1. Δημιουργούμε πρώτα την κενή παραγγελία και τη συνδέουμε με τον τρέχοντα χρήστη
            new_order = Order.objects.create(user=request.user)
            
            # 2. Παίρνουμε το αντικείμενο του προϊόντος χωρίς να το σώσουμε ακόμα στη βάση
            item = form.save(commit=False)
            
            # 3. Συνδέουμε το προϊόν με την παραγγελία που μόλις φτιάξαμε
            item.order = new_order
            
            # 4. Σώζουμε οριστικά στη βάση δεδομένων 
            item.save()
            
            return redirect('order_list') # Επιστροφή στο ιστορικό παραγγελιών
    else:
        form = OrderItemForm() # Κενή φόρμα για την αρχική εμφάνιση
        
    return render(request, 'order_form.html', {'form': form}) 

def order_cancel_view(request):
    return render(request, 'order_cancel.html')

def order_status_update_view(request):
    return render(request, 'order_status_update.html')

def order_list_filtered_view(request):
    return render(request, 'order_list_filtered.html')

def order_list_sorted_view(request):
    return render(request, 'order_list_sorted.html')