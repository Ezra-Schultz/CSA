from __future__ import print_function
import classroom_functions


def main():
    classManager = classroom_functions.AssignmentManager()
    print(classManager.select_course())

    # classManager.post_assignment('')

if __name__ == '__main__':
    main()
