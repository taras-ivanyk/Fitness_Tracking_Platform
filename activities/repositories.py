from typing import List, Optional
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import (
    Activity,
    Profile,
    Comment,
    Kudos,
    Follower,
    ActivityPoint,
    UserMonthlyStats
)


# --- 1. Базовий інтерфейс (як у вашому repository_interface.py) ---
class BaseRepository:
    """
    Базовий клас-інтерфейс, що визначає загальні методи.
    """

    def get_by_id(self, model_id: int):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def add(self, model):
        raise NotImplementedError


# --- 2. Реалізація репозиторіїв для кожної моделі ---

class UserRepository(BaseRepository):
    """
    Репозиторій для моделі User.
    Використовує вбудовану модель User від Django.
    """

    def get_by_id(self, model_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=model_id)
        except User.DoesNotExist:
            return None

    def get_all(self) -> List[User]:
        return User.objects.all()

    def add(self, **kwargs) -> User:
        """Створює нового користувача. kwargs: username, email, password"""
        return User.objects.create_user(**kwargs)


class ProfileRepository(BaseRepository):
    """Репозиторій для моделі Profile."""

    def get_by_id(self, model_id: int) -> Optional[Profile]:
        try:
            return Profile.objects.get(id=model_id)
        except Profile.DoesNotExist:
            return None

    def get_all(self) -> List[Profile]:
        return Profile.objects.all()

    def add(self, **kwargs) -> Profile:
        """Створює новий профіль. kwargs: user, display_name, ..."""
        return Profile.objects.create(**kwargs)


class ActivityRepository(BaseRepository):
    """Репозиторій для моделі Activity."""

    def get_by_id(self, model_id: int) -> Optional[Activity]:
        try:
            return Activity.objects.get(id=model_id)
        except Activity.DoesNotExist:
            return None

    def get_all(self) -> List[Activity]:
        return Activity.objects.all()

    def add(self, **kwargs) -> Activity:
        """Створює нову активність. kwargs: user, duration_sec, ..."""
        return Activity.objects.create(**kwargs)


class CommentRepository(BaseRepository):
    """Репозиторій для моделі Comment."""

    def get_by_id(self, model_id: int) -> Optional[Comment]:
        try:
            return Comment.objects.get(id=model_id)
        except Comment.DoesNotExist:
            return None

    def get_all(self) -> List[Comment]:
        return Comment.objects.all()

    def add(self, **kwargs) -> Comment:
        """Створює новий коментар. kwargs: activity, user, body, ..."""
        return Comment.objects.create(**kwargs)


class KudosRepository(BaseRepository):
    """Репозиторій для моделі Kudos."""

    def get_by_id(self, model_id: int) -> Optional[Kudos]:
        try:
            return Kudos.objects.get(id=model_id)
        except Kudos.DoesNotExist:
            return None

    def get_all(self) -> List[Kudos]:
        return Kudos.objects.all()

    def add(self, **kwargs) -> Kudos:
        """Створює нові kudos. kwargs: activity, user"""
        try:
            return Kudos.objects.create(**kwargs)
        except IntegrityError:  # Якщо юзер вже лайкнув
            return None


class ActivityPointRepository(BaseRepository):
    """Репозиторій для моделі ActivityPoint."""

    def get_by_id(self, model_id: int) -> Optional[ActivityPoint]:
        try:
            return ActivityPoint.objects.get(id=model_id)
        except ActivityPoint.DoesNotExist:
            return None

    def get_all(self) -> List[ActivityPoint]:
        return ActivityPoint.objects.all()

    def add(self, **kwargs) -> ActivityPoint:
        """Створює нову точку. kwargs: activity, lat, lon, ..."""
        return ActivityPoint.objects.create(**kwargs)


class FollowerRepository(BaseRepository):
    """Репозиторій для моделі Follower (має композитний ключ)."""

    def get_by_id(self, model_id: int):
        raise NotImplementedError("Follower не має єдиного ID, використовуйте get_by_composite_id")

    def get_by_composite_id(self, follower: User, followee: User) -> Optional[Follower]:
        try:
            return Follower.objects.get(follower=follower, followee=followee)
        except Follower.DoesNotExist:
            return None

    def get_all(self) -> List[Follower]:
        return Follower.objects.all()

    def add(self, **kwargs) -> Follower:
        """Створює підписку. kwargs: follower, followee"""
        try:
            return Follower.objects.create(**kwargs)
        except IntegrityError:  # Якщо вже підписаний
            return None


class UserMonthlyStatsRepository(BaseRepository):
    """Репозиторій для моделі UserMonthlyStats (має композитний ключ)."""

    def get_by_id(self, model_id: int):
        raise NotImplementedError("UserMonthlyStats не має єдиного ID, використовуйте get_by_composite_id")

    def get_by_composite_id(self, user: User, year: int, month: int) -> Optional[UserMonthlyStats]:
        try:
            return UserMonthlyStats.objects.get(user=user, year=year, month=month)
        except UserMonthlyStats.DoesNotExist:
            return None

    def get_all(self) -> List[UserMonthlyStats]:
        return UserMonthlyStats.objects.all()

    def add(self, **kwargs) -> UserMonthlyStats:
        """Створює статистику. kwargs: user, year, month, ..."""
        return UserMonthlyStats.objects.create(**kwargs)


# --- 3. ЄДИНА ТОЧКА ДОСТУПУ (DataAccessLayer) ---

class DataAccessLayer:
    """
    Єдина точка доступу до всіх репозиторіїв.
    Це імітує ваш старий клас DataAccessLayer.
    """

    def __init__(self):
        # Ми не приймаємо 'connection', бо Django керує цим.
        # Ми просто створюємо екземпляри наших репозиторіїв.
        self.users = UserRepository()
        self.profiles = ProfileRepository()
        self.activities = ActivityRepository()
        self.activity_points = ActivityPointRepository()
        self.comments = CommentRepository()
        self.followers = FollowerRepository()
        self.kudos = KudosRepository()
        self.user_stats = UserMonthlyStatsRepository()

    def __enter__(self):
        # Цей метод потрібен для 'with DataAccessLayer() as db:'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # У Django нам не потрібно закривати з'єднання вручну.
        # Просто виводимо повідомлення.
        self.stdout.write(self.style.WARNING("\nDataAccessLayer: Роботу завершено."))