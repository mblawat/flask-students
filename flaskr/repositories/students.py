from ..db import students_db
from ..db import Student
from ..errors.exceptions import EntityNotFoundException


class StudentsRepository:
    def get_all(self, query_args=None):
        if query_args is not None and (len(query_args) > 0) is True:
            query = self.student_query_from(query_args)
            students = query.all()
        else:
            students = Student.query.all()
        return students

    def get(self, id):
        return Student.query.filter_by(id=id).first()

    def create_student(self, json_student):
        student = Student()
        student.update_with(json_student)
        students_db.session.add(student)
        students_db.session.commit()
        return student.id

    def update(self, id, json_student):
        student = self.get(id)
        if student is None:
            raise EntityNotFoundException(f"Student with id {id} not found.")

        student.update_with(json_student)
        students_db.session.commit()

    def delete(self, id):
        student = self.get(id)
        if student is not None:
            students_db.session.delete(student)
            students_db.session.commit()

    def student_query_from(self, query_dict):
        query = Student.query

        if query_dict.get('id') is not None:
            query = query.filter(
                Student.id == query_dict.get('id')
            )
        if query_dict.get('fname') is not None:
            query = query.filter(
                Student.fname == query_dict.get('fname')
            )
        if query_dict.get('lname') is not None:
            query = query.filter(
                Student.lname == query_dict.get('lname')
            )
        if query_dict.get('agegrup') is not None:
            query = query.filter(
                Student.agegrup == query_dict.get('agegrup')
            )
        if query_dict.get('specialization') is not None:
            query = query.filter(
                Student.specialization == query_dict.get('specialization')
            )

        return query
