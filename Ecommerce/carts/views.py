from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from .models import *
from products.models import Product

from .serializers import *

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user=user, ordered=False)
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')

        cart_items = CartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        return Response({'success':'Item successfully added to your cart'})

    # put request to update the quantity of existing cart items
    def put(self, request):
        data = request.data
        cart_item = CartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        # print(f"quantity change: {quantity}")
        cart_item.quantity += quantity
        # print(f"final quantity in cart_item: {cart_item.quantity}")
        # print(f"final cart price pre-save: {cart_item.price}")
        cart_item.save()
        # print(f"final cart_item price post-save: {cart_item.price}")
        # print('\n')


        #uptating the total price of items in the cart
        cart = Cart.objects.get(id=cart_item.cart.id)
        # print(f"total cart price post-save: {cart.total_price}")
        product = Product.objects.get(id=cart_item.product.id)
        price_of_product = float(product.price)
        # print(f"quantity change: {quantity}")
        # print(f"price of product: {price_of_product}")
        # print(f"change in price: {quantity*price_of_product}")
        # print(f"initial cart total: {cart.total_price}")
        
        cart.total_price = cart.total_price + (quantity*price_of_product) - cart_item.price 
        #here, - cart_item.price is done because cart_item.save() function calls correct_price() signal which increases the total cart price
        # print(f"Final cart total: {cart.total_price + quantity*price_of_product}")

        cart.save()

        return Response({'success':'Items Updated'})
    
    def delete(self,request):
        user = request.user
        data = request.data

        cart_item = CartItems.objects.get(id=data.get('id'))
        cart_item.delete()
        
        #uptating the total price of items in the cart
        cart = Cart.objects.get(id=cart_item.cart.id)
        cart.total_price = cart.total_price - cart_item.price
        cart.save()

        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)