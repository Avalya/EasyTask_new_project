# СЭД Проект (Django + Flutter)

## 📚 Описание
Это простая система электронного документооборота (СЭД), состоящая из:
- 🤖 Django REST API (backend)
- 📱 Flutter UI (frontend)

Система позволяет подать заявку, отслеживать статус, прикреплять файлы и управлять заявками через админку.

---

## ♻ Функциональность

### 📁 Бэкенд (Django REST Framework)
| № | Функция | URL |
|----|----------------------|-------------------------------|
| 1  | Подать заявку     | POST `/api/applications/`       |
| 2  | Список заявок     | GET `/api/applications/`        |
| 3  | Одна заявка     | GET/PATCH `/api/applications/<id>/` |
| 4  | Статус заявки     | GET `/api/applications/status/<uuid>/` |
| 5  | Файлы           | `/media/uploads/...`            |
| 6  | JWT-логин         | POST `/api/token/`              |

### 📱 Фронтенд (Flutter)
| № | Экран | Описание |
|----|----------|-------------------------------|
| 1  | Главная       | Список заявок              |
| 2  | Поиск         | Фильтр заявок               |
| 3  | Форма         | Подача заявки               |
| 4  | Статус       | Проверка по UUID            |
| 5  | Логин         | Вход для админа         |
| 6  | Админпанель   | Статус, комментарий, файл |

---

## 🚀 Запуск (backend)
```bash
cd django_final
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 👍 Авторы
- Имя: [твоё имя]
- Универ: [тут можно добавить]# EasyTask_new_project
# EasyTask_
# EasyTask_
