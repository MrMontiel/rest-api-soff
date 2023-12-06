from app.infrastructure.database import ConectDatabase
from sqlalchemy import select, func,desc, case
from app.products.adapters.sqlalchemy.product import Product
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders
from datetime import datetime, timedelta
from babel.numbers import format_currency
from babel import Locale

session = ConectDatabase.getInstance()
locale = Locale('es', 'ES')

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
    
    if len(sales_this_week) != 0:
        
    # Crear un diccionario para contar las ventas por día
        sales_by_day = {}
        for sale in sales_this_week:
            sale_day = sale.sale_date.strftime("%Y-%m-%d")
            print(sale_day)
            if sale_day in sales_by_day:
                sales_by_day[sale_day] += 1
            else:
                sales_by_day[sale_day] = 1
        print(sales_by_day)
        # Encontrar el día más vendido
        most_sold_day = max(sales_by_day, key=sales_by_day.get)
        total_sales_on_most_sold_daysales_this_week = sales_by_day[most_sold_day]
        
        fecha = datetime.strptime(most_sold_day, '%Y-%m-%d')
        day = getSpanishDay(fecha.strftime('%A'))
    else:
        day = "Lunes"
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
    valor_formateado = format_currency(money, 'EUR', locale=locale)
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
    
    if(len(sales) == 0 or len(past_sales) == 0):
        percentage = 0
    else:
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
    else:
        return {
            "category": "Producto más vendido",
            "target": "No hay",
            "percentage": "No hay",
            "message": f"Inicia las ventas para poder identificar el producto más vendido."
        }
        

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

def getSpanishMounth(mounth: int):
    if mounth == 1:
        return 'Enero'
    elif mounth == 2:
        return 'Febrero'
    elif mounth == 3:
        return 'Marzo'
    elif mounth == 4:
        return 'Abril'
    elif mounth == 5:
        return 'Mayo'
    elif mounth == 6:
        return 'Junio'
    elif mounth == 7:
        return 'Julio'
    elif mounth == 8:
        return 'Agosto'
    elif mounth == 9:
        return 'Septiembre'
    elif mounth == 10:
        return 'Octubre'
    elif mounth == 11:
        return 'Noviembre'
    elif mounth == 12:
        return 'Diciembre'

def getGraficSales():
    sales_by_month = (
        session.query(
            func.extract('year', Sale.sale_date).label('year'),
            func.extract('month', Sale.sale_date).label('month'),
            func.sum(Sale.total).label('total_sales')
        ).group_by('year', 'month').order_by('year', 'month').all()
    )

    result = []
    for row in sales_by_month:
        year = row.year
        month = row.month
        total_sales = row.total_sales

        month_name = getSpanishMounth(month)

        result.append({"Year": year, "Month": month_name, "Total_Sales": total_sales})

    return result

def getPyment():
    current_month = func.extract('month', func.current_date())
    sales_by_month = (
        session.query(
            func.extract('year', Sale.sale_date).label('year'),
            func.extract('month', Sale.sale_date).label('month'),
            func.sum(Sale.total).label('total_sales'),
            func.sum(case((Sale.pyment_method == 'efectivo', Sale.total), else_=0)).label('cash_sales'),
            func.sum(case((Sale.pyment_method == 'transferencia', Sale.total), else_=0)).label('transfer_sales')
        ).filter(func.extract('month', Sale.sale_date) == current_month)
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )

    result = []
    for row in sales_by_month:
        year = row.year
        month = row.month
        total_sales = row.total_sales
        cash_sales = row.cash_sales
        transfer_sales = row.transfer_sales

        month_name = getSpanishMounth(month)

        cash_percentage = int((cash_sales / total_sales) * 100) if total_sales > 0 else 0
        transfer_percentage = int((transfer_sales / total_sales) * 100) if total_sales > 0 else 0

        result.append({
            "Año": year,
            "Mes": month_name,
            "Ventas_Totales": total_sales,
            "Ventas_Efectivo": cash_sales,
            "Ventas_Transferencia": transfer_sales,
            "Porcentaje_Efectivo": cash_percentage,
            "Porcentaje_Transferencia": transfer_percentage
        })

    return (result)


