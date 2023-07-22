import uuid
import logging
import random
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, email, name, otp, usertype):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number,
            email=email,
            OTP=otp,
            name=name,
            usertype=usertype,
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_customer(self, phone_number, password, appSignature=None, email=None, name=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        otp = random.randrange(10**5, 10**6)

        user = self.create_user(
            phone_number,
            password=password,
            email=email,
            isCustomer=True,
            name=name,
            otp=otp,
            usertype='',
        )
        user.save(using=self._db)
        return user
    
    def create_manager(self, phone_number, appSignature=None, email=None, name=None, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        otp = random.randrange(10**5, 10**6)

        user = self.create_user(
            phone_number,
            password=password,
            email=email,
            name=name,
            otp=otp,
            usertype='manager',
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, email=None, name=None):
        """
        Creates and saves a superuser with the given Phone Number, Name, Email and password.
        """

        user = self.create_user(
            phone_number,
            password=password,
            email=email,
            name=name,
            otp="00000",
            usertype='superadmin'
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)

        logger.info("Super User %s is Created", phone_number)

        return user



class User(AbstractBaseUser):

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number    = models.CharField(max_length=17, unique=True)
    email           = models.EmailField(verbose_name='email address', max_length=255, null=True, blank=True, help_text="Optional. For Receipt")
    name            = models.CharField(blank=False, null= True, max_length=255)

    usertype        = models.CharField(max_length=256, default='none', choices=[('none', 'None'), ('superadmin', 'Super Admin'), ('admin', 'Admin'), ('manager', 'Manager'),])
    isCustomer      = models.BooleanField(default=False)
    
    is_deleted      = models.BooleanField(default=False)
    deleted_date    = models.DateTimeField(null=True, blank=True, help_text="")

    # Other Info
    OTP             = models.PositiveIntegerField(null=True, blank=True)
    appversion      = models.CharField(max_length=100, null=True, blank=True, help_text="To Keep Track of app users")
    status          = models.CharField( default='active', choices=[('deleted', 'Deleted'), ('active', 'Active'), ('suspended', 'Suspended')], max_length=100, blank=False)

    # Default fields
    staff           = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    active          = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    admin           = models.BooleanField(default=False)
    isVerified      = models.BooleanField(default=False)

    # timestamps
    created_date       = models.DateTimeField(auto_now_add=True)
    modified_date      = models.DateTimeField(auto_now=True)
    # notice the absence of a "Password field", that's built in.

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = [ 'email', 'name' ] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.phone_number

    def get_short_name(self):
        # The user is identified by their email address
        return self.phone_number

    def __str__(self):              # __unicode__ on Python 2
        return self.phone_number


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_staff(self):
        "Is the user a admin member?"
        return self.staff

    @property
    def is_active(self):
        "Is the user active?"
        return self.active