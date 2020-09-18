from django.db import models
from django.contrib.auth.models import PermissionsMixin,UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomUserManager(UserManager):
    #マネージャーをマイグレーションにシリアライズして、RunPythonの中で使えるようにする

    use_in_migrations = True

    #usernameフィールドを無くし、emailフィールドをメインに扱うモデルを作成する
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        #送信されてきたメールアドレスを正規化している（例: foobar@gmail.com と FOOBAR@gmail.comを同じ者としてみなす
        email = self.normalize_email(email)
        user  = self.model(email=email,**extra_fields) #email属性をもつインスタンス変数を作成
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        #デフォルトで以下2つの属性をFalseで設定している
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # デフォルトで以下2つの属性をTrueで設定している
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError('Super user must has is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(_("email_address"),unique=True)
    username = models.CharField(_("username"),max_length=30,blank=True)
    profile_image = models.ImageField(upload_to="profile_image",blank=True,null=True)
    introduction = models.TextField(max_length=255,blank=True,null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=(
            "管理者だけ管理者サイトにログインできます"
        )
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=(
            "Activeとして扱われます"
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email" #ここでusernameとして扱われるところがemail属性に置き換わった
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _('users') #管理者サイト用

    def no_of_product(self):
        return self.product_set.count()

    def no_of_order(self):
        return self.order_set.count()

    def no_of_sold(self):
        sold_product = self.product_set.filter(is_sold=True)
        return sold_product.count()


class Category(models.Model):
    name = models.CharField(max_length=20)
    objects = models.Manager()


class Product(models.Model):
    title = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(max_length=500,blank=False,null=False)
    product_image = models.ImageField(upload_to="product_image",blank=True,null=True)
    provider = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.title

    def provider_name(self):
        return self.provider.username

    def category_name(self):
        return self.category.name


class Order(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def buyer_name(self):
        return self.buyer.username

    def product_name(self):
        return self.product.name


