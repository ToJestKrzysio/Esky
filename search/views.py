from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms


class SearchView(generic.TemplateView):
    template_name = 'search/search.html'
    success_url = reverse_lazy('search:results')

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
            return redirect('search:results')
        return super().get(request, *args, **kwargs)


class ResultsView(generic.FormView):
    form_class = forms.SearchForm
    template_name = 'search/results.html'
    success_url = reverse_lazy('search:results')
