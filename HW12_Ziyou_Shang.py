""" author: Ziyou Shang
This program contains the methods required for homework12
a program to store the data of students, instructors, and grades of different school
in different repository
"""

import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/instructors')
def instructors():
    dbpath = '/Users/shang/Desktop/homework/test1/810_hw.db'

    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {dbpath}"
    else:
        query = "select i.CWID, i.Name, i.Dept, g.Course, count(g.StudentCWID) as Students from instructors i join " \
                "grades g on i.CWID = g.InstructorCWID group by i.CWID, i.Name, i.Dept, g.Course "

    # convert the query result to a list of dictionaries to pass to the template
    data = [{'CWID': cwid, 'Name': name, 'Dept': dept, 'Course': course, 'Students': students}
            for cwid, name, dept, course, students in db.execute(query)]

    db.close()  # close the connection to the database

    return render_template('HW12.html',
                           title='Stevens Repository',
                           table_title='Courses and student counts',
                           instructors=data)


app.run(debug=True)
