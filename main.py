from datetime import datetime, UTC
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request"},
    )


DATABASE_URL = "postgresql+psycopg://postgres:dev@localhost:5433/postgres"

engine = create_engine(DATABASE_URL, echo=True)

class WorkOrderBase(SQLModel):
    title: str
    status: str


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrder(WorkOrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/work-orders", response_model=WorkOrder)
def create_work_order(work_order: WorkOrderCreate):
    db_work_order = WorkOrder.model_validate(work_order)

    with Session(engine) as session:
        session.add(db_work_order)
        session.commit()
        session.refresh(db_work_order)
        return db_work_order


@app.get("/work-orders/{work_order_id}", response_model=WorkOrder)
def get_work_order(work_order_id: int):
    with Session(engine) as session:
        work_order = session.get(WorkOrder, work_order_id)

        if not work_order:
            raise HTTPException(status_code=404, detail="Work order not found")

        return work_order
