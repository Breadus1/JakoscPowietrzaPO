from flask import Flask, request, jsonify
from flask.views import MethodView
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)

class PollutionDataModel(BaseModel):
    recorded_at: datetime
    temperature: Optional[int] = Field(None, ge=-50, le=50)
    pressure: Optional[int] = Field(None, ge=800, le=1200)
    humidity: Optional[int] = Field(None, ge=0, le=100)
    air_quality: Optional[int] = Field(None, ge=0)

class DataRepository:
    def __init__(self):
        self.data: List[PollutionDataModel] = []

    def add_data(self, record):
        self.data.append(record)

    def get_nearest(self, query_time):
        if not self.data:
            return None
        return min(self.data, key=lambda r: abs(r.recorded_at - query_time))

repo = DataRepository()

class PollutionDataEndpoint(MethodView):
    def post(self):
        try:
            data = request.json
            new_entry = PollutionDataModel(**data)
            repo.add_data(new_entry)
            return jsonify(new_entry.dict()), 201
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400

    def get(self):
        timestamp = request.args.get('timestamp')
        if not timestamp:
            return jsonify({"error": "Timestamp query parameter is required."}), 400

        query_time = datetime.fromisoformat(timestamp)
        closest = repo.get_nearest(query_time)
        return jsonify(closest.dict()) if closest else jsonify({"message": "No data found."}), 404

app.add_url_rule('/pollution', view_func=PollutionDataEndpoint.as_view('pollution_api'))

if __name__ == '__main__':
    app.run(debug=True)