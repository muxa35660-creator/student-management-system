# main.py
from models import Student, StudentGroup
from storage import save_group, load_group

FILENAME = "group.json"


def main():
    group = StudentGroup('ИТ-101')

    while True:
        print("\n--- МЕНЮ ---")
        print("1) Показать список студентов")
        print("2) Добавить студента")
        print("3) Удалить студента по ID")
        print("4) Добавить оценку по ID")
        print("5) Средний балл группы")
        print("6) Сохранить")
        print("7) Загрузить")
        print('8) Показать студента по ID')
        print('9) Показать отличников')
        print('10) Переименовать студента')
        print("0) Выход")

        choice = input('Выбор: ').strip()

        try:
            if choice == '1':
                group.print_all()

            elif choice == '2':
                name = input('Имя: ').strip()
                age = int(input('Возраст: '))
                student_id = input('ID: ').strip()
                s = Student(name, age, student_id)
                group.add_student(s)
                save_group(group, FILENAME)
                print('Студент добавлен')

            elif choice == "3":
                student_id = input("ID: ").strip()
                removed = group.remove_student(student_id)
                if removed:
                    save_group(group, FILENAME)
                print("Удалён" if removed else "Нет такого студента")

            elif choice == "4":
                student_id = input("ID: ").strip()
                grade = int(input("Оценка (1-5): ").strip())
                group.add_grade_to(student_id, grade)
                save_group(group, FILENAME)
                print("ОК: оценка добавлена")

            elif choice == "5":
                print("Студентов:", group.student_count)
                print("Средний балл группы:", group.average_group_grade)

            elif choice == "6":
                save_group(group, FILENAME)
                print("ОК: сохранено")

            elif choice == "7":
                group = load_group(FILENAME)
                print("ОК: загружено")

            elif choice == '8':
                ID = input('ID студента: ')
                print(group[ID])

            elif choice == '9':
                excellent = [s for s in group if s.is_excellent]
                if not excellent:
                    print('Отличников в группе нет')

                else:
                    print('Отличники: ')
                    for ind, student in enumerate(excellent, 1):
                        print(f'{ind}. {student.name}, {student.age} лет, средний балл={student.average_grade}, ID={student.student_id}')

            elif choice == '10':
                st_id = input('ID студента:').strip()
                st = group.find_student(st_id)
                if st is None:
                    print('Студента с таким ID в группе нет')
                else:
                    new_name = input('Новое имя: ').strip()
                    if new_name == st.name:
                        print('Имя студента осталось прежним')
                    else:
                        st.name = new_name
                        save_group(group, FILENAME)

            elif choice == "0":
                break

            else:
                print("Нет такого пункта меню")
        except FileNotFoundError as e:
            print('Файл с таким именем не найден', e)
        except (ValueError, TypeError, KeyError) as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    main()