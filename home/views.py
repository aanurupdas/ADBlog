from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
  allPosts = Post.objects.all()
  context = {'allPosts': allPosts}
  return render(request,'home/home.html',context)
  
def about(request):
  return render(request,'home/about.html')

def contact(request):   
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content'] 
        if len(name)<2 or len(phone)<10 or len(email)<3 or len(content)<4:
            messages.error(request,'Fill form correctly')
        else:
            contact = Contact(name=name, phone=phone,email=email, content=content)
            contact.save()
            messages.success(request,'Your message has been sent!')
    return render(request,'home/contact.html')

def search(request):
  query = request.GET['query']
  if len(query)>80:
	  allPosts = Post.objects.none()
  else:
	  allPostsTitle = Post.objects.filter(title__icontains=query)
	  allPostsContent = Post.objects.filter(content__icontains=query)
	  allPosts = allPostsTitle.union(allPostsContent)		  		 
  param = {'allPosts': allPosts,'query': query}
  return render(request,'home/search.html',param)   

def handleSignup(request):
  if request.method == 'POST':
    #Get the post paramaters
	  username = request.POST['username']
	  fname = request.POST['fname']
	  lname = request.POST['lname']
	  email = request.POST['email']
	  pass1 = request.POST['pass1']
	  pass2 = request.POST['pass2']

	  #Check for errorneous input
	  if len(username)>10:
		  messages.error(request,"Username must be under 10 characters")
		  return redirect('home')
		  
	  if not username.isalnum():
	    messages.error(request,"Username must have letters and numbers ")
	    return redirect('home')
		
	  if pass1!=pass2:
	    messages.error(request,"Passwords dont match ")
	    return redirect('home')

    #User create
	  myuser=User.objects.create_user(username,email,pass1)
	  myuser.first_name=fname
	  myuser.last_name=lname
	  myuser.save()
	  messages.success(request,"User account created successfully ")
	  return redirect('home')

  else:
    return HttpResponse("404") 
	 
def handleLogin(request):
	if request.method=='POST':
	  #Get the post paramaters
	  loginname=request.POST['loginname']
	  loginpass=request.POST['loginpass']
	  user=authenticate(username=loginname,password=loginpass)
	  if user is not None:
	    login(request,user)
	    messages.success(request,"Successfully login ")
	    return redirect('home')
	  else:
	    messages.error(request,"Invalid credentials")
	    return redirect('home')
	return HttpResponse("404")  
	  
def handleLogout(request): 
  logout(request)
  messages.success(request,"Successfully logout")
  return redirect('home')
 
