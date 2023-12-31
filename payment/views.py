from .serializers import PaymentSerializer
from .models import Payment
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from rest_framework import status


@api_view(['POST'])
def PaymentList(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'JWT token is missing'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
        user = User.objects.get(id=payload['id'])
        payments = Payment.objects.filter(user=user)
        payment_data_list = []

        for payment in payments:
            payment_data = {
                'id': payment.id,
                'commande_id' : payment.commande_id,
                'cardNumber' : payment.cardNumber,
                'cvv' : payment.cvv,
                'expirationDate' : payment.expirationDate,
                'price' : payment.price,
                'transactionDate' : payment.transactionDate,
            }
            payment_data_list.append(payment_data)
        return Response(payment_data_list, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'JWT token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'error': 'Invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def PaymentDetail(request, pk):
    try:
        payment = Payment.objects.get(id=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def PaymentCreate(request):
    try:
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        request.data['user'] = payload.get('id')

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
