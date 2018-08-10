from django.db import models
import bcrypt
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

now = str(datetime.now())
# print(type(now))

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []
        if not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif User.objects.filter(email=form['email']):
             errors.append("Account already exists.")
        if len(form['name']) < 3:
            errors.append("Name must have at least 3 characters.")
        if len(form['username']) < 2:
            errors.append("Username must have at least 3 characters.")
        elif User.objects.filter(username=form['username']):
             errors.append("Username already exists.")
        if not form['hdate']:
            errors.append('Hiring date is required.')
        elif form['hdate'] > now:
            errors.append("Hiring date can't be in the future.")
        if len(form['pass']) < 5:
            errors.append("Password must have at least 5 characters.")
        elif form['pass'] != form['confirmpass']:
            errors.append("Password and confirm password must match.")


        if not errors:
            hash1 = bcrypt.hashpw(form['pass'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=form['name'], username=form['username'], email=form['email'], hdate=form['hdate'], password=hash1)
            return (True, user)
        else:
            return (False, errors)


    def loginValidator(self, form):

        errors = []

        if not form['username']:
            errors.append("Username required.")
        elif not User.objects.filter(username=form['username']):
             errors.append("Please register first")
        elif len(form['pass']) < 5:
            errors.append("Password must have at least 5 characters.")
        else:
            user = User.objects.filter(username=form['username'])
            if not bcrypt.checkpw(form['pass'].encode(), user[0].password.encode()):
                errors.append("Sorry, password does not match our records.")

        if not errors:
            return (True, user[0])
        else:
            return (False, errors)

class ProductValidator(models.Manager):

     def productValidator(self, form, user_id):
        errors = []

        if not form['item']:
            errors.append('Item name is required')
        if len(form['item']) < 4:
            errors.append('Item name needs to be more than 3 characters')
            
        if not errors:
            poster = User.objects.get(id=user_id)
            product = Product.objects.create(item=form['item'], poster=poster)

            poster.wishitems.add(product)

            return (True, product)
        else:
            return (False, errors)



class User(models.Model):
    name = models.CharField(max_length=15)
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=15) 
    hdate = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)  
   

    # joins (connets our Trip model with out User model through our Join table)
    # trips (connects our Trip model with our User model (Trip table)
    def __repr__(self):
        return "<User {} | {} | {} {}>".format(self.id, self.name, self.username, self.email)

    objects = UserManager()

class Product(models.Model):
    item = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    poster = models.ForeignKey(User, related_name="postedproducts")
    wisher = models.ManyToManyField(User, related_name="wishitems")

   
    def __repr__(self):
        return "<Product {} | {} | {} {}>".format(self.id, self.item, self.created_at, self.poster) 
        
    objects = ProductValidator()
