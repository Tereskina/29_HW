import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from ads.models import Ad, Category
from HW_29.settings import TOTAL_ON_PAGE
from users.models import User


def index(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        items_list = [
            {'id': ad.pk,
             'name': ad.name,
             'author': ad.author.username,
             'price': ad.price,
             'descriptions': ad.description,
             'is_published': ad.is_published,
             'category': ad.category.name,
             'image': ad.image.url if ad.image else None} for ad in obj]

        response = {
            "items": items_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name']

    def post(self, request, *args, **kwargs) -> JsonResponse:
        data = json.loads(request.body)
        author = get_object_or_404(User, username=data['author'])
        category = get_object_or_404(Category, name=data['category'])

        ad: Ad = Ad.objects.create(name=data['name'],
                                   author=author,
                                   category=category,
                                   price=data['price'],
                                   description=data['description'],
                                   is_published=data['is_published']
                                   )
        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'category': ad.category.name,
            'is_published': ad.is_published
        }, safe=False)


class AdDetailView(DetailView):
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs) -> JsonResponse:
        ad = self.get_object()

        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'author': ad.author.username,
            'category': ad.category.name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None
        },
            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name']

    def patch(self, request, *args, **kwargs):

        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'name' in data:
            self.object.name = data['name']
        if 'price' in data:
            self.object.price = data['price']
        if 'description' in data:
            self.object.description = data['description']
        if 'is_published' in data:
            self.object.is_published = data['is_published']
        self.object.save()

        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'category': self.object.category.name,
            'is_published': self.object.is_published
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs) -> JsonResponse:
        self.object = self.get_object()

        # self.object.image = request.FILES.get('image')
        self.object.image = request.FILES.get('image')
        self.object.save()

        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'category': self.object.category.name,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None
        })
