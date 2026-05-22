from django.shortcuts import render, redirect

def result_portal(request):
    return render(request, 'results/result_portal.html')

def board_results(request):
    return render(request, 'results/board_results.html')

def competitive_results(request):
    return render(request, 'results/competitive_results.html')

def redirect_to_result(request, link_id):
    # For now, redirect to home
    return redirect('home')