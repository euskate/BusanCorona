from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render

class HomeView(TemplateView):

    template_name = 'index.html'
    
def test(request):
    return render(request, 'busan_div.html')