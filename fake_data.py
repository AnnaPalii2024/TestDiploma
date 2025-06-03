import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestDiploma.settings')
django.setup()

def populate_db(RentHouseFactory=None):
    from rent.rent_factory import RentHouseFactory

    RentHouseFactory.create_batch(3, role='tenant')
    RentHouseFactory.create_batch(3, role='landlord')
    print("Created 10 rent houses")

if __name__ == "__main__":
    populate_db()