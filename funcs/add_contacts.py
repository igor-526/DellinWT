import db_api

async def add_contacts():
    with open('contacts.txt', 'r') as file:
        for line in file.readlines():
            contact = line.strip('\n').split(' ')
            await db_api.add_contact(contact[0], contact[2], contact[1], contact[3], contact[4], contact[5])