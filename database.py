from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///Data.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))

def commit_and_close(session):
    session.commit()
    session.close()

def rollback_and_close(session):
    session.rollback()
    session.close()

def add_User(username,phone,address, password,cash):
    try:
        user_object = User(username=username,phone=phone,address=address,
        password=password,cash=round(cash,2))
        session.add(user_object)
        commit_and_close(session)
    except:
        rollback_and_close(session)
        raise

def add_Farm(Farm_name,bank_name,bank_account,phone,address,password):
    try:
        Farm_object = Farm(Farm_name=Farm_name,bank_name=bank_name,bank_account=bank_account,phone=phone,address=address,password=password)
        session.add(Farm_object)
        commit_and_close(session)
    except:
        rollback_and_close(session)
        raise    

def add_Product(Type,Owner,cost):
  try:
    product_object = Product(Type=Type,Owner=Owner,cost=round(cost,2))
    session.add(product_object)
    commit_and_close(session)
  except:
    rollback_and_close(session)
    raise

def query_product_by_id(id):
   cursor = session.query(
       Product).filter_by(
       id_table=id).first() 
   session.close()
   return cursor


def update_cost_product_by_id(id):
    product = session.query(
       Product).filter_by(
       id_table=id).first()
    product.cost = 0
    commit_and_close(session)

def update_cash_user_by_username(username,cost):
    user = session.query(
       User).filter_by(
       username=username).first()
    user.cash -= cost
    commit_and_close(session)

def query_user_by_username(username):
    a=session.query(User)
    b= a.filter_by(username=username)
    c=b.first()
    session.close()
    return c

def query_by_farmname(farmname):
    result = session.query(Farm).filter_by(Farm_name = farmname).first()
    session.close()
    return result

def delete_product_by_id(id):
    product = session.query(Product).filter_by(id_table=id).delete()
    commit_and_close(session)

def buy_product(username,product_id):
    user_cash = query_user_by_username(username).cash
    product_cost = query_product_by_id(product_id).cost

    if user_cash == product_cost or user_cash > product_cost:
        update_cash_user_by_username(username,product_cost)
        delete_product_by_id(product_id)
        return "bought"
    else:
        return "not enough cash"

def get_all_products():
    result = session.query(Product).all()
    session.close()
    return result


def get_owner_products(Owner):
    return session.query(Product).filter_by(Owner=Owner).all()


def get_all_users():
    return session.query(User).all()

def get_all_farms():
    result = session.query(Farm).all()
    session.close()
    return result

def query_by_username_and_password(username, password):
    result = session.query(User).filter_by(username = username, password = password).first()
    session.close()
    return result

def query_by_farmname_and_password(farmname, password):
    result = session.query(Farm).filter_by(Farm_name = farmname, password = password).first()
    session.close()
    return result

def delete_all_users():
    session.query(User).delete()
    commit_and_close(session)

def delete_all_products():
    session.query(Product).delete()
    commit_and_close(session)

##########################################################################

def get_all_Types():
    result = session.query(Type).all()
    session.close()
    return result

def query_type_by_name(Name):
   result = session.query(Type).filter_by(Name=Name).first()
   session.close()
   return result

def get_minPrice(Name):
  result = session.query(Type).filter_by(Name=Name).first().Min_price
  session.close()
  return result

def get_maxPrice(Name):
  result = session.query(Type).filter_by(Name=Name).first().Max_price
  session.close()
  return result

def set_minPrice(Name,newMinPrice):
  res = session.query(
       Type).filter_by(
       Name=Name).first()
  res.Min_price = newMinPrice
  commit_and_close(session)

def set_maxPrice(Name,newMaxPrice):
  res = session.query(
       Type).filter_by(
       Name=Name).first()
  res.Max_price = newMaxPrice
  commit_and_close(session)

def add_type(Name,img,min_price, max_price):
  try:
    product_object = Type(Name=Name,Img=img,Min_price=min_price, Max_price=max_price)
    session.add(product_object)
    commit_and_close(session)
  except:
    rollback_and_close(session)
    raise

def get_type_products_lowestPrice(Type):
    number = 0
    res = session.query(Product).filter_by(Type=Type).all()
    if res != []:
      number = res[0].cost
    for product in res:
      if product.cost < number:
        number = product.cost
    session.close()
    return number

def get_type_products_highestPrice(Type):
    number = 0
    res = session.query(Product).filter_by(Type=Type).all()
    if res != []:
      number = res[0].cost
    for product in res:
      if product.cost > number:
        number = product.cost
    session.close()
    return number

def get_type_products(Type):
  result = session.query(Product).filter_by(Type=Type).all()
  session.close
  return result

def query_product_by_id(id):
   result = session.query(
       Product).filter_by(
       id_table=id).first()  
   session.close()
   return result

def update_min_max_types():
    types = session.query(Type).all()
    for item in types:
      item.Min_price = get_type_products_lowestPrice(item.Name)
      item.Max_price = get_type_products_highestPrice(item.Name)
