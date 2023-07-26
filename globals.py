import pandas as pd

df = pd.read_excel('data/pizza_sales.xlsx')

df['day'] = df['order_date'].apply(lambda x: x.day)

df['hour'] = df['order_time'].apply(lambda x: x.hour)

df['month'] = df['order_date'].apply(lambda x: x.month)
df['month_extenso'] = df['month'].map({1: 'janeiro', 
        2: 'fevereiro',
        3: 'março',
        4: 'abril',
        5: 'maio',
        6: 'junho',
        7: 'julho',
        8: 'agosto',
        9: 'setembro',
        10: 'outubro',
        11: 'novembro',
        12: 'dezembro'})

faturamento = df['total_price'].sum()
faturamento = str(faturamento)
x = 'R$'
faturamento = x + faturamento

n_pedidos = df['order_id'].max()

n_pizzas_vendidas = df['quantity'].sum()

#media p/ dia
dff = df.groupby('order_date').agg({'total_price':'sum'})
dff = dff.reset_index()
lista_dias = dff['order_date'].to_list()
n_dias = len(lista_dias)
faturamento_total = dff['total_price'].sum()
avg_dia = faturamento_total/n_dias
avg_dia = round(avg_dia, 2)
avg_dia = str(avg_dia)
avg_dia = x + avg_dia

#faturamento por mes
faturamento_by_mes = df.groupby('month_extenso', sort=False).agg({'total_price':'sum'})
faturamento_by_mes = faturamento_by_mes.reset_index()

lista_meses = df['month_extenso'].unique()

#datas
data_minima = df['order_date'].min()
data_max = df['order_date'].max()
