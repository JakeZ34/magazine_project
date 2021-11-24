from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'
        
        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Already in use"
        
        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors
    def authenticator(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user=users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    def sign_up(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )


class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class MagazineManager(models.Manager):
    def mag_validator(self, form):
        errors = {}
        if len(form['title']) < 1:
            errors['title'] = "All Magazines have a Title."
        if len(form['description']) < 5:
            errors['description'] = "Tell us more about the Magazine in order to update or create."
        return errors

class Magazine(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_magazines", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_magazines")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = MagazineManager()

