from flaskr.db import get_db
import logging


class StudentsRepository:
    def __init__(self):
        self.db = get_db()

    def get_students(self, query_args=None):
        if query_args is not None and (len(query_args) > 0) is True:
            query_string = 'SELECT * FROM students WHERE '

            args_length = len(query_args)
            index = 0
            for key, value in query_args.items():
                query_string += f"{key} = '{value}'"

                index += 1
                if index < args_length:
                    query_string += ' AND '

            query_string += ' ORDER BY lastName ASC'
            students = self.db.execute(query_string).fetchall()
        else:
            students = self.db.execute(
                        'SELECT * FROM students ORDER BY lastName ASC'
                    ).fetchall()

        students = self.get_list_from_rows(students)
        return students

    def get_student(self, id):
        student = self.db.execute(
                    'SELECT * FROM students WHERE id = ?', (id,)
                ).fetchone()

        if student is None:
            return None
        else:
            student = self.get_dict_from_row(student)
            return student

    def create_student(self, json_student):
        self.db.execute(
            'INSERT INTO students (firstName, lastName, age, specialization)'
            ' VALUES (?, ?, ?, ?)',
            (json_student['firstName'], json_student['lastName'],
                json_student['age'], json_student['specialization'])
                )
        self.db.commit()

    def update_student(self, json_student):
        self.db.execute(
            'UPDATE students SET firstName = ?, lastName = ?, age = ?, specialization = ? WHERE id = ?',
            (json_student['firstName'], json_student['lastName'],
                json_student['age'], json_student['specialization'], json_student['id'])
                )
        self.db.commit()
    
    def delete_student(self, id):
        self.db.execute('DELETE FROM students WHERE id = ?', (id,))
        self.db.commit()

    def get_dict_from_row(self, row):
        return [x for x in row]

    def get_list_from_rows(self, rows):
        row_list = []
        for row in rows:
            row_list.append([x for x in row])
        return row_list
