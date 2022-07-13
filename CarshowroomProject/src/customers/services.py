from src.customers.models import CustomerModel

class CustomerService:
    def get_customer(self, customer_id):
        return CustomerModel.objects.get(user = customer_id)
