# HW_29 Django 

## Установка
Создать виртуальное окружение.
Установить зависимости

```sh
pip install poetry
poetry install
```

Загрузить докер
```sh
docker run --name 29-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

Добавить базу postgres:
User: postgres
Password: postgres

Выполнить миграции.
```sh
./manage.py makemigrations
./manage.py migrate 
```

Загрузить тестовые данные в базу
```sh
python ./manage.py loaddata data/location.json
python ./manage.py loaddata data/categories.json
python ./manage.py loaddata data/user.json
python ./manage.py loaddata data/ads.json


```

Запустить сервер
```sh
./manage.py runserver  
```


### Задание

# Шаг 0

Подключите к проекту DRF, как мы это делали в уроке.

# Шаг 1

Перепишите создание пользователей на GenericView из DRF. И не забудьте сохранить пагинацию в  списке!

# Шаг 2

Напишите ViewSet для модели Location.

```json
Request
GET /location/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"name": "Москва",
				"lat": 52.456734,
				"lng": 49.235543,
			},
			...
		],
	"next": null,
  "previous": null,
	"count": 4,
}

Request
GET /location/1/

Response
200
{
	"id": 1,
	"name": "Москва",
	"lat": 52.456734,
	"lng": 49.235543,
}

404
{
    "detail": "Not found."
}

Request
POST /location/
{
	"name": "Москва, м. Автозаводская",
	"lat": 52.456734,
	"lng": 49.235543,
}

Response
200
{
    "id": 5,
    "name": "Москва, м. Автозаводская",
    "lat": "52.456734",
    "lng": "49.235543"
}

400
{"name":["This field is required."]}

Request
PATCH /location/1/
{
	"name": "Москва, м. Автозаводская",
	"lat": 52.456734,
	"lng": 49.235543,
}

Response
200
{
	"id": 1,
	"name": "Москва, м. Автозаводская"
	"lat": 52.456734,
	"lng": 49.235543,
}

400
{"name":["This field is required."]}

Request
DELETE /location/1/

Response
204
```

# Шаг 3

Теперь можно приступать к поиску. Поиск будет для объявлений и фильтров будет несколько, поэтому давайте разобьем их по шагам.

## Шаг 1

Первое, что всегда встречается в маркетплейсах - умение отдавать объявления по категориям. 

Для этого, реализуйте возможность следующего запроса, который возвращает все объявления в переданных ему категориях (в нашем примере все объявления с category_id=1 или category_id=2):

```json
Request
GET /ad?cat=1/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"name": "Толстовка",
				"author": "Мария",
				"price": 500,
			},
			...
		]
	"total": 20,
	"num_pages": 10
} 
```

## Шаг 2

Следующее, что нам точно надо - это поиск по словам. Причем не просто по слову, а по вхождению слова в название. Для этого у нас есть следующая спецификация: 

```json
Request
GET /ad?text="Толстов"/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"name": "Толстовка",
				"author": "Мария",
				"price": 500,
			},
			{
				"id": 2,
				"name": "Продаю толстовку",
				"author": "Анна",
				"price": 1000,
			},
			...
		]
	"total": 20,
	"num_pages": 10
} 
```

## Шаг 3

Еще у нас достаточно широкая география, так что хотелось бы выбрать из всех объявлений только релевантные нам по месту. Спецификация следующая: 

```json
Request
GET /ad?location=Москва/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"name": "Толстовка",
				"author": "Мария",
				"price": 500,
			},
			...
		]
	"total": 20,
	"num_pages": 10
} 
```

NOTE: название локации возьмите из модели User, привязанной к объявлению и предусмотрите поиск по вхождению подстроки без учета регистра.

## Шаг 4

И еще один фильтр: было бы неплохо задать диапазон цен, в котором мы готовы рассматривать товары. Давайте сделаем это так: 

```json
Request
GET /ad?price_from=100&price_to=1000/

Response
200
{
	"items":
		[
			{
				"id": 1,
				"name": "Толстовка",
				"author": "Мария",
				"price": 500,
			},
			{
				"id": 2,
				"name": "Продаю толстовку",
				"author": "Анна",
				"price": 999,
			},
			...
		]
	"total": 20,
	"num_pages": 10
} 
```

**Критерии выполнения:**

- [ ]  Работа с пользователями реализованая через GenericView из DRF - ListApiView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
- [ ]  При выводе списка пользователей используется встроенная пагинация DRF
- [ ]  API для модели Location реализовано с использованием ViewSet и Router
- [ ]  В проекте используются Serializers
- [ ]  Все фильтры выполнены с использованием lookup's
- [ ]  Типы данных в JSON отдаются корректно
- [ ]  Методы из спецификации работают
- 
