from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Item, Category

engine = create_engine('sqlite:///itemCatalogs.db')

Base.metadata.bind = engine
database_session = sessionmaker(bind=engine)
session = database_session()

dumb_user = User(username="admin", email="anything8@yahoo.com",
                 picture='https://pbs.twimg.com/profile_images\
                 /2671170543/18debd694829ed78203a5a36dd364160_400x400.png')

session.add(dumb_user)
session.commit()

# category 1
category1 = Category(user_id=1, name='Vegetables')
session.add(category1)
session.commit()

item1Category1 = Item(user_id=1, name='carrots',
                      description='this is a species from vegetables',
                      category=category1)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='Asparagus',
                      description='this is a species from vegetables',
                      category=category1)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='Cardoon',
                      description='this is a species from vegetables',
                      category=category1)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='Celeriac',
                      description='this is a species from vegetables',
                      category=category1)
session.add(item4Category1)
session.commit()

#############################################################
# category 2
category2 = Category(user_id=1, name='fish')
session.add(category2)
session.commit()

item1Category1 = Item(user_id=1, name='African glass catfish',
                      description='this is a species from fishs',
                      category=category2)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='Asparagus',
                      description='this is a species from fishs',
                      category=category2)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='Bolty',
                      description='this is a species from fishs',
                      category=category2)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='Celeriac',
                      description='this is a species from fishs',
                      category=category2)
session.add(item4Category1)
session.commit()

#######################################################
# category 3
category3 = Category(user_id=1, name='market')
session.add(category3)
session.commit()

item1Category1 = Item(user_id=1, name='Perfect Competition',
                      description='this is a species from market',
                      category=category3)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='Monopolistic Competition',
                      description='this is a species from market',
                      category=category3)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='Oligopoly',
                      description='this is a species from market',
                      category=category3)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='Monopoly',
                      description='this is a species from market',
                      category=category3)
session.add(item4Category1)
session.commit()

##################################################################
# category 4
category4 = Category(user_id=1, name='sports')
session.add(category4)
session.commit()

item1Category1 = Item(user_id=1, name='Archery',
                      description='this is a species from sports',
                      category=category4)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='Athletics',
                      description='this is a species from sports',
                      category=category4)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='Bobsleigh',
                      description='this is a species from sports',
                      category=category4)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='Boxing',
                      description='this is a species from sports',
                      category=category4)
session.add(item4Category1)
session.commit()

###########################################################################
# category 5
category5 = Category(user_id=1, name='phones')
session.add(category5)
session.commit()

item1Category1 = Item(user_id=1, name='sony',
                      description='this is a species from phones',
                      category=category5)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='samsung',
                      description='this is a species from phones',
                      category=category5)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='iphone',
                      description='this is a species from phones',
                      category=category5)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='huwawei',
                      description='this is a species from phones',
                      category=category5)
session.add(item4Category1)
session.commit()

########################################################################
# category 6
category6 = Category(user_id=1, name='TVs')
session.add(category6)
session.commit()

item1Category1 = Item(user_id=1, name='sony',
                      description='this is a species from TVs',
                      category=category6)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='samsung',
                      description='this is a species from TVs',
                      category=category6)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='qompaq',
                      description='this is a species from TVs',
                      category=category6)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='dell',
                      description='this is a species from TVs',
                      category=category6)
session.add(item4Category1)
session.commit()

###############################################################
# category 7
category7 = Category(user_id=1, name='Laptops')
session.add(category7)
session.commit()

item1Category1 = Item(user_id=1, name='dell',
                      description='this is a species from Laptops',
                      category=category7)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='lenovo',
                      description='this is a species from Laptops',
                      category=category7)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='sony',
                      description='this is a species from Laptops',
                      category=category7)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='accer',
                      description='this is a species from Laptops',
                      category=category7)
session.add(item4Category1)
session.commit()

##############################################################
# category 8
category8 = Category(user_id=1, name='schools')
session.add(category8)
session.commit()

item1Category1 = Item(user_id=1, name='secondary',
                      description='this is a species from schools',
                      category=category8)
session.add(item1Category1)
session.commit()

item2Category1 = Item(user_id=1, name='primary',
                      description='this is a species from schools',
                      category=category8)
session.add(item2Category1)
session.commit()

item3Category1 = Item(user_id=1, name='quadratic',
                      description='this is a species from schools',
                      category=category8)
session.add(item3Category1)
session.commit()

item4Category1 = Item(user_id=1, name='high school',
                      description='this is a species from schools',
                      category=category8)
session.add(item4Category1)
session.commit()


print("added Successfully")