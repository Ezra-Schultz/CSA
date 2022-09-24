import csv

"""
Opens the CSV File and stores all the data in an array
Removes the header from the CSV File
Converts String ID to Ints
"""


def import_data():
    data = []
    with open('JBUDB.csv') as db_data:
        in_data = csv.reader(db_data, delimiter=',')
        for r in in_data:
            data.append(r)

        del data[0]

        for x in data:
            x[0] = int(x[0])

    return data


def find_by_id(id: int):
    return [i for i in import_data() if i[0] == id]


def find_by_firstname(firstname: str):
    return [i for i in import_data() if i[1] == firstname]


def find_by_lastname(lastname: str):
    return [i for i in import_data() if i[2] == lastname]


def find_by_email(email: str):
    return [i for i in import_data() if i[3] == email]


def find_by_position(position: str):
    return [i for i in import_data() if i[4] == position]


def find_by_department(department: str):
    return [i for i in import_data() if i[5] == department]
def add_user(firstname, lastname, position, department):
    with open('JBUDB.csv','a') as file:
        email = f"{firstname}.{lastname}@jbu.edu"
        if (find_by_email(email) == []):
            file.write(f'\n{import_data()[-1][0] + 1},{firstname},{lastname},{email},{position},{department}')
        else:
            print('Could not add user: email already present')


if __name__ == '__main__':
    # print(import_data())
    print(find_by_id(1024))
    print(find_by_firstname('Loree'))
    print(find_by_lastname('Weide'))
    print(find_by_email('Krystle.Wenoa@jbu.edu'))
    print(find_by_position('Professor'))
    print(find_by_department('Computer Science'))
    add_user('Hello', 'World', 'Professor', 'Computer Science')
