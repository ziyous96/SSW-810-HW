""" author: Ziyou Shang
These are the test cases for HW10
"""
import unittest

from HW09_Ziyou_Shang import Repository, Major, Instructor, file_reading_gen, Student, main


class TestHW10(unittest.TestCase):
    """ Test cases for HW10 """

    def test_normal_case(self):
        """ Test case for normal situation """

        # expected_major = {('SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']),
        #                   ('SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'])}
        #
        # expected_student = {('10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None),
        #                     ('10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None),
        #                     ('10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 564'], {'SSW 540', 'SSW 564'}, {'CS 513', 'CS 501', 'CS 545'}),
        #                     ('10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, {'CS 513', 'CS 501', 'CS 545'}),
        #                     ('10183', 'Chaoman, O', 'SFEN', ['SSW 689'], {'SSW 555', 'SSW 540'}, {'CS 513', 'CS 501', 'CS 545'}),
        #                     ('11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 800', 'SYS 671'}, None),
        #                     ('11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}),
        #                     ('11658', 'Kelly, P', 'SYEN', [], {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}),
        #                     ('11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}),
        #                     ('11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 800', 'SYS 671'}, None)}
        #
        # expected_instructor = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
        #                        ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
        #                        ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
        #                        ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
        #                        ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
        #                        ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
        #                        ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
        #                        ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
        #                        ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
        #                        ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
        #                        ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
        #                        ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}

        test1 = '/Users/shang/Desktop'
        r = Repository(test1)
        m = Major()
        m.name = 'SFEN'
        m.required = ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567']
        m.elective = ['CS 501', 'CS 513', 'CS 545']
        self.assertEqual(sorted(list(r.majors['SFEN'].required)), m.required)
        self.assertEqual(sorted(list(r.majors['SFEN'].elective)), m.elective)

        s = Student('Baldwin, C', 'SFEN', '10103')
        s.course_grade = {'SSW 567': 'A', 'SSW 564': 'A-', "SSW 687": 'B', 'CS 501': 'B'}
        self.assertEqual(r.students['10103'].name, s.name)
        self.assertEqual(r.students['10103'].major, s.major)
        self.assertEqual(r.students['10103'].course_grade, s.course_grade)

        i = Instructor('Einstein, A', 'SFEN', '98765')
        i.course_student = {'SSW 567' : 4, 'SSW 540': 3}
        self.assertEqual(r.instructors['98765'].name, i.name)
        self.assertEqual(r.instructors['98765'].depart, i.depart)
        self.assertEqual(r.instructors['98765'].course_student, i.course_student)

    def test_exceptions(self):
        """ Test exception cases of this program """

        self.assertRaises(FileNotFoundError, main())

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)