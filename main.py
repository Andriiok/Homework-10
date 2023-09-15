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
        self.validate(self.value)

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
        phone_found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                phone_found = True
                break

        if not phone_found:
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

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

def main():
    print("How can I help you?")

    book = AddressBook()

    while True:
        command = input().strip().lower()
        
        if command == "good bye" or command == "close" or command == "exit":
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, *fields = command.split()
                record = Record(name)
                for field in fields:
                    field_name, field_value = field.split(":")
                    record.add_field(field_name, field_value)
                book.add_record(record)
                print(f"Added contact: {name}")
            except ValueError:
                print("Give me name and fields please")
            except IndexError:
                print("Invalid command format")
        elif command.startswith("change"):
            try:
                _, name, field_name, new_value = command.split()
                record = book.find(name)
                if record:
                    record.edit_field(field_name, new_value)
                    print(f"Changed {field_name} for {name} to {new_value}")
                else:
                    print(f"Contact {name} not found")
            except ValueError:
                print("Give me name, field name, and new value please")
            except IndexError:
                print("Invalid command format")
        elif command.startswith("delete"):
            try:
                _, name, field_name = command.split()
                record = book.find(name)
                if record:
                    record.remove_field(field_name)
                    print(f"Deleted {field_name} for {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError:
                print("Give me name and field name please")
            except IndexError:
                print("Invalid command format")
        elif command.startswith("find"):
            try:
                _, name, field_name = command.split()
                record = book.find(name)
                if record:
                    found_field = record.find_field(field_name)
                    if found_field:
                        print(f"{name}'s {field_name}: {found_field}")
                    else:
                        print(f"{field_name} not found for {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError:
                print("Give me name and field name please")
            except IndexError:
                print("Invalid command format")
        elif command == "show all":
            if book:
                for name, record in book.data.items():
                    print(record)
            else:
                print("No contacts found")
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
