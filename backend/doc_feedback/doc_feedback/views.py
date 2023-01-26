from django.shortcuts import render

def main_page_view(request):
    """
    Returns the main page.
    """
    return render(request, 'main_page.html')

def status_view(request):
    """
    Returns the status page.
    """
    return render(request, 'status.html')
