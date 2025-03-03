from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from .forms import UserCreateForm

class RegisterView(CreateView):
    template_name = "pages/page-register.html"
    form_class = UserCreateForm
    # success_url = reverse_lazy("login")  # Redirect after successful registration

    def form_valid(self, form):
        form.save()  # Save the user
        return super().form_valid(form)
