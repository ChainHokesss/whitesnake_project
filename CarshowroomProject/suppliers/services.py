from .models import SupplierModel


class SuppliersService:
    def get_cars(self, supplier_id):
        supplier = SupplierModel.objects.prefetch_related('car_list').get(id = supplier_id)

        return supplier.car_list