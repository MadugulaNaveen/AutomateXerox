from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from datetime import datetime as dt
from .utilities import count_pdf_pages,order_cost
from xerox_machine.settings import PAYMENT_GATEWAY_API_KEY,PAYMENT_GATEWAY_API_SECRET
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .models import Document, UserDocument, Order

print("\nIn views baby\n")
    
cost_per_page = 1
# Create your views here.
def load(request):
    return render(request,'login.html')
  
  
  
def register(request):
  if (request.method == 'POST'):
    name = request.POST['name']
    user_name = request.POST['user_name']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    ph_no = request.POST['ph_no']
    email = request.POST['email']
    if(password1 == password2):
      if(User.objects.filter(username=user_name).exists()):
        messages.info(request,'Username Already Taken')
        return render(request,'login.html')
      else:
        user = User.objects.create_user(username=user_name,password=password1)
        user.save()
        print("User Created")
        messages.info(request,"Account Created,Log in Now")
        return render(request,'login.html')
    else:
      messages.info(request,'passwords doesnot match')
      return render(request,'login.html')
  else:
    return render(request, 'login.html')
  
def login(request):
  if(request.method == 'POST'):
    user_name = request.POST['user_name']
    password = request.POST['password']
    user = auth.authenticate(username = user_name,password = password)
    if user is not None:
      auth.login(request,user)
      if request.user.is_superuser:
        return render(request,'super_index.html')
      else:
        return render(request,'user_index.html')
    else:
      messages.info(request,'invalid credentials')
      return redirect('/login')
  else:
    return render(request,'login.html')




def xerox_details(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        documents = []
        user = request.user 
        now = dt.now()

        # Format the date and time
        date_string = now.strftime('%Y%m%d')
        time_string = now.strftime('%H%M%S')

        total_pages = 0
        # Generate the order ID using the user name, date, and time
        order_id = f'{user.username}_{date_string}_{time_string}'
        order = Order(order_id=order_id,cost =32, user = user)
        order.paid = False
        order.save()
        print(files)
        for file in files:
          document = Document(name=file.name, file=file,user=user,order= order,copies=1)
          document.save()
        
        documents = Document.objects.filter(user=order.user,order= order)
            
        return render(request, 'files.html', {'files': documents,'order':order,'display':'hide','show':'show'})
    else:
        return HttpResponse("Please submit the form with files.")




from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required

# @login_required
def calculate(request,order_id):
  if request.method == 'POST' and request.user.is_authenticated:
    user = request.user 
    order = get_object_or_404(Order, id=order_id)
    documents = Document.objects.filter(user=order.user,order= order)
    
    pdf_names = request.POST.getlist('pdf_name')
    print_links = request.POST.getlist('preview_link')
    types = request.POST.getlist('type')
    copies = request.POST.getlist('copies')
    charges = 0
    for i in range(len(pdf_names)):
      try:
        file_obj = Document.objects.get(name=pdf_names[i],order=order)
        file_obj.xerox_type = types[i]
        file_obj.copies= copies[i]
        file_obj.save()
        pages = count_pdf_pages(file_obj.file.path)
        charges +=order_cost(pages,types[i],copies[i])
        user_document = UserDocument(user=user,document=file_obj,order=order)
        user_document.save()
      except Document.DoesNotExist:
        print("errored")
        messages.error(request, f"File '{pdf_names[i]}' does not exist.")
    order.cost = charges
    order.save()
    client = razorpay.Client(auth=(PAYMENT_GATEWAY_API_KEY, PAYMENT_GATEWAY_API_SECRET))
    charges *=100
    data = { "amount": charges, "currency": "INR", "receipt": order.order_id }
    payment = client.order.create(data=data)
    return render(request,'files.html',{'price':order.cost,'files':documents,'payment':payment,'order':order,'display':'show','show':'hide','action':'action-none'})
  else:
    return render(request,'login.html')


import json 
@csrf_exempt
def payment_verification(request,order_id):
  if(request.method == 'POST'):
    newOrder = get_object_or_404(Order, id=order_id)
    newOrder.paid = True
    newOrder.save()
    
    documents = Document.objects.filter(user=newOrder.user,order= newOrder)
    names = [document.name for document in documents]
    urls =[document.file.url for document in documents]
    details={
      'id':newOrder.order_id,
      'username':newOrder.user.username,
      'cost':newOrder.cost,
      'documentNames':names,
      'documentUrls':urls,
    }
    print(details)
    # Convert the list to JSON
    orders_json = json.dumps(details)
    return render(request,'success.html',{'orders': orders_json})
  



# Super User page editing

# Updating the cost of each page.
def update(request):
  return render(request,'super_index.html')


# Orders page
def orders(request):
    orders = Order.objects.filter(paid = True)
    for order in orders:
      order.documents = Document.objects.filter(user=order.user,order= order)
      
    return render(request, 'super_orders.html', {'orders': orders})
  
# Deleting the completed Orders
def delete_row(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    user_documents = UserDocument.objects.filter(user=order.user,order=order)
    # Delete the associated documents
    documents = Document.objects.filter(user=order.user,order= order)
    for document in documents:
        document.file.delete()
        document.delete()

    for user_document in user_documents:
        user_document.delete()
    order.delete()
    return redirect('orders')
  
  
  
  
  
  
  
  


  