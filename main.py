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


def main():
    session = get_db_session()

    publisher_name = input("Введите имя издателя: ")

    results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
        join(Book, Book.id == Stock.id_book). \
        join(Shop, Shop.id == Stock.id_shop). \
        join(Sale, Sale.id_stock == Stock.id). \
        join(Publisher, Publisher.id == Book.id_publisher). \
        filter(Publisher.name == publisher_name). \
        all()

    for title, shop_name, price, date_sale in results:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    main()
