from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Invoice
from yookassa import Payment


def check_payment(id_payment):
    payment = Payment.find_one(id_payment)
    return payment.status


class Command(BaseCommand):
    help = "Проверить статусы платежей"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            invoices = Invoice.objects.filter(status="1")
            for invoice in invoices:
                payment_status = check_payment(invoice.yoomoney_id)
                if payment_status == "succeeded":
                    invoice.status = "2"
                    invoice.save()
