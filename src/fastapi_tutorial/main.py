from fastapi import FastAPI, Depends
from .models import Product
from .database import session, engine
from . import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return "OK"

products = [
    Product(id=1, name="Laptop", description="High-performance laptop with 16GB RAM", price=75000.0, quantity=25),
    Product(id=2, name="Wireless Mouse", description="Ergonomic wireless mouse with USB receiver", price=799.0, quantity=100),
    Product(id=3, name="Mechanical Keyboard", description="RGB mechanical keyboard with blue switches", price=2499.0, quantity=50),
    Product(id=4, name="Monitor", description="27-inch Full HD IPS monitor", price=12500.0, quantity=30),
    Product(id=5, name="Headphones", description="Wireless noise-cancelling headphones", price=3999.0, quantity=75),
]

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        try:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
        finally:
            db.close()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    try:
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
        return product
    except:
        return "Something went wrong"

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "product udpated"
    else:
        return "Product not found"

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    else:
        return "Product not found"