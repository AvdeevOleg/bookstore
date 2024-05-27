import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Publisher, Book, Shop, Stock, Sale

load_dotenv()

def get_db_session():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

def get_shops(publisher_info):
    session = get_db_session()

    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale, Sale.id_stock == Stock.id)

    if publisher_info.isdigit():
        results = query.filter(Publisher.id == int(publisher_info)).all()
    else:
        results = query.filter(Publisher.name == publisher_info).all()

    for title, shop_name, price, date_sale in results:
        print(f"{title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == "__main__":
    publisher_info = input("Введите имя или ID издателя: ")
    get_shops(publisher_info)

