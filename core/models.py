from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Both', 'Both'),
)
CATEGORY_CHOICE = (
    ('Cosmetics', 'Cosmetics'),
    ('Accessories', 'Accessories'),
    ('Clothes', 'Clothes')
)
SIZE = (
    ('XXS', 'XXS'),
    ('XS', 'XS'),
    ('XS-S', 'XS-S'),
    ('S', 'S'),
    ('M-L', 'M-L'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)
COLORS = (
    ('black', 'black'),
    ('red', 'red'),
    ('grey', 'grey'),
)
CLOTHE_OPTIONS = (
    ('Jacket', 'Jacket'),
    ('Coat', 'Coat'),
    ('Dresse', 'Dresse'),
    ('Shirt', 'Shirt'),
    ('T-shirt', 'T-shirt'),
    ('Jean', 'Jean')
)
ACCESSORIE_OPTIONS = (
    ('Scarf', 'Scarf'),
    ('Hat', 'Hat'),
    ('Glove', 'Glove'),
    ('Glasse', 'Glasse'),
    ('Jewelry', 'Jewelry'),
    ('Bag', 'Bag')
)
COSMETIC_OPTIONS = (
    ('Perfume', 'Perfume'),
    ('Depilatory', 'Depilatory'),
    ('Cream', 'Cream'),
    ('Soap', 'Soap'),
    ('Face Powder', 'Face Powder')
    )


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self): 
        return f'this is {self.user.username} with id:{self.id}'







class Product(models.Model):
    name = models.CharField(max_length=220)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER)
    for_kid = models.CharField(max_length=255, default='No', choices=(('Yes', 'Yes'), ('No', 'No')))
    quantity = models.IntegerField(default=0)
    featured = models.BooleanField(null=True, blank=True, default=False)
    description = models.TextField(null=True, blank=True)
    specification = models.TextField(null=True, blank=True)
    thumnail = models.ImageField(upload_to='upload/products')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True)
    related_product = models.ManyToManyField("self", default=None, blank=True)
    class Meta:
        abstract = True
        ordering = ['-created_at']

    @property
    def get_absolute_url(self):
        return reverse('core:Product-Details', kwargs={'klass':type(self).__name__, 'pk':self.pk})

    @property
    def get_add_url(self):
        return reverse('core:Adding-Cart', kwargs={'klass':type(self).__name__, 'pk':self.pk})


    @property
    def product_label(self):
        """_ Quand le produit est nouveau, il peut avoir reduction.
           _ Qaund le produit dure plus de 3 jour, il est ancien.
        """
        if not self.quantity:
            return '<div class="label stockout">out of stock</div>'

        delta_days = ( now() - self.created_at ).days
        if (delta_days < 3 and self.sale_price) or (delta_days < 3):
            return '<div class="label new">New</div>'
        elif self.sale_price:
            return '<div class="label sale">Sale</div>'
        return ''

    def real_price(self):
        if self.sale_price:
            return self.sale_price
        return self.price
    @property
    def product_price(self): 
        if self.sale_price:
            return f'<div class="product__price">$ {self.sale_price}.0\
            <span>$ {self.price}.0</span></div>'
        return f'<div class="product__price">$ {self.price}.0 </div>'
        

    def all_products(*args, **kwargs):
 
        objects = [kls.objects.all() for kls in args]
        new_list = []
        for queryset in objects:
            new_list.extend(queryset)
        try:
            if kwargs['featured'] or kwargs['is_new']: 
                return [item for item in new_list if item.featured or\
                        (now() - item.created_at).days < 3]
        except:
            return new_list

    @property
    def related(self):
        return self.related_product.all()

    @property
    def switch(self):
        # Bon, un peu de bidouille, ça factorise enormement mon code et le filtre marche à merveille
        # ce code ajoute des classes à une div pour faire le filtre dans index.html:HomePage
        cat = self.category.name if self.category.name != 'Cosmetics' else 'cosmetic'
        kid = 'kid' if self.for_kid == 'Yes' else ''
        array = [('Men', 'Male'), ('Women', 'Female'), ('Women Men', 'Both')]
        try:
            attribute = [' '.join([x[0], cat, kid])  for x in array if x[1]==self.gender][0]
        except IndexError:
            attribute = ''
        return attribute
       

class Quantity(models.Model):
    ''' Ici, nos templates sont justes configurer pour 3 couleurs:black, red,
    grey'''
    black_quantity = models.IntegerField(default=0)
    red_quantity = models.IntegerField(default=0)
    grey_quantity = models.IntegerField(default=0)
    class Meta:
        abstract = True
    
    @property 
    def available_color(self):
        black = 'black' if self.black_quantity else None
        red = 'red' if self.red_quantity else None
        grey = 'grey' if self.grey_quantity else None
        return [black, red, grey]

    
class ClotheProduct(Product, Quantity):
    size = models.CharField(max_length=255, choices=SIZE, null=True, blank=True)
    product_options = models.CharField(max_length=255, choices=CLOTHE_OPTIONS)
    class Meta:
        verbose_name = 'Clothes Product'

    @property
    def quantity(self):
        quantity =  sum([self.red_quantity, self.grey_quantity, self.black_quantity])
        return quantity

    def __str__(self):
        return f'{self.id}-->{self.name}'

    def filter_card(self):
        return ""


class Image(models.Model):
    product = models.ForeignKey(ClotheProduct, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='upload/products')
    
    def __str__(self):
        return f'{self.id}-->{self.name}'


class CosmeticProduct(Product, Quantity):
    product_options = models.CharField(max_length=255, choices=COSMETIC_OPTIONS)
    class Meta:
        verbose_name = 'Cosmetic Product'

    def __str__(self):
        return f'CosProduct:{self.id}-->{self.name}'


class AccessorieProduct(Product, Quantity):
    product_options = models.CharField(max_length=255, choices=ACCESSORIE_OPTIONS)
    class Meta:
        verbose_name = 'Accessorie Product'

    @property
    def quantity(self):
        quantity =  sum([self.red_quantity, self.grey_quantity, self.black_quantity])
        return quantity

    def __str__(self):
        return f'{self.id} --> {self.name}'

    def filter_card(self):
        return ""


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, choices=CATEGORY_CHOICE)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'category:{self.id}-->{self.name}'

    @classmethod
    def get_quantiy(self):
        return self.product_set().count()



class OrderProduct(models.Model):
    """
        I cannot link this class with Product because 
        of diversity of category Product.
    """
    category = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    product_id = models.IntegerField(null=True)
    color = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)
    session_order = models.CharField(max_length=50, null=True)#for session or users who don't have account
    size = models.CharField(max_length=50, null=True)
    price = models.IntegerField(null=True)

    def __str__(self): 
        return f'prduct:{self.category}'
    
class Order(models.Model):
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, blank=True, null=True )
    complete = models.BooleanField(default=False)
    quantity= models.IntegerField(default=0)

class BillingInfo(models.Model):
    order = models.OneToOneField("Order", on_delete=models.CASCADE, null=True, blank=True)
    session_order = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    appartement = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    account_password = models.CharField(max_length=50)
    notes = models.TextField()
    create_account = models.BooleanField(default=False)

    def billingProducts(self, customer=None):
        if customer:
            products = self.order.order_product_set()
            return products
        return [x for x in OrderProduct.objects.filter(session_order=self.session_order)]


    





    