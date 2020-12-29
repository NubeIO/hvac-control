from flask_restful import Resource, reqparse, abort

from src import db
from src.lora.device_registry import DeviceRegistry
from src.models.model_sensor import SensorModel


class SensorBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('id', type=str, required=True, dest='device_id')
    parser.add_argument('sensor_type', type=str, required=True)
    parser.add_argument('sensor_model', type=str, required=True)
    parser.add_argument('micro_edge_input_type', type=str, required=True)
    parser.add_argument('sensor_wake_up_rate', type=int, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('enable', type=bool, required=True)
    parser.add_argument('fault', type=int)
    parser.add_argument('data_round', type=int)
    parser.add_argument('data_offset', type=float)

    def add_sensor(self, uuid, data):
        try:
            sensor = SensorModel(uuid=uuid, **data)
            sensor.save_to_db()
            return sensor
        except Exception as e:
            abort(500, message=str(e))

    def update_sensor(self, uuid, data):
        SensorModel.filter_by_uuid(uuid).update(data)
        db.session.commit()
        sensor_return = SensorModel.find_by_uuid(uuid)
        DeviceRegistry.get_instance().add_device(sensor_return.name, uuid)
        return sensor_return