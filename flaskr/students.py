import json
from flask import (
    Blueprint, request, make_response, url_for
)
from werkzeug.exceptions import abort
from .db import object_as_dict
from .repositories.students import StudentsRepository
from .errors.exceptions import EntityNotFoundException

bp = Blueprint('students', __name__)


@bp.route('/students/', defaults={'id': None}, methods=['GET'])
@bp.route('/students/<id>', methods=['GET'])
def index(id):
    repository = StudentsRepository()

    if id is None:
        students = repository.get_all(request.args)
        students = [object_as_dict(x) for x in students]
        jResult = json.dumps(students)
        return create_response(response_body=jResult)
    else:
        student = repository.get(id)
        if student is None:
            abort(404, f"Student id {id} does not exist.")

        jResult = json.dumps(object_as_dict(student))
        return create_response(response_body=jResult)


@bp.route('/students', methods=['POST'])
def create():
    json_student = request.get_json()
    if json_student['fname'] is None or \
            json_student['lname'] is None or \
            json_student['agegrup'] is None or \
            json_student['specialization'] is None:
        abort(400, f"Student data is incorrect.")

    repository = StudentsRepository()
    id = repository.create_student(json_student)
    url = "http://localhost:5000" + url_for('students.index') + str(id)
    response_json = json.dumps({"url": url})
    return create_response(response_body=response_json, status_code=201)


@bp.route('/students/<id>', methods=['PUT'])
def update(id):
    json_student = request.get_json()
    if json_student['fname'] is None or \
            json_student['lname'] is None or \
            json_student['agegrup'] is None or \
            json_student['specialization'] is None:
        abort(400, f"Student data is incomplete.")

    repository = StudentsRepository()

    try:
        repository.update(id, json_student)
    except EntityNotFoundException as exception:
        abort(404, str(exception))
    else:
        return create_response()


@bp.route('/students/<id>', methods=['DELETE'])
def delete(id):
    repository = StudentsRepository()
    repository.delete(id)
    return create_response()


def create_response(response_body='{}', status_code=200):
    response = make_response(response_body, status_code)
    response.mimetype = 'application/json'
    return response
