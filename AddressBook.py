import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
from colorama import init, Fore


class AddressBook(UserDict):
    file_name = 'AddressBook.bin'

    def show_all_records(self):
        return self.data

    def iterate(self, n=1):
        for key, value in self.data.items():
            d_list = list(self.data.values())
            for i in range(0, len(d_list), n):
                yield key, d_list[i:i + n]

    def add_record(self, record):
        self.data[record.name.value] = record

    def save_contacts(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.data, f)
        print(f'Your contact saved!')

    def load_contacts(self):
        try:
            with open(self.file_name, 'rb') as f:
                self.data = pickle.load(f)
        except:
            return


class Record:
    def __init__(self, name, phone=None, email=None, birthday=None):
        self.name = name
        self.email = email
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)
            print(self.phones)

    def add_phone(self, phone):
        self.phones.append(phone)
        # print(self.phones)

    def create_phone(self, record, user_input=None, update=False):
        if user_input:
            for i in range(10):
                phone = Phone(user_input)
                if phone.validate_phone(user_input):
                    if update:
                        record.phones = [phone]
                    else:
                        record.add_phone(phone)
                    break
                else:
                    print("Incorrect phone number format entered.\n"
                          "Enter your phone in the format '+380991122333'")
                    user_input = input("Enter contact phone: ")

    def create_email(self, record, user_email):
        if user_email:
            for i in range(10):
                email = Email(user_email)
                if email.validate_email(user_email):
                    record.email = email
                    break
                else:
                    print("Email entered incorrectly.\n"
                          "Please enter a valid email: 'example@gmail.com'")
                    user_email = input("Enter contact email: ")

    def create_birthday(self, record, user_birthday):
        if user_birthday:
            for i in range(10):
                birthday = Birthday(user_birthday)
                if birthday.validate_birthday(user_birthday):
                    record.birthday = birthday
                    break
                else:
                    print("Birthday invalid.\n"
                          "Birthday should be in the format\n"
                          "'day.month.year' and less than current date.")
                    user_birthday = input("Enter contact Birthday: ")

    def formatting_record(self, record):
        phones = getattr(record, 'phones', '')
        if phones:
            p_l = [phone.value for phone in phones]
            phone_val = p_l
        else:
            phone_val = "Phone number missing."
        email = getattr(record, 'email', '')
        if email:
            email_val = email.value
        else:
            email_val = "Email is missing."
        birthday = getattr(record, 'birthday', '')
        if birthday:
            birthday_val = birthday.value
        else:
            birthday_val = "Date of birth is missing."

        return {"phone": phone_val, "email": email_val,
                "birthday": birthday_val}



class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.startswith('+'):
            raise ValueError
        if len(value) != 13:
            raise ValueError

    def validate_phone(self, phone):
        pattern = r"^[\+]?3?[\s]?8?[\s]?\(?0\d{2}?\)?" \
                  r"[\s]?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}$"
        a = re.match(pattern, phone)
        if a is not None:
            return phone


class Email(Field):

    def validate_email(self, email):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        a = re.match(pattern, email)
        if a is not None:
            return email


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def set_value(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValueError

    def validate_birthday(self, birthday):
        try:
            bt_obj = datetime.strptime(birthday, '%d.%m.%Y')
            if bt_obj.date() >= datetime.now().date():
                return None
            return birthday
        except:
            pass


def main():
    address_book = AddressBook()
    address_book.load_contacts()
    print(Fore.LIGHTBLUE_EX + '-' * 52)
    print('|You can use following commands:\n'
          '|add - Add new contact\n'
          '|find - Find contact in Address Book\n'
          '|show all - Shows the entire Address Book\n'
          '|get bith - Show birthdays\n'
          '|change - Change contact\n'
          '|del - Delete contact from address book\n'
          '|close, exit, good bye or . - Closing the program\n')
    print('-' * 52)
    while True:
        user_inp = input('Enter command: ').lower().strip()
        user_exit_list = ['good bye', 'close', 'exit', '.']
        if user_inp in user_exit_list:
            print('Good bye!\n'
                  'Your data has been successfully saved in the Address Book!')
            break
        elif user_inp == 'hello':
            print('How can I help you?')
            continue
        elif 'add' in user_inp:
            add_contacts(address_book)
        elif 'find' in user_inp:
            find_contacts(address_book)
        elif 'show all' in user_inp:
            show_all_contacts(address_book)
        elif 'get bith' in user_inp:
            birthday_contacts(address_book)
        elif 'change' in user_inp:
            change_contacts(address_book)
        elif 'del' in user_inp:
            remove_contacts(address_book)
        else:
            print('Choose the right command!')
            continue


def add_contacts(address_book):
    user_name = input("Enter contact name: ")
    if not user_name:
        print("Contact name is required")
        return
    else:
        name = Name(user_name)
    record = Record(name)

    user_phone = input("Enter contact phone: ")
    record.create_phone(record=record, user_input=user_phone, update=True)

    user_email = input("Enter contact email: ")
    record.create_email(record=record, user_email=user_email)

    user_birthday = input("Enter contact Birthday: ")
    record.create_birthday(record=record, user_birthday=user_birthday)
    address_book.add_record(record)
    address_book.save_contacts()


def show_all_contacts(address_book):
    data = address_book.show_all_records()
    if not data:
        print('The address book is empty.')
    else:
        for name, record in data.items():
            rec_data = record.formatting_record(record)
            print(f"|Name: {name}, Phone: {rec_data['phone']}, "
                  f"Email: {rec_data['email']}, "
                  f"Birthday: {rec_data['birthday']}|")

def find_contacts(address_book):
    find_user = input('Enter contact name or phone: ')
    data = address_book.show_all_records()
    if not data:
        print('The address book is empty.')
    else:
        flag = False
        for name, record in data.items():
            rec_data = record.formatting_record(record)
            if name.startswith(find_user):
                flag = True
                print(f"Name: {name}, Phone: {rec_data['phone']}, "
                      f"Email: {rec_data['email']}, "
                      f"Birthday: {rec_data['birthday']}")
            phone = getattr(record, 'phone', '')
            if phone:
                if phone.value.startswith(find_user):
                    flag = True
                    print(f"Name: {name}, Phone: {rec_data['phone']}, "
                          f"Email: {rec_data['email']}, "
                          f"Birthday: {rec_data['birthday']}")
        if not flag:
            print('Contact with this name or phone number was not found.')


def birthday_contacts(address_book):
    birth_user = int(input('Enter a number of days: '))
    flag = False
    now = datetime.now().date()
    data = address_book.show_all_records()
    current_date = now + timedelta(days=birth_user)
    for name, record in data.items():
        rec_data = record.formatting_record(record)
        if record.birthday:
            birth = rec_data['birthday']
            new_user_date = datetime.strptime(birth, "%d.%m.%Y").date()
            new_date = datetime(day=new_user_date.day,
                                month=new_user_date.month, 
                                year=now.year).date()
            if new_date >= now and new_date < current_date:
                flag = True
                print(f"Name: {name}, Phone: {rec_data['phone']}, "
                      f"Email: {rec_data['email']}, "
                      f"Birthday: {rec_data['birthday']}")
    if not flag:
        print('There are no birthdays in this range!')


def change_contacts(address_book):
    change_user = input('Enter contact name: ')
    data = address_book.show_all_records()
    if not data:
        print('The address book is empty.')
    else:
        flag = False
        for name, record in data.items():
            rec_data = record.formatting_record(record)
            if name.startswith(change_user):
                flag = True
                print("-"*50)
                print(f"|add phone - press 1|\n"
                      f"|change email - press 2|\n"
                      f"|change birthday - press 3|\n"
                      f"|change name - press 4\n"
                      f"|change phone number - press 5")
                print("-" * 50)
                change = int(input('Enter your choice: '))
                if change == 1:
                    num = input('Enter number: ')
                    record.create_phone(record=record, user_input=num,
                                        update=False)
                    print(f'In contact {name} append '
                          f'{[phone.value for phone in record.phones]}')
                elif change == 2:
                    mail = input('Enter new email: ')
                    record.create_email(record=record, user_email=mail)
                    print(f'In contact {name} change or append email '
                          f'{record.email.value}')
                elif change == 3:
                    birthday = input('Enter new date: ')
                    record.create_birthday(record=record, user_birthday=birthday)
                    print(f'In contact {name} change or append date birthday '
                          f'{record.birthday.value}')
                elif change == 4:
                    new_name = input('Enter new name: ')
                    record.name = Name(new_name)
                elif change == 5:
                    num = input('Enter number: ')
                    record.create_phone(record=record, user_input=num,
                                        update=True)
                    print(f'In contact {name} update '
                          f'{[phone.value for phone in record.phones]}')
                else:
                    print(f'{change} invalid choice')
                    return
        address_book.save_contacts()


def remove_contacts(address_book):
    print('|del - Delete user|\n'
          '|del all - Clean Adress Book|')
    remove_date = input('Enter your choice: ')
    if remove_date == 'del':
        remove_user = input('Enter the name of the contact to be deleted: ')
        address_book.data.pop(remove_user)
        print(f'Contact {remove_user} deleted.')
    elif remove_date == 'del all':
        print(f'Are you sure you want to clear the Address Book?')
        question = input('Y or N: ').lower().strip()
        if question == 'n':
            print('non')
            return
        elif question == 'y':
            print('lol')
            address_book.data.clear()
    address_book.save_contacts()


if __name__ == "__main__":
    main()

