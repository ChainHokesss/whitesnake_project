from django.db.models.signals import m2m_changed
from .models import DiscountModel

def add_supplier_to_discountbase(sender, **kwargs):
    print(sender)
    print(kwargs)


m2m_changed.connect(add_supplier_to_discountbase, sender=DiscountModel.car.through, action = "post_add")