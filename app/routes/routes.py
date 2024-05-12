import os 
import sqlite3
from datetime import datetime, timedelta
from flask import render_template, redirect, Blueprint, url_for
from ..forms import AppointmentForm

bp = Blueprint('main', __name__)
DB_FILE = os.environ.get("DB_FILE")



# @bp.route('/', methods=['GET', 'POST'])
# def main():
#     form = AppointmentForm()

#     if form.validate_on_submit():
#         with sqlite3.connect(DB_FILE) as conn:
#             curs = conn.cursor()

#             params = {
#                 'name': form.name.data,
#                 'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
#                 'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
#                 'description': form.description.data,
#                 'private': form.private.data
#             }

#         curs.execute(""" INSERT INTO appointments(name, start_datetime, end_datetime, description, private)
#                             VALUES(:name, :start_datetime, :end_datetime, :description, :private)
#                      """, params)
#         conn.commit()

#         return redirect('/')

#     with sqlite3.connect(DB_FILE) as conn:
#         curs = conn.cursor()
#         curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime')
#         rows = curs.fetchall()

#         appointments = [] 
#         for row in rows:
#             appointment = list(row)
#             start_datetime = datetime.strptime(appointment[2], "%Y-%m-%d %H:%M:%S")
#             end_datetime = datetime.strptime(appointment[3], "%Y-%m-%d %H:%M:%S")
#             appointment[2] = start_datetime
#             appointment[3] = end_datetime
#             appointments.append(appointment)
#     return render_template('main.html', appointments=appointments, form=form)

@bp.route('/', methods=['GET', 'POST'])
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route("/<int:year>/<int:month>/<int:day>", methods=["GET", "POST"])
def daily(year, month, day):
    form = AppointmentForm()

    if form.validate_on_submit():
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()

            params = {
                'name': form.name.data,
                'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
                'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
                'description': form.description.data,
                'private': form.private.data
            }

        curs.execute(""" INSERT INTO appointments(name, start_datetime, end_datetime, description, private)
                            VALUES(:name, :start_datetime, :end_datetime, :description, :private)
                     """, params)
        conn.commit()

        return redirect(url_for('.main'))

    day = datetime(year, month, day)
    next_day = day + timedelta(days=1)

    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments WHERE start_datetime BETWEEN :day AND :next_day ORDER BY start_datetime', (day, next_day))
        rows = curs.fetchall()

        appointments = [] 
        for row in rows:
            appointment = list(row)
            start_datetime = datetime.strptime(appointment[2], "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(appointment[3], "%Y-%m-%d %H:%M:%S")
            appointment[2] = start_datetime
            appointment[3] = end_datetime
            appointments.append(appointment)
    return render_template('main.html', appointments=appointments, form=form)
