from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse

from .forms import RegistrationForm


class RegistrationView(View, TemplateView):

    template_name = 'registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegistrationForm()

        return context

    def post(self, *args, **kwargs):
        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/login/')
