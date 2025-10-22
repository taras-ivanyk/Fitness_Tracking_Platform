from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from activities.models import Profile, Activity
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Демонструє роботу репозиторія (Django ORM) для 3-х сутностей'

    def handle(self, *args, **options):

        # self.stdout.write() - це "красивий" print з кольорами
        self.stdout.write(self.style.SUCCESS(
            "--- ДЕМОНСТРАЦІЯ РОБОТИ РЕПОЗИТОРІЯ (DJANGO ORM) ---"
        ))

        # === 1. Сутність "User" (Користувач) ===
        self.stdout.write(self.style.HTTP_INFO("\n[1/3] Робота з сутністю User..."))
        try:
            # Використовуємо get_or_create, щоб уникнути помилки,
            # якщо користувач вже існує
            user, created = User.objects.get_or_create(
                username="demo_user",
                defaults={'email': 'demo@example.com', 'password': 'password123'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано User: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User '{user.username}' вже існує."))

        except Exception as e:
            raise CommandError(f"Помилка при створенні User: {e}")

        # === 2. Сутність "Profile" (Профіль) ===
        self.stdout.write(self.style.HTTP_INFO("\n[2/3] Робота з сутністю Profile..."))

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'display_name': 'Demo User', 'age': 30, 'city': 'Kyiv'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано Profile для: {profile.user.username}"))
        else:
            self.stdout.write(self.style.WARNING(f"Profile для {profile.user.username} вже існує."))

        # === 3. Сутність "Activity" (Активність) ===
        self.stdout.write(self.style.HTTP_INFO("\n[3/3] Робота з сутністю Activity..."))

        # Запис (Add): Додаємо нову активність
        activity = Activity.objects.create(
            user=user,
            duration_sec=3600,
            distance_m=10500,
            elevation_gain_m=120,
            height=150,
            start_time=timezone.now(),
            end_time=timezone.now()
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано Activity (ID: {activity.id})"))

        # Вичитка всіх даних (Get All)
        self.stdout.write(self.style.HTTP_INFO("\n--- Демонстрація 'get_all' для Activity ---"))
        all_activities = Activity.objects.all().order_by('id')

        for act in all_activities:
            self.stdout.write(f"  ID: {act.id}, Користувач: {act.user.username}, Дистанція: {act.distance_m}м")

        # Пошук по ID (Get By ID)
        self.stdout.write(self.style.HTTP_INFO(f"\n--- Демонстрація 'get_by_id' (шукаємо ID: {activity.id}) ---"))
        try:
            found_act = Activity.objects.get(id=activity.id)
            self.stdout.write(f"  Знайдено: {found_act.user.username} - {found_act.distance_m}м")
        except Activity.DoesNotExist:
            self.stdout.write(self.style.ERROR("Помилка: не вдалося знайти щойно створену активність."))

        self.stdout.write(self.style.SUCCESS("\n--- ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА ---"))