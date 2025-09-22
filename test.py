import pandas as pd

df = pd.read_csv('test_sales_data.csv')


def store_periods(group):
    """
    Групирует периоды в промопериод.
    Промопериодом мы считаем непрерывный(!) отрезок времени,
    когда были продажи в рамках одного магазина.
    """
    promo_periods_df = group.sort_values('period_id')
    promo_periods_df['is_new_period'] = (
        (promo_periods_df['period_id'] - promo_periods_df['period_id'].shift(1)) != 1
    )
    periods = promo_periods_df['is_new_period'].cumsum()
    promo_periods_df['period_group'] = periods
    return promo_periods_df


def continuous_period_by_store(df):
    """Общее количество промопериодов (во всех магазинах)"""
    counts_promo_by_store = df.groupby('store_id').apply(
        lambda group: len(store_periods(group)['period_group'].unique()),
        include_groups=False
    )
    return counts_promo_by_store.sum()


def median_duration_periods(df):
    """Медиана продолжительности промопериода (количество недель)."""
    median_period_by_store = df.groupby('store_id').apply(
        lambda group: store_periods(group).groupby('period_group').size().median(),
        include_groups=False
    )
    return median_period_by_store.median()


def sales_by_store_by_period(df):
    """Объемы продаж по промопериодам."""
    median_period_by_store = df.groupby('store_id').apply(
        lambda group: store_periods(group).groupby('period_group')['sales_volume'].median(),
        include_groups=False
    )
    return median_period_by_store


def median_periods_by_store(df):
    """Медиану количества промопериодов на один магазин"""
    median_period_by_store = df.groupby('store_id').apply(
        lambda group: store_periods(group).groupby('period_group').size(),
        include_groups=False
    )
    return median_period_by_store.median()


def display():
    print(60*'-')
    print(f'Общее количество промопериодов (во всех магазинах): {continuous_period_by_store(df)}')
    print(60*'-')
    print(f'Медиана продолжительности промопериода (количество недель): {median_duration_periods(df):.0f}')
    print(60*'-')
    medians = sales_by_store_by_period(df)
    print("Объемы продаж по промопериодам:")
    medians = sales_by_store_by_period(df)
    for (store_id, period_group), median_value in medians.items():
        print(f'Магазин: {store_id}.Промопериод: {period_group}. Объем продаж: {median_value:.2f}')
    print(60*'-')
    print(f'Медиана количества промопериодов: {median_periods_by_store(df)}')
    print(60*'-')



if __name__ == '__main__':
    display()
