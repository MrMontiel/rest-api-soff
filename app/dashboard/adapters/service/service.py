from app.infrastructure.database import ConectDatabase
from sqlalchemy import select, func,desc
from app.sales.adapters.sqlalchemy.sale import Sale
from datetime import datetime, timedelta


session = ConectDatabase.getInstance()

def getBestSellingDay(sales: list):
    Monday = Tuesday = Wednesday = Thursday = Friday = Saturday = Sunday = 0
    
    for n in sales:
        day = str(n.sale_date.strftime("%A"))
        if day == 'Monday':
            Monday += 1
        elif day == 'Tuesday':
            Tuesday += 1
        elif day == 'Wednesday':
            Wednesday += 1
        elif day == 'Thursday':
            Thursday += 1
        elif day == 'Friday':
            Friday += 1
        elif day == 'Saturday':
            Saturday += 1
        elif day == 'Sunday':
            Sunday += 1
            
    max = ""
    if Monday >= 0:
        max = Monday
    else:
        if Tuesday > Monday and Tuesday > Wednesday and Tuesday > Thursday and Tuesday > Friday and Tuesday > Saturday and Tuesday > Sunday:
            max = Tuesday
        elif Tuesday > Monday and Tuesday > Wednesday and Tuesday > Thursday and Tuesday > Friday and Tuesday > Saturday and Tuesday > Sunday:
            max = Tuesday
    pass
        
        
def getAmountSales(amount_sales: int, amount_past_sales: int):
    
    percentage = (amount_past_sales * 100)/amount_sales 
    
    target = {
        "category": "ventas",
        "target": f"+{len(amount_past_sales)}",
        "percentage": f"+{percentage * 100}%",
        "message":  ""
    }
    
    return target
    
def getTargetsDashboard():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday, Sale.sale_date <= sunday)).all()
    # past_sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday - timedelta(days=6), Sale.sale_date <= monday)).all()
    
    getBestSellingDay(sales)
    print(len(sales))
    
    return getAmountSales(len(sales), 8)