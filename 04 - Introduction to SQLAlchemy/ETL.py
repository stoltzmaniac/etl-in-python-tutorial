from os import listdir
import sys
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from utils import read_clean_data
from test_data import test_data_integrity
from models import Base, Status, Country, Orders


# Check to see if new data passes tests, abort script if not
# Assuming you get a single new file placed into "new_data" directory
new_filename = 'new_data/' + listdir('new_data')[0]
new_data = read_clean_data(new_filename)
integrity_test = test_data_integrity(new_data)
if not integrity_test:
    sys.exit("[ERROR] - ETL Aborted - New data did not pass integrity tests!")


# Create a connection to the database - if this does not exist, one is created (for SQLite)
database_location = "sqlite:///my_sales_db.sqlite"
print(f"Creating a connection to the database: {database_location}")
engine = sqlalchemy.create_engine(database_location)

# Create / Build Schema
Base.metadata.create_all(engine)

# Access data via a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data iteratively, begin by filling out the dimension tables
for status_ in list(new_data['STATUS'].unique()):
    status = Status(status=status_)
    session.add(status)
session.commit()

for country_ in list(new_data['COUNTRY'].unique()):
    country = Country(country=country_)
    session.add(country)
session.commit()

for order_ in new_data.to_dict(orient='records'):
    status = session.query(Status).filter(Status.status == order_['STATUS']).first()
    country = session.query(Country).filter(Country.country == order_['COUNTRY']).first()
    order = Orders(
        order_number=order_['ORDERNUMBER'],
        order_line_number=order_['ORDERLINENUMBER'],
        quantity_ordered=order_['QUANTITYORDERED'],
        price_each=order_['PRICEEACH'],
        sales=order_['SALES'],
        status=status,
        country=country)
    session.add(order)
session.commit()