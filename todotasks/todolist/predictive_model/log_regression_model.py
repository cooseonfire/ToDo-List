import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import itertools
import datetime


log_reg_model = LogisticRegression()  # initiate model


def preprocess_todo(todo):
    priority = todo.priority
    if todo.is_finished:
        delta = todo.finished_date - todo.created_date
    else:
        delta = datetime.date.today() - todo.created_date
    duration = delta.days
    if todo.deadline:
        deadline_delta = datetime.date.today() - todo.deadline
        is_before_deadline = 1 if deadline_delta.days <= 0 else 0
    else:
        is_before_deadline = 1
    is_finished = 1 if todo.is_finished else 0
    return priority, duration, is_before_deadline, is_finished


def train_data(user):
    data = []
    for todolist in itertools.chain(user.todolists.all()):
        for todo in todolist.todos.all():
            data.append(preprocess_todo(todo))

    return data



def train(user):
    data = train_data(user)
    cols = ['priority', 'duration', 'is_before_deadline', 'is_finished']
    pd_df = pd.DataFrame(data, columns=cols)
    pd_df.head()

    # split
    feature_cols = ['priority', 'duration', 'is_before_deadline']
    X = pd_df[feature_cols]
    y = pd_df.is_finished

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    log_reg_model.fit(X_train, y_train)
    y_pred = log_reg_model.predict(X_test)

    return accuracy_score(y_test, y_pred), X_train, y_train


def predict(user):
    data = []
    for todolist in itertools.chain(user.todolists.all()):
        for todo in todolist.todos.all():
            if not todo.is_finished:
                data.append(preprocess_todo(todo))

    cols = ['priority', 'duration', 'is_before_deadline', 'is_finished']
    pd_df = pd.DataFrame(data, columns=cols)
    pd_df.head()

    feature_cols = ['priority', 'duration', 'is_before_deadline']
    X_data = pd_df[feature_cols]

    _, x_train, y_train = train(user)
    log_reg_model.fit(x_train, y_train)
    return log_reg_model.predict(X_data)

