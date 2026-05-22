from django.shortcuts import render

def test_list(request):
    return render(request, 'exams/test_list.html')

def take_test(request, test_id):
    return render(request, 'exams/take_test.html', {'test_id': test_id})

def test_result(request, test_id):
    return render(request, 'exams/test_result.html', {'test_id': test_id})