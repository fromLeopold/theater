from datetime import timedelta

import pandas as pd
import plotly.express as px
from django.db.models import Model
from django.utils import timezone
from admin_panel.models import DailyPerformanceStatistics, DailyTimeStatistics


graph_layout_settings = {
    'template': 'plotly_dark',
    'title_x': 0.5,
    'title_font_size': 10,
    'margin': dict(l=20, r=20, t=40, b=20),
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'font': dict(color='white')
}


def get_graphs_set():
    graphs = {
        'Доход по дням за последний месяц': revenue_over_time_html_graph(),
        'Количество проданных билетов по дням за последний месяц': tickets_sold_over_time_html_graph(),
        'Доход по дням недели за последний месяц': revenue_by_weekday_html_graph(),
        'Количество проданных билетов по дням недели за последний месяц': tickets_sold_by_weekday_html_graph(),
        'Доход по спектаклям за последний месяц': revenue_by_performance_html_graph(),
        'Количество проданных билетов по спектаклям за последний месяц': tickets_sold_by_performance_html_graph(),
        'Линейный график доход по дням за последний месяц': visits_over_time_html_graph(),
    }
    return graphs


# Функция для получения данных за последний месяц
def get_last_month_data(model: Model):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    return model.objects.filter(date__range=[start_date, end_date]).order_by("date")


# Линейный график проданные билеты по времени за последний месяц
def visits_over_time_html_graph():
    # Получение данных за последний месяц
    stats = get_last_month_data(DailyTimeStatistics).values('date', 'sold_tickets')
    df = pd.DataFrame(stats)
    df['date'] = pd.to_datetime(df['date'])
    grouped_df = df.groupby(df['date'].dt.time).agg({'sold_tickets': 'sum'}).reset_index()
    fig = px.line(grouped_df, x='date', y='sold_tickets',
                  title='Проданные билеты по времени за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Линейный график доход по дням за последний месяц
def revenue_over_time_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('date', 'revenue')
    df = pd.DataFrame(stats)
    df['date'] = pd.to_datetime(df['date'])
    grouped_df = df.groupby(df['date']).agg({'revenue': 'sum'}).reset_index()
    fig = px.line(grouped_df, x='date', y='revenue',
                  title='Доход по дням за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Линейный график количество проданных билетов по дням за последний месяц
def tickets_sold_over_time_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('date', 'sold_tickets')
    df = pd.DataFrame(stats)
    df['date'] = pd.to_datetime(df['date'])
    grouped_df = df.groupby(df['date']).agg({'sold_tickets': 'sum'}).reset_index()
    fig = px.line(grouped_df, x='date', y='sold_tickets',
                  title='Количество проданных билетов по дням за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Столбчатая диаграмма доход по дням недели за последний месяц
def revenue_by_weekday_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('date', 'revenue')
    df = pd.DataFrame(stats)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name()
    weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekdays_order, ordered=True)
    df_grouped = df.groupby('weekday', as_index=False)['revenue'].sum()
    fig = px.bar(df_grouped, x='weekday', y='revenue',
                 title='Доход по дням недели за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Столбчатая диаграмма количество проданных билетов по дням недели за последний месяц
def tickets_sold_by_weekday_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('date', 'sold_tickets')
    df = pd.DataFrame(stats)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name()
    weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekdays_order, ordered=True)
    df_grouped = df.groupby('weekday', as_index=False)['sold_tickets'].sum()
    fig = px.bar(df_grouped, x='weekday', y='sold_tickets',
                 title='Количество проданных билетов по дням недели за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Столбчатая диаграмма доход по спектаклям за последний месяц
def revenue_by_performance_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('performance__name', 'revenue')
    df = pd.DataFrame(stats)
    df_grouped = df.groupby('performance__name', as_index=False)['revenue'].sum()
    fig = px.bar(df_grouped, x='performance__name', y='revenue',
                 title='Доход по спектаклям за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)


# Столбчатая диаграмма количество проданных билетов по спектаклям за последний месяц
def tickets_sold_by_performance_html_graph():
    stats = get_last_month_data(DailyPerformanceStatistics).values('performance__name', 'sold_tickets')
    df = pd.DataFrame(stats)
    df_grouped = df.groupby('performance__name', as_index=False)['sold_tickets'].sum()
    fig = px.bar(df_grouped, x='performance__name', y='sold_tickets',
                 title='Количество проданных билетов по спектаклям за последний месяц')
    fig.update_layout(**graph_layout_settings)
    return fig.to_html(full_html=False)

