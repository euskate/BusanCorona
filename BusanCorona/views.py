from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render

class HomeView(TemplateView):

    template_name = 'index.html'
    
def menu1(request):
    template = './busan_div.html'
    context = {'template':template}
    return render(request, 'menu1.html', context=context)

def menu2(request):
    template = './busan_Total.html'
    context = {'template':template}
    return render(request, 'menu2.html', context=context)

def menu3(request):
    template = './busan.html'
    context = {'template':template}
    return render(request, 'menu3.html',context=context)

def menu4(request):
    template = './contactUs.html'
    context = {'template':template}
    return render(request, 'menu4.html',context=context)