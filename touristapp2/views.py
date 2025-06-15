from django.shortcuts import render,HttpResponse
from .forms import *
from .import views
from .models import *
from django.shortcuts import render

from .models import Resort
#from recommendation.models import Resort
from .models import Feedbackmodel  # adjust import if needed

def index(request):
    # Feedback form (POST)
    if request.method == 'POST' and 'message' in request.POST:
        feedback = Feedbackmodel(fb=request.POST['message'])
        feedback.save()

    # Resort filtering (GET)
    resort_type = request.GET.get('resort_type')
    resorts = Resort.objects.all()
    if resort_type:
        resorts = resorts.filter(resort_type=resort_type)  # use your actual field name

    # JS-compatible resort data
    recommended_resorts = [
        {
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude
        }
        for r in resorts
    ]

    return render(request, 'index.html', {
        "resorts": resorts,
        "recommended_resorts": recommended_resorts,
    })

def about(request):
    return render(request,'about.html')
def service(request):
    return render(request,'service.html')
def package(request):
    return render(request,'package.html')
def booking(request):
    if request.method=='POST':
        details=Bookingform(request.POST)
        if details.is_valid():
            if details.cleaned_data.get('have_you_availed_membership')=='Yes':
                recs=Membershipmodel.objects.all()
                for rec in recs:
                    if rec.name==details.cleaned_data.get('name') and rec.email==details.cleaned_data.get('email'):
                        post=details.save()
                        return HttpResponse('Booked successfully')
                    else:
                        details._errors['have_you_availed_membership']=details.error_class(['You are not a member'])
                        return render(request,'booking.html',{'form':details})
            else:
                request.session['form_data2'] = details.cleaned_data
                

            rooms=Roomsmodel.objects.all()
            for room in rooms:
                if room.name==details.cleaned_data.get('destination'):
                    if details.cleaned_data.get('type_of_room')=='S' and room.studio==0:
                        details._errors['type_of_room']=details.error_class(['Booking studiofull'])
                        return render(request,'booking.html',{'form':details})
                    elif details.cleaned_data.get('type_of_room')=='1' and room.onebed==0:
                        details._errors['type_of_room']=details.error_class(['Booking onebedfull'])
                        return render(request,'booking.html',{'form':details})
                    elif details.cleaned_data.get('type_of_room')=='2' and room.twobed==0:
                        details._errors['type_of_room']=details.error_class(['Booking twobedfull'])
                        return render(request,'booking.html',{'form':details})
                    else:
                        request.session['form_data2'] = details.cleaned_data
                        return render(request,'payment2.html')        
        else:
            return render(request,'booking.html',{'form':details})
    else:
        form=Bookingform(None)
        return render(request,'booking.html',{'form':form})

def bookingpaid(request):
    details=request.session.get('form_data2')
    details1=Bookingform(details)
    post=details1.save()
    rooms=Roomsmodel.objects.all()
    for room in rooms:
        if room.name==details1.cleaned_data.get('destination'):
            if details1.cleaned_data.get('type_of_room')=='S':
                room.studio-=1
                room.save()
            elif details1.cleaned_data.get('type_of_room')=='1':
                room.onebed-=1
                room.save()
            elif details.cleaned_data.get('type_of_room')=='2':
                room.twobed-=1
                room.save()
    return HttpResponse("Booking confirmed")
def error(request):
    return render(request,'error.html')
def northindia(request):
    return render(request,'northindia.html')
def southindia(request):
    return render(request,'southindia.html')
def international(request):
    return render(request,'international.html')
def asia(request):
    return render(request,'asia.html')
def europe(request):
    return render(request,'europe.html')
def india(request):
    return render(request,'india.html')

def membership(request):
    if request.method=='POST':
        details=Membershipform(request.POST)
        if not details.is_valid():
            return render(request,'membership.html',{'form':details})
        else:
            request.session['form_data'] = details.cleaned_data
            return render(request,'payment.html')
    else:
        form=Membershipform(None)
        return render(request,'membership.html',{'form':form})
def membershippaid(request):
    details=request.session.get('form_data')
    details1=Membershipform(details)
    post=details1.save(commit=False)
    post.save()
    return HttpResponse("data submitted")
    
def testimonial(request):
    return render(request,'testimonial.html')
def contact(request):
    return render(request,'contact.html')

# Create your views here...
from django.shortcuts import render
from .utils.recommend import get_recommendations, get_all_resorts

def resort_recommendation_view(request):
    # Get filter parameters from GET (for filtering resorts)
    region = request.GET.get('region')
    rating = request.GET.get('rating')

    # Get all resorts (assuming a list of resort objects or dicts)
    all_resorts = get_all_resorts()

    # Filter resorts by region and rating if filters are provided
    if region:
        all_resorts = [r for r in all_resorts if getattr(r, 'region', None) == region]
    if rating:
        all_resorts = [r for r in all_resorts if getattr(r, 'rating', 0) >= float(rating)]

    recommendations = []
    selected_resort = None

    # If POST, get selected resort and fetch recommendations
    if request.method == "POST":
        selected_resort = request.POST.get("resort_name")
        recommendations = get_recommendations(selected_resort)

    context = {
        "resorts": all_resorts,             # filtered list for dropdown or display
        "selected_resort": selected_resort,
        "recommendations": recommendations,
        "regions": ['North India', 'South India', 'International'],  # adjust as needed
        "ratings": [5, 4, 3, 2, 1],
    }

    return render(request, "touristapp2/recommend.html", context)


