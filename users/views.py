import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from HW_29.settings import TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('username')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        response = {}

        items_list = [
            {'id': user.pk,
             'username': user.username,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'role': user.role,
             'age': user.age,
             'location': list(map(str, user.location.all())),
             'total_ads': user.ads.filter(is_published=True).count()
             } for user in obj
        ]
        response['items'] = items_list
        response['total'] = self.object_list.count()
        response['num_pages'] = paginator.num_pages

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        user = self.get_object()

        return JsonResponse(
            {
                'id': user.pk,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'location': list(map(str, user.location.all())),
                'total_ads': user.ads.filter(is_published=True).count()
            }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.age = user_data["age"]

        for location_name in user_data["location"]:
            loc, _ = Location.objects.get_or_create(name=location_name)
            self.object.location.add(loc)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(map(str, self.object.location.all())),
            'total_ads': self.object.ads.filter(is_published=True).count()
        }, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse(
            {'status': 'ok. user delete successfully'}, status=204
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', "password", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data['username'],
            password=user_data["password"],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            role=user_data['role']
        )

        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            user.location.add(location)

        return JsonResponse({
            'id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location': list(map(str, user.location.all())),
            'total_ads': user.ads.filter(is_published=True).count()
        }, safe=False)

