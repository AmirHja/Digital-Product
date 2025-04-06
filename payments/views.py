import uuid
import requests

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from payments.models import Gateway, Payment
from payments.serializers import GatewaySerializer
from subscriptions.models import Package, Subscription


class GatewayView(APIView):
    def get(self, request):
        gateway = Gateway.objects.first(is_active=True)
        serializer = GatewaySerializer(gateway, many=True)
        return Response(serializer.data)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gateway_id = request.query_params.get('gateway')
        package_id = request.query_params.get('package')

        try:
            package = Package.objects.get(pk=package_id, is_enable=True)
            gateway = Gateway.objects.get(pk=gateway_id, is_enable=True)
        except (Package.DoesNotExist, Gateway.DoesNotExist):
            return Response(
                data={'error': 'Package or Gateway does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        payment = Payment.objects.create(
            user=request.user,
            package=package,
            gateway=gateway,
            price=package.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4()),
        )

        return Response(data={"token": payment.token, "callback-url": "some url"})

    def post(self, request):
        token = request.data.get('token')
        st = request.data.get('status')

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response(
                data={'error': 'Token does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        if st != 10:
            payment.status = Payment.Status.CANCELLED
            payment.save()

            return Response(
                data={"detail": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        r = requests.post("bank-verify-url", data={})
        if r.status_code // 100 != 2:
            payment.status = Payment.Status.ERROR
            payment.save()

            return Response(
                data={"detail": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = Payment.Status.PAID
        payment.save()

        Subscription.objects.create(
            user=request.user,
            package=payment.package,
            expiry_date=timezone.now() + timezone.timedelta(days=payment.package.duration.days),
        )

        return Response(
            data={"detail": "Payment verification successful"},
            status=status.HTTP_200_OK
        )


