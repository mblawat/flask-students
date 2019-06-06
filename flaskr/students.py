import json
from flask import (
    Blueprint, request, make_response
)
from werkzeug.exceptions import abort
from .repositories.students import StudentsRepository

bp = Blueprint('students', __name__)


@bp.route('/students/', defaults={'id': None}, methods=['GET'])
@bp.route('/students/<id>', methods=['GET'])
def index(id):
    repository = StudentsRepository()

    if id is None:
        students = repository.get_students(request.args)
        jResult = json.dumps(students)
        return create_response(response_body=jResult)
    else:
        student = repository.get_student(id)
        if student is None:
            abort(404, f"Student id {id} does not exist.")

        jResult = json.dumps(student)
        return create_response(response_body=jResult)


@bp.route('/students', methods=['POST'])
def create():
    repository = StudentsRepository()

    json_student = request.get_json()
    if json_student['firstName'] is None or \
            json_student['lastName'] is None or \
            json_student['age'] is None or \
            json_student['specialization'] is None:
        abort(400, f"Student data is incorrect.")

    repository.create_student(json_student)
    return create_response(status_code=201)


@bp.route('/students/<id>', methods=['PUT'])
def update(id):
    json_student = request.get_json()
    if json_student['firstName'] is None or \
            json_student['lastName'] is None or \
            json_student['age'] is None or \
            json_student['specialization'] is None:
        abort(400, f"Student data is incorrect.")

    repository = StudentsRepository()

    student = repository.get_student(id)
    if student is None:
        abort(404, f"Student id {id} does not exist.")

    repository.update_student(json_student)
    return create_response()


@bp.route('/students/<id>', methods=['DELETE'])
def delete(id):
    repository = StudentsRepository()
    repository.delete_student(id)
    return create_response()


def create_response(response_body=None, status_code=200):
    response = make_response(response_body, status_code)
    response.mimetype = 'application/json'
    return response
