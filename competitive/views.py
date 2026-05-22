from django.shortcuts import render

def exam_list(request):
    return render(request, 'competitive/exam_list.html')

def exam_detail(request, exam_slug):
    return render(request, 'competitive/exam_detail.html', {'exam_slug': exam_slug})

def exam_syllabus(request, exam_slug):
    return render(request, 'competitive/exam_syllabus.html', {'exam_slug': exam_slug})

def previous_papers(request, exam_slug):
    return render(request, 'competitive/previous_papers.html', {'exam_slug': exam_slug})