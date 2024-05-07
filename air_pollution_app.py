from flask import Flask, request, jsonify
from flask.views import MethodView
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError