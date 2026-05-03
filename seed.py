# №9.1

from app.database import SessionLocal
from app.models import Product


def seed():
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            db.add_all([
                Product(title="Laptop", price=999.99, count=10, description="High-performance laptop"),
                Product(title="Mouse", price=29.99, count=50, description="Wireless mouse"),
            ])
            db.commit()
            print("Seeded 2 products.")
        else:
            print("Products already exist, skipping seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
