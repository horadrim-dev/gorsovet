from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Sozyv, Deputat, Fraction
from django.core.exceptions import ObjectDoesNotExist

class DeputatyListView(ListView):
    template_name = "deputaty/deputaty.html"
    # model = Organization
    # queryset = Organization.objects.filter(level=1)

    def get_queryset(self):
        sozyv_id = self.request.GET.get("sozyv", None)

        try:
            sozyv = Sozyv.objects.get(pk=sozyv_id)
        except ObjectDoesNotExist:
            sozyv = Sozyv.objects.last()

        if not sozyv:
            return Deputat.objects.all()

        qs = Deputat.objects.filter(sozyvy=sozyv)

        fraction_id = self.request.GET.get("fraction", None)
        qs = qs.filter(fractions=fraction_id)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sozyv_list'] = Sozyv.objects.all().order_by('-order')
        context['fraction_list'] = Fraction.objects.all().order_by('-order')

        sozyv_id = self.request.GET.get("sozyv", None)
        fraction_id = self.request.GET.get("fraction", None)

        try:
            active_sozyv = Sozyv.objects.get(pk=sozyv_id)
        except ObjectDoesNotExist:
            active_sozyv = Sozyv.objects.last()

        try:
            active_fraction = Fraction.objects.get(pk=fraction_id)
        except ObjectDoesNotExist:
            active_fraction = None

        page_title = "{} ({})".format(active_sozyv.name, active_fraction.name) if active_fraction else active_sozyv.name

        context['active_sozyv'] = active_sozyv
        context['active_fraction'] = active_fraction
        context['page_title'] = page_title
        return context


class DeputatDetailView(DetailView):
    template_name = "deputaty/detail.html"
    model = Deputat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['object'].name
        return context