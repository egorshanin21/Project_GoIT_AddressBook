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

    def add_phone(self, phone):
        self.phones.append(phone)
        print(self.phones)

    def formatting_record(self, record):

        phone = getattr(record, 'phone', '')
        if phone:
            phone_val = phone.value
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

        return {"phone": phone_val, "email": email_val, "birthday": birthday_val}

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now().date()
            bday2 = self.birthday.value.split('.')
            b = datetime(year=now.year, month=int(bday2[1]),day=int(bday2[0])).date()
            next = b - now
            if next.days < 0:
                b = datetime(year=now.year + 1, month=int(bday2[1]),
                             day=int(bday2[0])).date()
                print(b - now)
            else:
                next = b - now
                print(next)


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
        pattern = r"^[\+]?3?[\s]?8?[\s]?\(?0\d{2}?\)?[\s]?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}$"
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
    while True:
        print(Fore.LIGHTBLUE_EX +'__________________________________________________\n'
              'You can use following commands:\n'
              '|add| - Add new contact\n'
              '|find| - Find contact in Address Book\n'
              '|show all| - Shows the entire Address Book\n'
              '|get bith| - Show birthdays\n'
              '|close, exit, good bye or .| - Closing the program\n'
              '__________________________________________________\n')
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
            add_handler(address_book)
        elif 'find' in user_inp:
            find_handler(address_book)
        elif 'show all' in user_inp:
            show_all_handler(address_book)
        elif 'get bith' in user_inp:
            birthday_handler(address_book)
        else:
            print('Choose the right command!')
            continue


def add_handler(address_book):
    user_name = input("Enter contact name: ")
    if not user_name:
        print("Contact name is required")
        return
    else:
        name = Name(user_name)
    record = Record(name)

    user_phone = input("Enter contact phone: ")
    if user_phone:
        for i in range(10):
            phone = Phone(user_phone)
            if phone.validate_phone(user_phone):
                record.phone = phone
                break
            else:
                print("Incorrect phone number format entered. Enter your phone in the format '+380991122333'")
                user_phone = input("Enter contact phone: ")

    user_email = input("Enter contact email: ")
    if user_email:
        for i in range(10):
            email = Email(user_email)
            if email.validate_email(user_email):
                record.email = email
                break
            else:
                print("Email entered incorrectly. Please enter a valid email: 'example@gmail.com'")
                user_email = input("Enter contact email: ")

    user_birthday = input("Enter contact Birthday: ")
    if user_birthday:
        for i in range(10):
            birthday = Birthday(user_birthday)
            if birthday.validate_birthday(user_birthday):
                record.birthday = birthday
                break
            else:
                print("Birthday invalid. Birthday should be in the format 'day.month.year' and less than current date.")
                user_birthday = input("Enter contact Birthday: ")
    address_book.add_record(record)
    address_book.save_contacts()


def show_all_handler(address_book):
    data = address_book.show_all_records()
    if not data:
        print('The address book is empty.')
    else:
        for name, record in data.items():
            rec_data = record.formatting_record(record)
            print(f"|Name: {name}, Phone: {rec_data['phone']}, Email: {rec_data['email']}, Birthday: {rec_data['birthday']}|")


def find_handler(address_book):
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
                print(f"Name: {name}, Phone: {rec_data['phone']}, Email: {rec_data['email']}, Birthday: {rec_data['birthday']}")
            phone = getattr(record, 'phone', '')
            if phone:
                if phone.value.startswith(find_user):
                    flag = True
                    print(f"Name: {name}, Phone: {rec_data['phone']}, Email: {rec_data['email']}, Birthday: {rec_data['birthday']}")
        if not flag:
            print('Contact with this name or phone number was not found.')

def birthday_handler(address_book):
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
            n_d = datetime(day=new_user_date.day, month=new_user_date.month, year=now.year).date()
            if n_d >= now and n_d < current_date:
                flag = True
                print(f"Name: {name}, Phone: {rec_data['phone']}, Email: {rec_data['email']}, Birthday: {rec_data['birthday']}")
    if not flag:
        print('There are no birthdays in this range!')





if __name__ == "__main__":
    main()

