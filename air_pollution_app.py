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