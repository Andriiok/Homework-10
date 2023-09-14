from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @staticmethod
    def validate(value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Phone number must contain 10 digits.")

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                found = True
                break

        if not found:
            raise ValueError(f"Phone number {old_phone} not found in the record")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("How can I help you?")

    while True:
        command = input().strip().lower()

        if command == "good bye" or command == "close" or command == "exit":
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Added contact: {name}, {phone}")
        elif command.startswith("change"):
            _, name, phone = command.split()
            try:
                record = book.find(name)
                record.edit_phone(record.phones[0].value, phone)
                print(f"Changed phone for {name} to {phone}")
            except ValueError as e:
                print(e)
        elif command.startswith("phone"):
            _, name = command.split()
            try:
                record = book.find(name)
                print(f"Phone number for {name}: {record.phones[0]}")
            except ValueError as e:
                print(e)
        elif command == "show all":
            if book.data:
                for record in book.data.values():
                    print(record)
            else:
                print("No contacts found")
        else:
            print("Invalid command. Try again.")
















