import os
import pandas as pd
import pyodbc
import logging


def get_ms_sql_connection():
    """Создает соединение с SQL Server."""

    server = os.environ.get('SQL_SERVER', 'localhost')
    port = os.environ.get('SQL_PORT', '1433')
    database = os.environ.get('SQL_DB', 'master')

    conn_str = (
        f"Driver={{SQL Server}};"
        f"Server={server},{port};"
        f"Database={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(conn_str)

def load_data_to_excel(file_name: str):
    query = """
    SELECT
        ID,
        ProductName,
        Description,
        PurchasePrice,
        CONVERT(VARCHAR(10), PurchaseDate, 104) as PurchaseDateFormatted,
        SellingPrice,
        SellingPrice - PurchasePrice AS Profit,
        ROUND((SellingPrice - PurchasePrice) * 100.0 / NULLIF(PurchasePrice, 0), 2) AS ProfitPercent,
        CASE
            WHEN PurchasePrice > 100 THEN 'Дорогой'
            WHEN PurchasePrice > 30 THEN 'Средний'
            ELSE 'Бюджетный'
        END AS PriceCategory
    FROM master.dbo.Products
    WHERE Description IN ('Комната', 'Зал')
        AND PurchasePrice > 10
        AND PurchaseDate >= '20190101'
        AND PurchaseDate < '20210101'
    ORDER BY PurchaseDate DESC
    """

    try:
        logging.info("Подключение к базе данных...")
        with get_ms_sql_connection() as conn:
            # Pandas сам выполняет запрос и превращает результат в таблицу (DataFrame)
            df = pd.read_sql(query, conn)

        if df.empty:
            logging.warning("Нет данных, соответствующих условиям.")
            return

        # # Переименовываем столбцы (аналог массива headers в VBA)
        # df.columns = [
        #     "ID", "Товар", "Описание", "Цена закупки",
        #     "Дата закупки", "Цена продажи", "Прибыль",
        #     "Прибыль %", "Категория цены"
        # ]

        # Сохранение в Excel
        logging.info(f"Загружено {len(df)} строк. Сохранение в файл...")

        # Используем контекстный менеджер для записи
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Данные', index=False)

            # Настройка форматирования (аналог NumberFormat и AutoFit в VBA)
            workbook  = writer.book
            worksheet = writer.sheets['Данные']

            # Формат для чисел
            num_format = workbook.add_format({'num_format': '#,##0.00'})
            # Формат для процентов
            pct_format = workbook.add_format({'num_format': '0.00%'})

            # Применяем форматы к столбцам (A=0, B=1 и т.д.)
            worksheet.set_column('D:G', 15, num_format) # Цены и прибыль
            worksheet.set_column('H:H', 12, pct_format) # Проценты
            worksheet.set_column('B:C', 20)             # Ширина для текста

            # Добавляем автофильтр
            # worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

        logging.info(f"Файл '{file_name}' успешно создан!")

    except Exception as e:
        logging.error(f"Ошибка при работе с SQL/Excel: {e}")
