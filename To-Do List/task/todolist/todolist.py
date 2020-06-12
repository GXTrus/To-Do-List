from datetime import datetime

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
            print("1) Today's tasks\n2) Add task\n0) Exit")
            user_input = self.enter_choice(('0', '1', '2'))
            if user_input == '2':
                self.add_task()
            elif user_input == '1':
                self.today_task()
            if user_input == '0':
                break
        print('\nBye!')

    def enter_choice(self, variants):
        while True:
            a = input()
            if a in variants:
                break
            else:
                print('\nerror\n')
        return a

    def today_task(self):
        print('\nToday:')
        rows = self.session.query(self.TaskTable).filter(self.TaskTable.deadline == self.today).all()
        if len(rows):
            for a in range(len(rows)):
                print(f'{a + 1}. {rows[a]}')
            print()
        else:
            print('Nothing to do!\n')
        return

    def add_task(self):
        print('\nEnter task')
        task = input()
        new_row = self.TaskTable(task=task)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')
        return


if __name__ == '__main__':
    my_todo_list = ToDoList()
