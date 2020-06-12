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
            print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
            user_input = self.enter_choice(('0', '1', '2', '3', '4'))
            if user_input == '1':
                self.today_task()
            elif user_input == '2':
                self.week_task()
            elif user_input == '3':
                self.all_tasks()
            elif user_input == '4':
                self.add_task()
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

    def today_task(self):
        print(f"Today {self.today.day} {self.today.strftime('%b')}:")
        self.days_tasks(self.today)
        return True

    def week_task(self):
        for day_n in range(7):
            cur_day = self.today + timedelta(days=day_n)
            week_days = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()
            print(f"{week_days[cur_day.weekday()]} {cur_day.day} {cur_day.strftime('%b')}:")
            self.days_tasks(cur_day)
        return True

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
        return

    def add_task(self):
        task = input('\nEnter task\n')
        deadline = input('Enter deadline')
        new_row = self.TaskTable(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')
        return


if __name__ == '__main__':
    my_todo_list = ToDoList()
