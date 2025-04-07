import os
import polars as pl
import psycopg2
import structlog
from psycopg2.extras import execute_values
from rapidfuzz import process as rapid_process

log = structlog.get_logger()

CONNECTION = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    database=os.environ['POSTGRES_DB'],
    port=5432
)

def _ingest_raw_fact():
    path = "~/data/Amazon-Sale-Report.csv"
    log.info('ingest_raw_fact', path=path)
    df = pl.read_csv(path)
    df = df.drop("Unnamed: 22")
    log.info(df.head())

    return df.to_dict(as_series=False)

def _clean_data(df):
    import ast
    log.info(type(df))
    df = ast.literal_eval(df)
    df = pl.DataFrame(df)
    log.info(df.head())

    log.info('clean_data')
    state_df = pl.read_csv("~/data/state.csv")
    log.info(state_df.head())

    def clean_state(state):
        if "," in state:
            state = state.split(",")[-1].strip()
        state = state.split("-") [0].strip()
        return state.lower()
    # Clean city in df
    df = df.with_columns(
        df["ship-state"].map_elements(clean_state, return_dtype=pl.Utf8).alias("clean_state")
    )
    log.info(df.head())

    def match_city(state, state_list):
        if not isinstance(state, str) or not state:
            return None
        try:
            match = rapid_process.extractOne(state, state_list, score_cutoff=70)
            if match:
                return match[0]  # match là tuple (match, score, index)
            return None
        except Exception as e:
            print(f"Lỗi khi fuzzy matching cho state '{state}': {e}")
            return None

    # Create a list of state from the city_df
    state_list = state_df["Subdivision Name"].to_list()
    log.info(state_list)
    df = df.with_columns(
        pl.col("clean_state").map_elements(
            lambda x: match_city(x, state_list),
            return_dtype=pl.Utf8
        ).alias("matched_state")
    )
    log.info(df.head())

    df = df.join(state_df, left_on="matched_state", right_on="Subdivision Name", how="left")

    log.info(df.head())

    df = df.drop("matched_state", "clean_state", "Subdivision category")

    log.info(df.head())

    return df.to_dict(as_series=False)

def _write_to_dw(df):
    import ast
    log.info('write_to_dw')
    df = ast.literal_eval(df)
    df = pl.DataFrame(df)
    log.info(df.columns)
    with CONNECTION as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS raw_fact')
        cursor.execute("""
            CREATE TABLE raw_fact (
                idx INT,                        -- Cột đại diện cho index (khóa tự tăng nếu cần)
                order_id VARCHAR(50),           -- Order ID
                order_date DATE,                -- Date (đổi tên thành order_date để tránh mâu thuẫn với từ khóa DATE)
                status VARCHAR(50),             -- Status
                fulfilment VARCHAR(50),         -- Fulfilment
                sales_channel VARCHAR(50),      -- Sales Channel
                ship_service_level VARCHAR(50), -- ship-service-level
                style VARCHAR(50),              -- Style
                sku VARCHAR(50),                -- SKU
                category VARCHAR(100),          -- Category
                size VARCHAR(20),               -- Size
                asin VARCHAR(20),               -- ASIN
                courier_status VARCHAR(50),     -- Courier Status
                qty INT,                        -- Qty
                currency VARCHAR(10),           -- currency
                amount DECIMAL(10,2),           -- Amount
                ship_city VARCHAR(100),         -- ship-city
                ship_state VARCHAR(100),        -- ship-state
                ship_postal_code VARCHAR(20),   -- ship-postal-code
                ship_country VARCHAR(50),       -- ship-country
                promotion_ids TEXT,             -- promotion-ids
                b2b BOOLEAN,                    -- B2B
                fulfilled_by VARCHAR(50),       -- fulfilled-by
                code VARCHAR(5)                 -- code
            );
        """)

        conn.commit()

    with CONNECTION as conn:
        cursor = conn.cursor()
        rows = [row for row in df.iter_rows()]
        insert_query = """
            INSERT INTO raw_fact (
                idx, order_id, order_date, status, fulfilment, sales_channel,
                ship_service_level, style, sku, category, size, asin,
                courier_status, qty, currency, amount, ship_city, ship_state,
                ship_postal_code, ship_country, promotion_ids, b2b, fulfilled_by, code
            ) VALUES %s
            """
        execute_values(cursor, insert_query, rows)
        conn.commit()
    log.info(f"Ingestion raw_fact complete")




