from flask_restful import Resource, reqparse, abort
from src import db
from src.models.model_schedule import ScheduleModel


class ScheduleBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('enable', type=bool, required=True)

    def add_schedule(self, uuid, data):
        try:
            sch = ScheduleModel(uuid=uuid, **data)
            sch.save_to_db()
            return sch
        except Exception as e:
            abort(500, message=str(e))

    def update_schedule(self, uuid, data):
        ScheduleModel.filter_by_uuid(uuid).update(data)
        db.session.commit()
        sch_return = ScheduleModel.find_by_uuid(uuid)
        return sch_return
