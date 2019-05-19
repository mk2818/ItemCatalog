from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Category, Item


engine = create_engine('sqlite:///categoryitem.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Fake Data elements
#
# category = []
# category = [
#   {'id'   : 1,
#    'name' : 'Soccer',
#    'Item' : [{'cat_id'      : 1,
#               'description' : 'The shoes',
#               'id'          : 1,
#               'title'       : 'Socker cleats'},
#              {'cat_id'      : 1,
#               'description' :'The shirt',
#               'id'          : 2,
#               'title'       : 'Jersey'}]
#   }
# ]
# category = [
#   {'id'   : 1,
#    'name' : 'Soccer',
#    'Item' : [{'cat_id'      : 1,
#               'description' : 'The shoes',
#               'id'          : 1,
#               'title'       : 'Soccer cleats'},
#              {'cat_id'      : 1,
#               'description' : 'The shirt',
#               'id'          : 2,
#               'title'       : 'Jersey'}]
#   },
#   {'id'   : 2,
#    'name' : 'Basketball'
#   },
#   {'id'   : 3,
#    'name' : 'Baseball',
#    'Item' : [{'cat_id'      : 3,
#               'description' : 'The bat',
#               'id'          : 3,
#               'title'       : 'Bat'}]
#   },
#   {'id'   : 4,
#    'name' : 'Frisbee'
#   },
#   {'id'   : 5,
#    'name' : 'Snowboarding',
#    'Item' : [{'cat_id'      : 5,
#               'description' :
#    'Best for any terrain and conditions. All-mountain snowboards perform '
#    'anywhere on a mountain/u2014groomed runs, backcountry, even park and '
#    'pipe. They may be directional (meaning downhill only) or twin-tip (for '
#    'riding switch, meaning either direction). Most boarders ride all-'
#    'mountain boards. Because of the versatility, all-mountain boards are '
#    'good for beginners who are still learning what terrain they like.',
#               'id'          : 7,
#               'title'       : 'Snowboard'}]
#   },
#   {'id'   : 8,
#    'name' : 'Rock Climbing'
#   }
# ]

# Fake Items
# items = []
# items = [{'cat_id'      : 1,
#           'description' : 'The shoes',
#           'id'          : 1,
#           'title'       : 'Soccer cleats'
#          }
#         ]
# items = [{'cat_id'      : 1,
#           'description' : 'The shoes',
#           'id'          : 1,
#           'title'       : 'Socker cleats'
#          },
#          {'cat_id'      : 1,
#           'description' : 'The shirt',
#           'id'          : 2,
#           'title'       : 'Jersey'
#          }
#         ]

""""
  ***************
  * Table: User *
  ***************
"""


# Create dummy user
# picture='https://pbs.twimg.com/profile_images/
#          2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='')
session.add(user1)
session.commit()

""""
  *******************
  * Table: Category *
  *******************
"""


# {'id':'1', 'name':'Soccer'}
category1 = Category(id='1', name="Soccer", user_id='1')
session.add(category1)
session.commit()

# {'id':'2', 'name':'Basketball'}
category2 = Category(id='2', name='Basketball', user_id='1')
session.add(category2)
session.commit()

# {'id':'3', 'name':'Baseball'},
category3 = Category(id='3', name="Baseball", user_id='1')
session.add(category3)
session.commit()


#  {'id':'4', 'name':'Frisbee'}
category4 = Category(id='4', name="Frisbee", user_id='1')
session.add(category4)
session.commit()


#   {'id':'5', 'name':'Snowboarding'}
category5 = Category(id='5', name="Snowboarding", user_id='1')
session.add(category5)
session.commit()


#   {'id':'6', 'name':'Rock Climbing'}
category6 = Category(id='6', name="Rock Climbing", user_id='1')
session.add(category6)
session.commit()


""""
  ****************
  * Table: Items *
  ****************
"""


# Item for Soccer
# {'id':'1', 'cat_id':'1', description':'The shoes', 'title':'Soccer cleats'}
item1 = Item(id='1',
             category_id='1',
             title='Soccer cleats',
             description='The shoes',
             user_id='1')
session.add(item1)
session.commit()

# Item for Soccer
# {'id':'2','cat_id':1, description':'The shirt', 'id':'2', 'title':'Jersey'}
item2 = Item(id='2',
             category_id='1',
             title='Jersey',
             description='The shirt',
             user_id='1')
session.add(item2)
session.commit()

# Item for Baseball
# {'id':'3','cat_id':3, description':'The bat', 'title':'Bat'}
item3 = Item(id='3',
             category_id='3',
             title='Bat',
             description='The bat',
             user_id='1')
session.add(item3)
session.commit()


# 'Item':['id': '4', 'cat_id':5, 'description':
#     'Best for any terrain and conditions. All-mountain snowboards perform '
#     'anywhere on a mountain/u2014groomed runs, backcountry, even park and '
#     'pipe. They may be directional (meaning downhill only) or twin-tip (for '
#     'riding switch, meaning either direction). Most boarders ride all-'
#     'mountain boards. Because of the versatility, all-mountain boards are '
#     'good for beginners who are still learning what terrain they like.',
#     'title':'Snowboard'}] },]
item4 = Item(id='4',
             category_id='5',
             title='Snowboard',
             description='Best for any terrain and conditions. All-mountain '
                         'snowboards perform anywhere on a mountain-groomed '
                         'run, backcountry, even park and pipe. They may be '
                         'directional (meaning downhill only) or twin-tip '
                         '(for riding switch, meaning either direction). '
                         'Most boarders ride all-mountain boards. Because of '
                         'the versatility, all-mountain boards are good for '
                         'beginners who are still learning what terrain they '
                         'like.',
             user_id='1')
session.add(item4)
session.commit()

print "added categories and items!"
