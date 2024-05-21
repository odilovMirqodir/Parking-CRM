from django.views.generic import TemplateView
from .models import Parking


class IndexPageView(TemplateView):
    model = Parking
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parking_id = self.request.GET.get('parking_id')

        if parking_id:
            try:
                parking = Parking.objects.get(id=parking_id)
                context['parking_status'] = parking.is_active
            except Parking.DoesNotExist:
                context['parking_status'] = None
        else:
            context['parking_status'] = None

        return context
