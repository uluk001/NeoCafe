from celery import shared_task
from decimal import Decimal
from apps.accounts.models import CustomUser

@shared_task
def update_user_bonus_points(user_id, total_price, spent_bonus_points):
    """
    Updates user bonus points.
    """
    user = CustomUser.objects.get(id=user_id)
    new_bonus_points = Decimal(total_price) * Decimal('0.05')
    user.bonus += new_bonus_points - spent_bonus_points
    user.save()
