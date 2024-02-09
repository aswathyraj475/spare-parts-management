
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from owner.models import Item  # Import your Item model
from user.models import CustomUser  # Import your CustomUser model
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Cast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, b):
        try:
            item = Item.objects.get(id=b)
            user = request.user
            cart = Cart.objects.get(user=user, item=item)
            if cart.quantity < cart.item.stock:
                cart.quantity += 1
                cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, item=item, quantity=1)
            cart.save()

        return Response(status=status.HTTP_201_CREATED)


class CartRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, b):
        try:
            item = Item.objects.get(id=b)
            user = request.user
            cart = Cart.objects.get(user=user, item=item)
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                cart.delete()
        except Cart.DoesNotExist:
            pass

        return Response(status=status.HTTP_200_OK)


class CartViewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).annotate(
            price_as_decimal=Cast('item__price', DecimalField()),
            subtotal=ExpressionWrapper(
                F('quantity') * F('price_as_decimal'),
                output_field=DecimalField()
            )
        )
        total = cart.aggregate(total=Sum('subtotal'))['total'] or 0
        serializer = CartSerializer(cart, many=True)
        return Response({'cart': serializer.data, 'total': total}, status=status.HTTP_200_OK)

class CartDeleteAPIView(APIView):
    def delete(self, request, b):
        user = request.user
        item = get_object_or_404(Item, id=b)
        try:
            cart = Cart.objects.get(user=user, item=item)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_cart_list(request):
    cart_items = Cart.objects.all()
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)