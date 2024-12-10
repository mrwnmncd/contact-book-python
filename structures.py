
import uuid


class ContactManagerError(Exception): 
    class ContactExistsError(Exception): ...
    class ContactNotExistsError(Exception): ...

class vcard:
    N: str
    FN: str
    ORG: str
    TITLE: str
    TEL: str
    EMAIL: str
    ADR: str
    URL: str
    BDAY: str
    NOTE: str
    REV: str
    UID: str
    
    def __init__(this):
        pass

class contact:
    contact_id: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    birth_date: str  = ""
    gender: str = ""
    contact_number: str = ""
    email_address: str = ""

    def __init__(this, **kwargs):
        this.contact_id = kwargs.get('contact_id')
        this.first_name = kwargs.get('first_name')
        this.middle_name = kwargs.get('middle_name')
        this.last_name = kwargs.get('last_name')
        this.birth_date = kwargs.get('birth_date')
        this.gender = kwargs.get('gender')
        this.contact_number = kwargs.get('contact_number')
        this.email_address = kwargs.get('email')

    def assign_id(this):
        this.contact_id = str(uuid.uuid4())

    def __str__(self) -> str:
        string_value = ""
        string_value += f"Contact ID: {self.contact_id}\n"
        string_value += f"First Name: {self.first_name}\n"
        string_value += f"Middle Name: {self.middle_name}\n"
        string_value += f"Last Name: {self.last_name}\n"
        string_value += f"Birth Date: {self.birth_date}\n"
        string_value += f"Gender: {self.gender}\n"
        string_value += f"Contact Number: {self.contact_number}\n"
        string_value += f"Email Address: {self.email_address}\n"
        return string_value

    def validate(self):
        if not self.first_name or self.first_name.strip() == "":
            raise ContactManagerError("First name is required.")
        if not self.last_name or self.last_name.strip() == "":
            raise ContactManagerError("Last name is required.")
        if not self.contact_number or self.contact_number.strip() == "":
            raise ContactManagerError("Contact number is required.")
        if not self.email_address or self.email_address.strip() == "":
            raise ContactManagerError("Email address is required.")