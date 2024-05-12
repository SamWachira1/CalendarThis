import os 
import sqlite3
from datetime import datetime
from flask import render_template, redirect, Blueprint
from ..forms import AppointmentForm

bp = Blueprint('main', __name__)
DB_FILE = os.environ.get("DB_FILE")



@bp.route('/', methods=['GET', 'POST'])
def main():
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

        return redirect('/')

    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime')
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
