from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductOut,
    ErrorResponse,
    UserValidation,
    UserIn,
    UserOut,
)
from app.exceptions import (
    CustomExceptionA,
    CustomExceptionB,
    handle_custom_exception_a,
    handle_custom_exception_b,
)

app = FastAPI(title="Контрольная работа №4")

# №10.1
app.add_exception_handler(CustomExceptionA, handle_custom_exception_a)
app.add_exception_handler(CustomExceptionB, handle_custom_exception_b)


# №10.2
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "error_code": 422,
            "message": "Validation error",
            "details": errors,
        },
    )


# №9.1

@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# №10.1

@app.get("/check-condition/{value}")
def check_condition(value: int):
    if value <= 0:
        raise CustomExceptionA(detail=f"Value must be positive, got {value}")
    return {"status": "ok", "value": value}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    items = {1: "Item A", 2: "Item B", 3: "Item C"}
    if item_id not in items:
        raise CustomExceptionB(detail=f"Item with id={item_id} not found")
    return {"item_id": item_id, "name": items[item_id]}


# №10.2

@app.post("/validate-user")
def validate_user(user: UserValidation):
    return {"status": "ok", "user": user.model_dump()}


# №11.1 / №11.2

db_users: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    db_users[user_id] = user.model_dump()
    return {"id": user_id, **db_users[user_id]}


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db_users[user_id]}


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db_users.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
