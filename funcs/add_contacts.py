import db_api
import csv


async def add_contacts():
    await db_api.del_contacts()
    with open("fixtures/contacts.csv", encoding='utf-8') as contacts:
        reader = csv.reader(contacts, delimiter=",")
        for contact in reader:
            print(contact)
            await db_api.add_contact(int(contact[0]), contact[1], contact[2], contact[3], contact[4], contact[5],
                                     contact[6])
