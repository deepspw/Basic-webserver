# To use simply import into your python shell
from sqlalchemy import create_engine # create engine is used to speak to the database through python
from sqlalchemy.orm import sessionmaker # imports the ability to create sessions in order to commit and save data
from database_setup import Base, Restaurant, MenuItem # imports my classes from database_setup

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()