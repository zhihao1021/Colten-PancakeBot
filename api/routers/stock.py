from fastapi import APIRouter, HTTPException, status

from schemas import StockData, StockDataOnlyCode

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
async def get_stock_list() -> list[str]:
    stock_code_list = await StockData.find_all(projection_model=StockDataOnlyCode).to_list()

    return list(map(lambda stock: stock.code, stock_code_list))


@router.get(
    path="/{stock_code}",
    status_code=status.HTTP_200_OK,
    response_model=StockData
)
async def get_stock_info(stock_code: str) -> StockData:
    target_stock = await StockData.find_one(StockData.code == stock_code)

    if target_stock is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="stock not found"
        )

    return target_stock
