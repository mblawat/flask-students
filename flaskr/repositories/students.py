from ..db import students_db
from ..db import Student
from ..errors.exceptions import EntityNotFoundException


class StudentsRepository:
    def get_students(self, query_args=None):
        if query_args is not None and (len(query_args) > 0) is True:
            query = self.student_query_from(query_args)
            students = query.all()
        else:
            students = Student.query.all()
        return students

    def get_student(self, id):
        return Student.query.filter_by(id=id).first()

    def create_student(self, json_student):
        student = Student()
        student.update_with(json_student)
        students_db.session.add(student)
        students_db.session.commit()
        return student.id

    def update_student(self, json_student):
        id = json_student['id']
        student = self.get_student(id)
        if student is None:
            raise EntityNotFoundException(f"Student with id {id} not found.")

        student.update_with(json_student)
        students_db.session.commit()

    def delete_student(self, id):
        student = self.get_student(id)
        if student is not None:
            students_db.session.delete(student)
            students_db.session.commit()

    def student_query_from(self, query_dict):
        query = Student.query

        if query_dict.get('id') is not None:
            query = query.filter(
                Student.id == query_dict.get('id')
            )
        if query_dict.get('firstName') is not None:
            query = query.filter(
                Student.firstName == query_dict.get('firstName')
            )
        if query_dict.get('lastName') is not None:
            query = query.filter(
                Student.lastName == query_dict.get('lastName')
            )
        if query_dict.get('age') is not None:
            query = query.filter(
                Student.age == query_dict.get('age')
            )
        if query_dict.get('specialization') is not None:
            query = query.filter(
                Student.specialization == query_dict.get('specialization')
            )

        return query
