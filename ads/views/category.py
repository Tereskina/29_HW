import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)
        categories = self.object_list.order_by('name')

        response = []
        for cat in categories:
            response.append({
                'id': cat.pk,
                'name': cat.name,
            })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs) -> JsonResponse:
        data = json.loads(request.body)

        cat: Category = Category.objects.create(name=data['name'])

        return JsonResponse({
            'id': cat.pk,
            'name': cat.name,
        },
            safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        cat = self.get_object()

        return JsonResponse(
            {
                'id': cat.pk,
                'name': cat.name,
            },
            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data['name']

        self.object.save()

        return JsonResponse(
            {
                'id': self.object.pk,
                'name': self.object.name
            }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=204)
