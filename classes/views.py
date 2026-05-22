from django.shortcuts import render

def class_list(request):
    return render(request, 'classes/class_list.html')

def class_detail(request, class_number):
    return render(request, 'classes/class_detail.html', {'class_number': class_number})

def subject_detail(request, class_number, subject_slug):
    return render(request, 'classes/subject_detail.html', {
        'class_number': class_number,
        'subject_slug': subject_slug
    })
# Create your views here.
