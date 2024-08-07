#this file contains the logic for a user to login with their email or password

from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import *
from django.http import HttpRequest

UserModel = get_user_model()

class EmailPhoneNumberBackend(ModelBackend):

     def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        
        try:
            print(type(username))


            if "@" in username:
                user = CustomUser.objects.get(
                    Q(email=username)
                )
            else:
                print(f"this is a number")

                user = CustomUser.objects.get(
                    Q(phone_number=username)
                )
                print(user)
                
        except UserModel.DoesNotExist:
            
            raise ValidationError(
                {"error":"user credentials does not exist"}
            )
            #return "Invalid user credentials"
        
        except Exception as e:
            raise ValidationError(
                {"error":"user credentials does not exist"}
            )

        if user.check_password(password):
            return user