from django.shortcuts import render


def loginpage(request):
    return render(request, 'accounts/loginpage.html')
