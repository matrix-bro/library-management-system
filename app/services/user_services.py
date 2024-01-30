from django.contrib.auth import get_user_model
User = get_user_model()

def create_user_account(name, email, membership_date, password):
    user = User.objects.create_user(name=name, email=email, membership_date=membership_date, password=password)

    return user
    