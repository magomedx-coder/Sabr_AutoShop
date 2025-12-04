from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
	class Role(models.TextChoices):
		BUYER = 'buyer', 'Покупатель'
		MANAGER = 'manager', 'менеджер'
		ADMIN = 'admin', 'Администратор'


	
	user = models.OneToOneField(
		get_user_model(),
		on_delete=models.CASCADE,
		related_name='profile'
	)
	role = models.CharField(
		max_length=20,
		choices=Role.choices,
		default=Role.BUYER
	)

	class Meta:
		verbose_name = 'Профиль пользователя'
		verbose_name_plural = 'Профили пользователей'



	def __str__(self):
		return f"{self.user} ({self.get_role_display()})"
	

RoleChoices = UserProfile.Role
