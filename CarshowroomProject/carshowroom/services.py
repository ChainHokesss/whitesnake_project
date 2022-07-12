from .models import CarshowroomModel


class CarshowroomServices:
    def get_crashowroom(self, carshowroom_id):
        return CarshowroomModel.objects.get(id = carshowroom_id)

    def get_purchase_history(self, carshowroom):
        filters = {
            'carshowroom':  carshowroom
        }

    def get_statistics(self, carshowroom):
        data = {
            # 'income':
        }

        return data