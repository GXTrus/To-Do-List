from datetime import datetime, timedelta

from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ToDoList:
    def __init__(self):
        db_todo = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base = declarative_base()

        class TaskTable(Base):
            __tablename__ = 'task'
            id = Column(Integer, primary_key=True)
            task = Column(String, default='default_value')
            deadline = Column(Date, default=datetime.today())

            def __repr__(self):
                return f"{self.task}, {self.deadline}"

            def __str__(self):
                return self.task

        self.today = datetime.today().date()

        Base.metadata.create_all(db_todo)
        Session = sessionmaker(bind=db_todo)
        self.session = Session()
        self.TaskTable = TaskTable
        self.work()

    def work(self):
        while True:
            print(
                "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) "
                "Exit")
            user_input = self.enter_choice(('0', '1', '2', '3', '4', '5', '6'))
            if user_input == '1':
                self.today_tasks()
            elif user_input == '2':
                self.weeks_tasks()
            elif user_input == '3':
                self.all_tasks()
            elif user_input == '4':
                self.missed_tasks()
            elif user_input == '5':
                self.add_task()
            elif user_input == '6':
                self.delete_task()
            elif user_input == '0':
                break
        print('Bye!')

    def enter_choice(self, variants):
        while True:
            a = input()
            if a in variants:
                break
            else:
                print('\nerror\n')
        print()
        return a

    def days_tasks(self, day_):
        rows = self.session.query(self.TaskTable).filter(self.TaskTable.deadline == day_).all()
        if len(rows):
            for a in range(len(rows)):
                print(f'{a + 1}. {rows[a]}')
        else:
            print('Nothing to do!')
        print()
        return True

    # 1 Today's tasks
    def today_tasks(self):
        print(f"Today {self.today.day} {self.today.strftime('%b')}:")
        self.days_tasks(self.today)
        return True

    # 2 Week's tasks
    def weeks_tasks(self):
        for day_n in range(7):
            cur_day = self.today + timedelta(days=day_n)
            week_days = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()
            print(f"{week_days[cur_day.weekday()]} {cur_day.day} {cur_day.strftime('%b')}:")
            self.days_tasks(cur_day)
        return True

    # 3 All tasks
    def all_tasks(self):
        rows = self.session.query(self.TaskTable).all()
        print('All tasks:')
        if len(rows):
            for a in range(len(rows)):
                cur_day = rows[a].deadline
                print(f"{a + 1}. {rows[a]}. {cur_day.day} {cur_day.strftime('%b')}")
        else:
            print('Nothing to do!')
        print()
        return True

    # 4 Missed tasks
    def missed_tasks(self):
        rows = self.session.query(self.TaskTable).filter(self.TaskTable.deadline < self.today).all()
        print('Missed tasks:')
        if len(rows):
            for a in range(len(rows)):
                cur_day = rows[a].deadline
                print(f"{a + 1}. {rows[a]}. {cur_day.day} {cur_day.strftime('%b')}")
        else:
            print('Nothing is missed!')
        print()
        return True

    # 5 Add task
    def add_task(self):
        task = input('\nEnter task\n')
        deadline = input('Enter deadline\n')
        new_row = self.TaskTable(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')
        return True

    # 6 Delete task
    def delete_task(self):
        print('\nChose the number of the task you want to delete')
        self.session.query(self.TaskTable).order_by(self.TaskTable.deadline)
        rows = self.session.query(self.TaskTable).all()
        if len(rows):
            for a in range(len(rows)):
                cur_day = rows[a].deadline
                print(f"{a + 1}. {rows[a]}. {cur_day.day} {cur_day.strftime('%b')}")
        x = int(input())
        specific_row = rows[x - 1]
        self.session.delete(specific_row)
        self.session.commit()
        print('The task has been deleted!\n')
        return True


if __name__ == '__main__':
    my_todo_list = ToDoList()
