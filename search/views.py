from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from . import forms


class SearchView(generic.TemplateView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            form = forms.SearchForm(self.request.GET)
        else:
            form = forms.SearchForm()
        context["form"] = form
        return context

    def get(self, request, *args, **kwargs):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            return redirect(reverse('search:flights') + request.get_full_path()[1:])
        return super().get(request, *args, **kwargs)


class ResultsView(generic.TemplateView):
    form_class = forms.SearchForm
    template_name = 'search/flights.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.SearchForm(self.request.GET)
        return context


class ResultsAjaxView(generic.TemplateView):
    template_name = 'search/results.html'
