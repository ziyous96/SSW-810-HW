""" author: Ziyou Shang
This program contains the methods required for homework9
a program to store the data of students, instructors, and grades of different school
in different repository
"""
import os
from collections import defaultdict
from prettytable import PrettyTable


class Repository:
    """ Class to hold all the information for different universities """

    def __init__(self, dire, ptable=True):
        """ Constructor of Repository with list of class Student, Instructor as attributes """

        self.dire = dire   # directory of the data files
        self.students = dict()  # cwid as keys, Student as values
        self.instructors = dict() # cwid as keys, Instructor as values
        self.majors = defaultdict(Major) # major as keys, Major class as values

        try:
            self.get_student_data(os.path.join(dire, 'students.txt'))
            self.get_instructor_data(os.path.join(dire, 'instructors.txt'))
            self.get_grade_data(os.path.join(dire, 'grades.txt'))
            self.get_major_data(os.path.join(dire, 'majors.txt'))
        except ValueError as e1:
            print(e1)
        except FileNotFoundError as e2:
            print(e2)

        self.summarize_student_course()

        if ptable:
            print('\n Major Summary')
            self.pretty_print_major()

            print('\nStudent Summary')
            self.pretty_print_student()

            print('\nInstructor Summary')
            self.pretty_print_instructor()

    def pretty_print_student(self):
        """ Print out a pretty table for the data stored in students """

        pt = PrettyTable()  # initialize prettytable
        pt.field_names = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

        for s in self.students:  # add values

            pt.add_row([s,
                        self.students[s].name,
                        self.students[s].major,
                        sorted(list(self.students[s].course_grade.keys())),
                        self.students[s].rr,
                        self.students[s].re])

        print(pt)

    def pretty_print_instructor(self):
        """ Print out a pretty table for the data stored in instructors """

        pt = PrettyTable()  # initialize prettytable
        pt.field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']

        for i in self.instructors:  # add values
            for k in self.instructors[i].course_student:
                pt.add_row([i,
                            self.instructors[i].name,
                            self.instructors[i].depart,
                            k,
                            self.instructors[i].course_student[k]])

        print(pt)

    def pretty_print_major(self):
        """ Print out a pretty table for the data stored in majors """

        pt = PrettyTable()
        pt.field_names = ['Dept', 'Required', 'Electives']

        for m in self.majors:
            pt.add_row([m, sorted(list(self.majors[m].required)), sorted(list(self.majors[m].elective))])

        print(pt)

    def get_student_data(self, file_path):
        """ Function to get the data from students.txt """

        for cwid, name, major in file_reading_gen(file_path, 3, sep=';', header=True):
            self.students[cwid] = Student(name, major, cwid)

    def get_instructor_data(self, file_path):
        """ Function to get the data from instructors.txt """

        for cwid, name, depart in file_reading_gen(file_path, 3, sep='|', header=True):
            self.instructors[cwid] = Instructor(name, depart, cwid)

    def get_grade_data(self, file_path):
        """ Function to get the data from grades.txt """

        for cwid, course, grade, instructor in file_reading_gen(file_path, 4, sep='|', header=True):
            self.students[cwid].add_grade(course, grade)
            self.instructors[instructor].add_student(course)

    def get_major_data(self, file_path):
        """ Function to get the data from majors.txt """

        for major, r_e, course in file_reading_gen(file_path, 3, sep='\t', header=True):
            # read and store in Major

            self.majors[major].name = major
            if r_e == 'R':
                self.majors[major].required.add(course)
            elif r_e == 'E':
                self.majors[major].elective.add(course)

    def summarize_student_course(self):
        """ Function to organize and summerize the data collected """

        for s in self.students:
            self.students[s].rr = self.majors[self.students[s].major].required.copy()
            self.students[s].re = self.majors[self.students[s].major].elective.copy()

            self.students[s].check_remain_required()
            self.students[s].check_remain_elective()


class Student:
    """ Student class to store the information of students """

    def __init__(self, name, major, cwid):
        """ Constructor of Student class with name, major, cwid as parameters"""

        self.name = name
        self.major = major
        self.cwid = cwid
        self.course_grade = defaultdict(str)  # course as keys, letter grade as values
        self.rr = set()   # a set for the remaining required course the student needs to take
        self.re = set()   # a set for the remaining elective course the student needs to take

    def check_remain_required(self):
        """ check the remaining required course of the student """

        temp = self.rr.copy()
        for c in temp:   # check the grade and remove the unnecessary courses
            if self.course_grade[c] in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                self.rr.remove(c)
            else:
                self.course_grade.pop(c)

    def check_remain_elective(self):
        """ check the remaining elective course of the student """

        temp = self.re.copy()
        for c in temp:   # check the grade and remove the unnecessary courses
            if self.course_grade[c] in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                self.re = None
            else:
                self.course_grade.pop(c)

    def add_grade(self, course, grade):
        """ add grade to the student """

        self.course_grade[course] = grade


class Instructor:
    """ Instructor class to store the information of instructors """

    def __init__(self, name, depart, cwid):
        """ Constructor of Instructor class with name, department, cwid as parameter """

        self.name = name
        self.depart = depart
        self.cwid = cwid
        self.course_student = defaultdict(int)   # course as keys, number of students as values

    def add_student(self, course):
        """ add student to course """

        self.course_student[course] += 1


class Major:
    """ Major class to store the requied courses of the major """

    def __init__(self):
        """ Constructor of Major class with name, requied courses and elective courses """

        self.name = ""    # name of the major
        self.required = set()   # a set for the required courses of the major
        self.elective = set()   # a set for the elective courses of the major


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


def main():
    """ The main function of the program """
    test1 = '/Users/shang/Desktop'
    test2 = '/Users/shang/xx'   # exception case

    r = Repository(test1)
    r2 = Repository(test2)


if __name__ == '__main__':
    main()
