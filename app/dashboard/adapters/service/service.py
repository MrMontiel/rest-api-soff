from app.infrastructure.database import ConectDatabase
from sqlalchemy import select, func,desc
from app.products.adapters.sqlalchemy.product import Product
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders
from datetime import datetime, timedelta
import locale


session = ConectDatabase.getInstance()
locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')

def getSpanishDay(day: str):
    if day == 'Monday':
        return 'Lunes'
    elif day == 'Tuesday':
        return 'Martes'
    elif day == 'Wednesday':
        return 'Miércoles'
    elif day == 'Thursday':
        return 'Jueves'
    elif day == 'Friday':
        return 'Viernes'
    elif day == 'Saturday':
        return 'Sábado'
    elif day == 'Sunday':
        return 'Domingo'

def getBestSellingDay():
    today = datetime.utcnow()
    last_monday = today - timedelta(days=(today.weekday() + 6) % 7)
    sales_this_week = session.query(Sale).filter(Sale.sale_date >= last_monday, Sale.sale_date <= today).all()
    
    # Crear un diccionario para contar las ventas por día
    sales_by_day = {}
    for sale in sales_this_week:
        sale_day = sale.sale_date.strftime("%Y-%m-%d")
        if sale_day in sales_by_day:
            sales_by_day[sale_day] += 1
        else:
            sales_by_day[sale_day] = 1
        
    # Encontrar el día más vendido
    most_sold_day = max(sales_by_day, key=sales_by_day.get)
    total_sales_on_most_sold_day = sales_by_day[most_sold_day]
    
    fecha = datetime.strptime(most_sold_day, '%Y-%m-%d')
    day = getSpanishDay(fecha.strftime('%A'))
    
    response = {
        "category": 'Día más vendido',
        "target": day,
        "percentage": '20%',
        "message": f'¿Sabías que los {day} hay un aumento de ventas?'
    }
    return response

def moneyWin():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday, Sale.sale_date <= sunday)).all()
    past_sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday - timedelta(days=6), Sale.sale_date <= monday)).all()
    
    money = 0
    for n in sales:
        money += n.total
    valor_formateado = locale.currency(money, grouping=True)
    value = valor_formateado.rstrip('0').rstrip('.') if '.' in valor_formateado else valor_formateado.rstrip('0')
    response = {
        "category": 'Dinero ganado',
        "target": value,
        "percentage": '08%',
        "message": 'Realizamos un 08% más de dinero que la semana pasada'
    }
    
    
    return response 
    
def getAmountSales():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday, Sale.sale_date <= sunday)).all()
    past_sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday - timedelta(days=6), Sale.sale_date <= monday)).all()
    
    percentage = (len(sales))/len(past_sales)
    
    response = {
        "category": "Ventas",
        "target": f"+{len(sales)}",
        "percentage": f"+{percentage}%",
        "message": f"Realizamos un {percentage}% más de ventas que la semana pasada"
    }
    
    return response

def ProductMoreSale():

    today = datetime.utcnow()
    last_monday = today - timedelta(days=(today.weekday() + 6) % 7)

    # Consulta para encontrar el producto más vendido en el rango de fechas dado
    most_sold_product = session.query(Product, func.sum(SalesOrders.amount_product).label('total_sold')) \
        .join(SalesOrders, Product.id == SalesOrders.product_id) \
        .join(Sale, SalesOrders.sale_id == Sale.id) \
        .filter(Sale.sale_date >= last_monday, Sale.sale_date <= today) \
        .group_by(Product.id) \
        .order_by(func.sum(SalesOrders.amount_product).desc()) \
        .first()

    if most_sold_product:
        product, total_sold = most_sold_product
        response = {
            "category": "Producto más vendido",
            "target": product.name,
            "percentage": product.name,
            "message": f"{product.name} es el producto más vendido con {total_sold} unidades vendidas."
        }
        return response


def getTargetsDashboard():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday, Sale.sale_date <= sunday)).all()
    past_sales = session.scalars(select(Sale).filter(Sale.sale_date >= monday - timedelta(days=6), Sale.sale_date <= monday)).all()
    

    day = getBestSellingDay()
    sales = getAmountSales()
    money = moneyWin()
    product = ProductMoreSale()

        
    return [day, sales, money, product]