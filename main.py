import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# === CONFIG ===
FOLDER_PATH = "datasets"
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "healthcare",
    "user": "postgres",
    "password": "postgres"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def try_parse_decimal(value):
    try:
        return float(value) if value else None
    except:
        return None

def get_or_cache_id(cur, cache, table, column, value, id_col):
    if value in cache:
        return cache[value]
    cur.execute(
        sql.SQL("SELECT {id} FROM {tbl} WHERE {col} = %s").format(
            id=sql.Identifier(id_col),
            tbl=sql.Identifier(table),
            col=sql.Identifier(column)
        ),
        (value,)
    )
    result = cur.fetchone()
    if result:
        cache[value] = result[0]
        return result[0]
    cur.execute(
        sql.SQL("INSERT INTO {tbl} ({col}) VALUES (%s) RETURNING {id}").format(
            tbl=sql.Identifier(table),
            col=sql.Identifier(column),
            id=sql.Identifier(id_col)
        ),
        (value,)
    )
    id_val = cur.fetchone()[0]
    cache[value] = id_val
    return id_val

def get_or_cache_procedure(cur, cache, code, code_type, desc):
    key = (code, code_type, desc)
    if key in cache:
        return cache[key]
    cur.execute("""
        SELECT procedure_id FROM procedure 
        WHERE billing_code = %s AND billing_code_type = %s AND description = %s
    """, (code, code_type, desc))
    result = cur.fetchone()
    if result:
        cache[key] = result[0]
        return result[0]
    cur.execute("""
        INSERT INTO procedure (billing_code, billing_code_type, description)
        VALUES (%s, %s, %s) RETURNING procedure_id
    """, (code, code_type, desc))
    proc_id = cur.fetchone()[0]
    cache[key] = proc_id
    return proc_id

def get_or_cache_plan(cur, cache, insurance_id, plan_name):
    key = (insurance_id, plan_name)
    if key in cache:
        return cache[key]
    cur.execute("SELECT plan_id FROM insurance_plan WHERE insurance_id = %s AND plan_name = %s",
                (insurance_id, plan_name))
    result = cur.fetchone()
    if result:
        cache[key] = result[0]
        return result[0]
    cur.execute("INSERT INTO insurance_plan (insurance_id, plan_name) VALUES (%s, %s) RETURNING plan_id",
                (insurance_id, plan_name))
    plan_id = cur.fetchone()[0]
    cache[key] = plan_id
    return plan_id

def process_file(filepath, conn):
    print(f"📄 Processing file: {os.path.basename(filepath)}")
    df = pd.read_csv(filepath, dtype=str)
    df.columns = df.columns.str.strip()
    df = df.where(pd.notnull(df), None)

    cur = conn.cursor()

    hospital_cache = {}
    payer_cache = {}
    plan_cache = {}
    procedure_cache = {}

    charge_rows = []

    for _, row in df.iterrows():
        hospital_id = get_or_cache_id(cur, hospital_cache, "hospital", "hospital_name", row["hospital_name"], "hospital_id")

        if hospital_id not in hospital_cache or hospital_cache[hospital_id] == "NEW":
            cur.execute("""
                UPDATE hospital SET 
                    street_address = %s,
                    city = %s,
                    state = %s,
                    zip_code = %s
                WHERE hospital_id = %s
            """, (row["street_address"], row["city"], row["state"], row["zip_code"], hospital_id))
            hospital_cache[hospital_id] = "SET"

        insurance_id = get_or_cache_id(cur, payer_cache, "insurance_provider", "payer_name", row["payer_name"], "insurance_id")
        plan_id = get_or_cache_plan(cur, plan_cache, insurance_id, row["plan_name"])
        procedure_id = get_or_cache_procedure(cur, procedure_cache, row["billing_code"], row["billing_code_type"], row["description"])

        charge_rows.append((
            hospital_id,
            procedure_id,
            plan_id,
            try_parse_decimal(row["standard_charge"]),
            try_parse_decimal(row.get("negotiated_dollar")),
            try_parse_decimal(row.get("negotiated_percentage")),
            try_parse_decimal(row.get("estimated_amount")),
            try_parse_decimal(row.get("min_charge")),
            try_parse_decimal(row.get("max_charge"))
        ))

    cur.executemany("""
        INSERT INTO charges (
            hospital_id, procedure_id, plan_id,
            standard_charge, negotiated_dollar,
            negotiated_percentage, estimated_amount,
            min_charge, max_charge
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, charge_rows)

    conn.commit()
    cur.close()
    print(f"✅ Done: {os.path.basename(filepath)}")

def main():
    conn = connect_db()
    files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if f.endswith(".csv")]

    for file in files:
        process_file(file, conn)

    conn.close()
    print("✅ All CSVs in folder processed successfully.")

if __name__ == "__main__":
    main()
