import csv
from structures import contact


class contact_file_manager:

    def to_csv(file_path, contacts: dict[str, contact]) -> list[dict]:
        if not file_path.endswith(".csv"):
            raise ValueError("Invalid file format. Please provide a CSV file.")
        
        with open(file_path, mode="w") as csv_file:
            csv_writer = csv.DictWriter(csv_file)
            for contact_id, user_contact in contacts.items():
                csv_writer.writerow({
                    "Contact ID": user_contact.contact_id,
                    "First Name": user_contact.first_name,
                    "Middle Name": user_contact.middle_name,
                    "Last Name": user_contact.last_name,
                    "Birth Date": user_contact.birth_date,
                    "Gender": user_contact.gender,
                    "Contact Number": user_contact.contact_number,
                    "Email Address": user_contact.email_address,
                })
            

    def from_csv(file_path) -> list[dict]:

        if not file_path.endswith(".csv"):
            raise ValueError("Invalid file format. Please provide a CSV file.")

        contacts: list[dict] = []

        with open(file_path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                contact_id = row["Contact ID"]
                first_name = row["First Name"]
                middle_name = row["Middle Name"]
                last_name = row["Last Name"]
                birth_date = row["Birth Date"]
                gender = row["Gender"]

                contact_number = row["Contact Number"]
                email_address = row["Email Address"]

                contact = {
                    "contact_id": contact_id,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "birth_date": birth_date,
                    "gender": gender,
                    "contact_number": contact_number,
                    "email_address": email_address,
                }

                contacts.append(contact)

        return contacts

    def from_vcf(file_path) -> list[dict]:
        raise NotImplementedError("This function is not yet implemented.")


if __name__ == "__main__":
    print("This is a module. Import this module to use its functions.")
