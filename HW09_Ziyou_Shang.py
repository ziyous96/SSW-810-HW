""" author: Ziyou Shang
This program contains the methods required for homework9
a program to store the data of students, instructors, and grades of different school
in different repository
"""
from collections import defaultdict

from prettytable import PrettyTable


class Repository:
    """ Class to hold all the information for different universities """

    def __init__(self, students, instructors):
        """ Constructor of Repository with list of class Student, Instructor as attributes """

        self.students = students
        self.instructors = instructors

    def pretty_print_student(self):
        """ Print out a pretty table for the data stored of students """

        pt = PrettyTable()      # initialize prettytable
        pt.field_names = ['CWID', 'Name', 'Completed Courses', 'Major']

        for s in self.students:        # add values
            pt.add_row([s.cwid, s.name, list(s.course_grade.keys()), s.major])

        print(pt)

    def pretty_print_instructor(self):
        """ Print out a pretty table for the data stored of instructors """

        pt = PrettyTable()      # initialize prettytable
        pt.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']

        for i in self.instructors:        # add values
            for k in i.course_student:
                pt.add_row([i.cwid, i.name, i.depart, k, i.course_student[k]])

        print(pt)


class Student:
    """ Student class to store the information of students """

    def __init__(self, name, major, cwid):
        """ Constructor of Student class with name, major, cwid as parameters"""

        self.name = name
        self.major = major
        self.cwid = cwid
        self.course_grade = defaultdict(str)


class Instructor:
    """ Instructor class to store the information of instructors """

    def __init__(self, name, depart, cwid):
        """ Constructors of Instructor class with name, department, cwid as parameter """

        self.name = name
        self.depart = depart
        self.cwid = cwid
        self.course_student = defaultdict(int)


def file_reading_gen(path, fields, sep=',', header=False):
    """ Read files with a fixed number of fields and a pre-defined separating character """

    try:
        fp = open(path, 'r')  # open and read file
    except FileNotFoundError:
        print(f"Cannot open {path}")

    else:
        with fp:
            count = 0  # variable to count the line
            for line in fp:

                if header:  # skip the header if necessary
                    header = False
                    continue

                line = line.strip('\n')
                count += 1
                result = line.split(sep)  # separate the line and store the fields

                if len(result) != fields:
                    raise ValueError(f"{path} has {len(result)} fields on line {count} but expected {fields}.")

                yield tuple(result)


def summarize_files(file_path1, file_path2, file_path3):
    """ function to read, summarize, and store the data """

    students = []   # initialize lists for students and instructors
    instructors = []

    for cwid, name, major in file_reading_gen(file_path1, 3, sep='\t', header=False):
        students.append(Student(name, major, cwid))            # read and store students.txt

    for cwid, name, depart in file_reading_gen(file_path2, 3, sep='\t', header=False):
        instructors.append(Instructor(name, depart, cwid))     # read and store instructors.txt

    for cwid, course, grade, instructor in file_reading_gen(file_path3, 4, sep='\t', header=False):
        for s in students:         # read and store grades.txt
            if cwid == s.cwid:
                s.course_grade[course] = grade
        for i in instructors:
            if instructor == i.cwid:
                i.course_student[course] += 1

    rep = Repository(students, instructors)
    return rep


def main(file1, file2, file3):
    """ The main function of the program """

    summarize_files(file1, file2, file3)


def test_suite():
    """ Automated test to check the result """

    r = summarize_files('students.txt', 'instructors.txt', 'grades.txt')
    r.pretty_print_student()  # print the prettytable to check the result
    r.pretty_print_instructor()

test_suite()