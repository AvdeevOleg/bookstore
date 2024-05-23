import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Publisher, Book, Shop, Stock, Sale, Base

load_dotenv()


def get_db_session():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine


def load_data(session, data):
    publishers = {p['name']: Publisher(name=p['name']) for p in data['publishers']}
    session.add_all(publishers.values())
    session.commit()

    books = {b['title']: Book(title=b['title'], id_publisher=publishers[b['id_publisher']].id) for b in data['books']}
    session.add_all(books.values())
    session.commit()

    shops = {s['name']: Shop(name=s['name']) for s in data['shops']}
    session.add_all(shops.values())
    session.commit()

    stocks = [Stock(id_book=books[s['id_book']].id, id_shop=shops[s['id_shop']].id, count=s['count']) for s in
              data['stocks']]
    session.add_all(stocks)
    session.commit()

    sales = [Sale(price=s['price'], date_sale=datetime.strptime(s['date_sale'], '%Y-%m-%d'),
                  id_stock=stocks[s['id_stock'] - 1].id, count=s['count']) for s in data['sales']]
    session.add_all(sales)
    session.commit()


def main():
    session, engine = get_db_session()

    Base.metadata.create_all(engine)

    with open('fixtures/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    load_data(session, data)


if __name__ == "__main__":
    main()
