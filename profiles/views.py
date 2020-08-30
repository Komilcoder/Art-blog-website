from django.shortcuts import render, redirect , get_object_or_404
from .models import Profile,Relationship,RelationshipManager
from .forms import ProfileModelForm, CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

@login_required(login_url='/accounts/login/')
def my_profile_view(request):
       
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None,instance=profile)
    confirm= False  
    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm
    }

    
    return render(request, 'profiles/myprofile.html',context)


def invites_received(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatiotion_recieved(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs':results,
        'is_empty':is_empty,
    }    

       
    return render(request,'profiles/my_invites.html', context)



def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profile(user)
    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)


# it is invite friends
def invite_profile_list(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_invites(user)

    context = {'qs':qs}
    return render(request, 'profiles/invite_list.html', context)

def Loginpage(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, login)
        return redirect('home')
    else:
        return render(request,'registration/login.html') 



def logout_view(request):
    logout(request)
    return redirect('home')



def Registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    else:    
        form = CreateUserForm()    
        context = {'form':form}
        return render(request, 'registration/signup.html', context)        


# for seeing profile on browser 
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        qs = Profile.objects.get_all_profile(self.request.user)
        return qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_rec = Relationship.objects.filter(sender=profile)
        rel_sen = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_rec:
            rel_receiver.append(item.receiver.user)
        for item in rel_sen:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender']  = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] == True     
        return context 


# this is for sending freindship each other
def send_invatiation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relat = Relationship.objects.create(sender=sender, receiver=receiver,status='send')  
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile')      

# this is deleting freindship 
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.filter((Q(sender=sender) & Q(receiver=receiver)) |(Q(sender=receiver) & Q(receiver=sender)))  
        rel.delete() 
        return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect('profiles:my_profile')      


def accept_invatition(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sende=sender, receiver=receiver)
        if rel.status =='sender':
            rel.status == 'accepted'
            rel.save()
    return redirect('profiles:my_invite')        




def reject_invatition(request):
    if request.method == 'POST':
        pk= request.POST.get('profile+_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my_invite')    