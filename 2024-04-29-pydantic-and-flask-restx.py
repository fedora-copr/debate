"""
Heavily inspired by https://github.com/python-restx/flask-restx/issues/59#issuecomment-899790061

Run like `python3 <the-file-name>`.

PROBLEMS:
- we aren't able to document the fields in models using Pydantic
"""

import json
import random
from datetime import datetime
from typing import *

import flask
from flask_restx import Api, Namespace, Resource
from pydantic import BaseModel, Field, ValidationError


class Error(BaseModel):
    error: str
    code: int

    # TODO: is this needed?
    class Config:
        @staticmethod
        def json_schema_extra(schema: dict, model):
            schema["properties"].pop("code")
            # This just hides the "code" key from the generated schema.


class Network(BaseModel):
    id: str
    state: str
    created: str
    title: str
    owner: str
    description: str
    node_count: int
    link_count: int


class AssignedHost(BaseModel):
    uid: int
    hostname: str
    pop: str


class Reservation(BaseModel):
    uid: int
    status: str
    owner: str
    created_at: datetime
    networks: Union[List[Union[Network, Error]], Error] = Field(default_factory=list)
    host: AssignedHost


app = flask.Flask(__name__)
app.config["RESTX_INCLUDE_ALL_MODELS"] = True
api_blueprint = flask.Blueprint("api", __name__)
show_blueprint = flask.Blueprint("show", __name__, url_prefix="/show")
api = Api(api_blueprint, title="with pydantic")
ns = Namespace("ns", path="/namespace")
app.register_blueprint(api_blueprint, url_prefix="/api")

ns.schema_model(Error.__name__, Error.schema())
ns.schema_model(Network.__name__, Network.schema())
ns.schema_model(AssignedHost.__name__, AssignedHost.schema())
ns.schema_model(Reservation.__name__, Reservation.schema())

api.add_namespace(ns)


def get_stuff_from_backend(id: int):
    return Reservation(
        uid=id,
        status="golden",
        # randomize ValidationError
        owner=random.choice((1, "jdoe")),
        created_at=datetime.now(),
        networks=[], 
        host=AssignedHost(uid=1, hostname="example.com", pop="LHR"),
    )


# Handle pydantic's validation as error 400
@ns.errorhandler(ValidationError)
def handle_pydantic_validation_error(_err):
    # where the returning "error.message" comes from?
    return json.loads(Error(code=400, error="bad request").json()), 400

@ns.route("/get/<id>/")
class Sample(Resource):
    @ns.response(200, "Success", ns.models["Reservation"])
    @ns.response("40x,50x", "Error", ns.models["Error"])
    def get(self, id):
        result = get_stuff_from_backend(id)
        return json.loads(result.json())


# Normal non-blueprint route
@app.route("/")
def show():
    return "Hello world! Check /api/namespace/get/ID/"


if __name__ == "__main__":
    print(app.url_map)
    app.run()
