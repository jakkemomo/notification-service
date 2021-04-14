from django.shortcuts import render
from django.views.generic.edit import FormView


class SendView(FormView):
    template_name = 'send_mail.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SendView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.process_action(self.request.POST)
        return super().form_valid(form)


def success_send(request):
    return render(request, template_name='success_send.html')