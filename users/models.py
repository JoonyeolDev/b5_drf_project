from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    password = models.CharField("비밀번호", max_length=256)
    username = models.CharField("이름", max_length=100, unique=True)
    gender = models.CharField("성별", max_length=1, choices=GENDERS)
    date_of_birth = models.DateField("생년월일", null=True)
    introduction = models.TextField("자기소개", null=True, blank=True)
    image = models.ImageField("프로필 이미지", blank=True, upload_to="%Y/%m/")
    preference = models.CharField("선호 음료", max_length=256, null=True, blank=True)
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin