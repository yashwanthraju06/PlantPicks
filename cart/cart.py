from store.models import Product,Profile
import datetime
class Cart():
    def __init__(self,request):
        self.session=request.session
        #Get request
        self.request=request

        cart=self.session.get('session_key')

        if 'session_key' not in request.session:
            cart=self.session['session_key']={}

        self.cart=cart 
    def db_add(self,product,quantity):
        product_id=str(product)
        product_qty=str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)

        self.session.modified=True 
        #Deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            current_user=Profile.objects.filter(user__id=self.request.user.id) 
            #{'3':1,'2':4} to{"3":1}  
            carty=str(self.cart)  
            carty=carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))

    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)

        self.session.modified=True 
        #Deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile 
            current_user=Profile.objects.filter(user__id=self.request.user.id) 
            #{'3':1,'2':4} to{"3":1}  
            carty=str(self.cart)  
            carty=carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))
    def cart_total(self):
       #get product ids
       product_ids=self.cart.keys()
       #lookup those keys in our Product database model
       products=Product.objects.filter(id__in=product_ids)
       #Get quantities
       quantities=self.cart
       total=0
       for key,value in quantities.items():
           #convert key string into int so we can do math
           key=int(key)
           for product in products:
               if product.id==key:
                   if product.is_sale:
                       total=total+(product.sale_price*value)
                   else:
                       total=total+(product.price*value)
       return total   

       
          
    def __len__(self):
        return len(self.cart)
    def get_prods(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)

        return products
    def get_quants(self):
        quantities=self.cart
        return quantities
    def update(self,product,quantity):
        product_id=str(product)
        product_qty=int(quantity)
        ourcart=self.cart
        ourcart[product_id]=product_qty
        self.session.modified=True
        if self.request.user.is_authenticated:
            #get the current user profile 
            current_user=Profile.objects.filter(user__id=self.request.user.id) 
            #{'3':1,'2':4} to{"3":1}  
            carty=str(self.cart)  
            carty=carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))
        thing=self.cart
        return thing 
    def delete(self,product):
        product_id=str(product)
        #delete from ditctionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True
        if self.request.user.is_authenticated:
            #get the current user profile 
            current_user=Profile.objects.filter(user__id=self.request.user.id) 
            #{'3':1,'2':4} to{"3":1}  
            carty=str(self.cart)  
            carty=carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))    