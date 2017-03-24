from model import *
from datetime import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

session.query(Business).delete()
session.query(Owner).delete()

example_owner=Owner(
	name="Potato Amigo",
	phone='049324234',
	email='potato.amigo@gmail.com',
	dob=date(2000,7,21),
	city='Tivon',
	address='Haemek 11a',
	zipcode='36699')

session.add(example_owner)
session.commit()

example_business_password='Business_Password_123'
for i in xrange(1,10):
	example_business= Business(
		name="Falafel "+str(i),
		phone='052423545',
		email=str(i),
		city='Haifa',
		address='Hashalom 13',
		zipcode='12345',
		category='food',
		owner_id=1)

	example_business.hash_password(example_business_password)



	session.add(example_business)
session.commit()