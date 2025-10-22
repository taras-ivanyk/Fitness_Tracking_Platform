from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime

# --- 1. ІМПОРТУЄМО ВАШУ ЄДИНУ ТОЧКУ ДОСТУПУ ---
from activities.repositories import DataAccessLayer


class Command(BaseCommand):
    help = 'Демонструє роботу ПАТЕРНУ "Репозиторій" та "DataAccessLayer"'

    def handle(self, *args, **options):

        # self.stdout - це "print" для команд Django
        self.stdout.write(self.style.SUCCESS(
            "--- ПОЧАТОК ДЕМОНСТРАЦІЇ РОБОТИ РЕПОЗИТОРІЇВ ---"
        ))

        # --- 2. Створюємо "db" - вашу єдину точку доступу ---
        # Використовуємо 'with' як у вашому старому main.py

        # Додаємо stdout до DataAccessLayer, щоб __exit__ міг друкувати
        db = DataAccessLayer()
        db.stdout = self.stdout
        db.style = self.style

        with db:
            # === 1. Робота з UserRepository ===
            self.stdout.write(self.style.HTTP_INFO("\n--- [1/3] Робота з UserRepository ---"))

            # Унікальний username, щоб уникнути помилок при повторному запуску
            timestamp = int(datetime.now().timestamp())
            username = f"demo_user_{timestamp}"

            try:
                # Використовуємо db.users.add, як у вашому main.py
                user = db.users.add(
                    username=username,
                    email=f"{username}@example.com",
                    password="password123"
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано User: {user.username}"))
            except Exception as e:
                raise CommandError(f"Помилка при створенні User: {e}")

            # === 2. Робота з ProfileRepository ===
            self.stdout.write(self.style.HTTP_INFO("\n--- [2/3] Робота з ProfileRepository ---"))

            # Використовуємо db.profiles.add
            profile = db.profiles.add(
                user=user,
                display_name=f"Demo User {timestamp}",
                age=30,
                city="Kyiv"
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано Profile для: {profile.user.username}"))

            # === 3. Робота з ActivityRepository ===
            self.stdout.write(self.style.HTTP_INFO("\n--- [3/3] Робота з ActivityRepository ---"))

            # Використовуємо db.activities.add
            activity = db.activities.add(
                user=user,
                duration_sec=3600,
                distance_m=10500,
                elevation_gain_m=120,
                height=150,
                start_time=timezone.now(),
                end_time=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Успішно додано Activity (ID: {activity.id})"))

            # Демонстрація 'get_all'
            self.stdout.write(self.style.HTTP_INFO("\n--- Демонстрація 'get_all' для Activity ---"))
            all_activities = db.activities.get_all().order_by('id')

            for act in all_activities:
                self.stdout.write(f"  ID: {act.id}, Користувач: {act.user.username}, Дистанція: {act.distance_m}м")

            # Демонстрація 'get_by_id'
            self.stdout.write(self.style.HTTP_INFO(f"\n--- Демонстрація 'get_by_id' (шукаємо ID: {activity.id}) ---"))
            found_act = db.activities.get_by_id(activity.id)
            self.stdout.write(f"  Знайдено: {found_act.user.username} - {found_act.distance_m}м")

        # __exit__ з DataAccessLayer буде викликано тут
        self.stdout.write(self.style.SUCCESS("\n--- ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА ---"))