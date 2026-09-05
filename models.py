# models.py

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f'Привет, меня зовут {self.name}!')

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 16 or value > 100:
            raise ValueError('Возраст должен быть целым числом от 16 до 100')
        self.__age = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Имя не может быть пустым')
        self.__name = value.strip()

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self.__grades = []

    def add_grade(self, grade):
        if not isinstance(grade, int) or  grade < 1 or grade > 5:
            raise ValueError('Оценка должна быть целым числом и лежать в диапазоне от 1 до 5')
        self.__grades.append(grade)

    @property
    def average_grade(self):
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)

    def introduce(self):
        super().introduce()
        print(f'Мой ID: {self.student_id}, средний балл: {self.average_grade}')

    def __str__(self):
        return f"Student({self.name}, id={self.student_id}, avg={self.average_grade})"

    @property
    def is_excellent(self):
        return self.average_grade >= 4.8

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'student_id': self.student_id,
            'grades': self.__grades[:]
        }

    @classmethod
    def from_dict(cls, data):
        s = cls(data['name'], data['age'], data['student_id'])
        for g in data.get('grades', []):
            s.add_grade(g)
        return s


class StudentGroup:
    def __init__(self, group_name):
        self.group_name = group_name
        self.students = []

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError('Студент должен быть типом Student')
        if self.find_student(student.student_id) is not None:
            raise ValueError('Студент с таким ID уже есть в группе')
        self.students.append(student)


    @property
    def average_group_grade(self):
        if not self.students:
            return 0
        sm = 0
        for student in self.students:
            sm += student.average_grade
        return sm / len(self.students)


    def print_all(self):
        for student in self.students:
            student.introduce()

    def __str__(self):
        return f"Group {self.group_name}: {len(self.students)} студентов"

    @property
    def student_count(self):
        return len(self.students)

    def to_dict(self):
        return {
            'group_name': self.group_name,
            'students': [student.to_dict() for student in self.students]
        }

    @classmethod
    def from_dict(cls, data):
        g = cls(data['group_name'])
        for stud_data in data.get('students', []):
            g.add_student(Student.from_dict(stud_data))

        return g

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def remove_student(self, student_id):
        st = self.find_student(student_id)
        if st is None:
            return False
        self.students.remove(st)
        return True

    def __len__(self):
        return len(self.students)

    def __contains__(self, item):
        if isinstance(item, Student):
            return any(student.student_id == item.student_id for student in self.students)
        return any(student.student_id == item for student in self.students)

    def __iter__(self):
        for student in self.students:
            yield student

    def __getitem__(self, item):
        s = self.find_student(item)
        if s is None:
            raise KeyError('Студента с таким ID в группе нет')
        return s

    def add_grade_to(self, student_id, grade):
        s = self.find_student(student_id)
        if s is None:
            raise KeyError('Студента с таким ID в группе нет')
        s.add_grade(grade)