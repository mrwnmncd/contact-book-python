from file_parser import contact_file_manager
from structures import contact, ContactManagerError


class contact_manager:
    __contacts_store_file_path: str
    __contacts: dict[str, contact]

    def __init__(this):
        this.__contacts = {}

    def load_contacts(this, file_path: str):
        this.__contacts_store_file_path = file_path
        contact_store = contact_file_manager.from_csv(this.__contacts_store_file_path)
        for entry in contact_store:
            contact_information = this.__contacts[entry["contact_id"]] = contact()
            contact_information.contact_id = entry["contact_id"]
            contact_information.first_name = entry["first_name"]
            contact_information.middle_name = entry["middle_name"]
            contact_information.last_name = entry["last_name"]
            contact_information.birth_date = entry["birth_date"]
            contact_information.gender = entry["gender"]
            contact_information.contact_number = entry["contact_number"]
            contact_information.email_address = entry["email_address"]

    def search_contact(this, generic_search, **search): # -> contact | None:
        if generic_search or (
            search.get("contact_id")
            or search.get("first_name")
            or search.get("last_name")
        ):
            for contact_id, contact_information in this.__contacts.items():
                if (
                    generic_search.lower() == contact_id
                    or search.get("contact_id", "").lower() == contact_id
                    or generic_search.lower()
                    == contact_information.contact_number.lower()
                    or generic_search.lower()
                    == contact_information.email_address.lower()
                    or generic_search.lower() == contact_information.first_name.lower()
                    or generic_search.lower() == contact_information.last_name.lower()
                    or search.get("contact_number", "").lower()
                    == contact_information.contact_number.lower()
                    or search.get("email_address", "").lower()
                    == contact_information.email_address.lower()
                    or search.get("first_name", "").lower()
                    == contact_information.first_name.lower()
                    or search.get("last_name", "").lower()
                    == contact_information.last_name.lower()
                ):
                    return contact_information
        else:
            raise ValueError(
                "Please provide a valid search criteria. Search with contact_id, first_name, or last_name."
            )

        return None

    def add_contact(this, contact_information: contact):
        retreived_contact = this.__contacts.get(contact_information.contact_id, None)
        if retreived_contact is not None:
            raise ContactManagerError(
                f"Contact of ID {contact_information} already exists!"
            )
        this.__contacts[contact_information.contact_id] = contact_information

    def update_contact(this, contact_id: str, contact_information: contact):
        retreived_contact = this.__contacts.get(contact_id, None)
        if retreived_contact is None:
            raise ContactManagerError(f"Contact of ID {contact_id} does not exist!")
        this.__contacts[contact_id] = contact_information
        contact_file_manager.to_csv(this.__contacts_store_file_path, this.__contacts)


    def delete_contact(this, contact_id: str) -> bool:
        retreived_contact = this.__contacts.get(contact_id, None)
        if retreived_contact is None:
            raise ContactManagerError(f"Contact of ID {contact_id} does not exist!")
        del this.__contacts[contact_id]
        contact_file_manager.to_csv(this.__contacts_store_file_path, this.__contacts)
        return True