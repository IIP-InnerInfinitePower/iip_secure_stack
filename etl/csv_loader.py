import sys, pandas as pd, sqlalchemy as sa

PORT = "0"  # replace after getting it
engine = sa.create_engine(
    f"postgresql+psycopg2://app_rw:AppRW#2025@127.0.0.1:{PORT}/iipdb", future=True
)
csv = sys.argv[1]
df = pd.read_csv(csv)
with engine.begin() as c:
    df.to_sql("dim_client", c, schema="stg", if_exists="replace", index=False)
    cols = list(df.columns)
    keys = ["client_id"]
    set_cols = [x for x in cols if x not in keys]
    ins = ",".join(cols)
    setc = ",".join([f"{c}=EXCLUDED.{c}" for c in set_cols]) if set_cols else ""
    c.exec_driver_sql(
        f"""INSERT INTO prod.dim_client ({ins})
                          SELECT {ins} FROM stg.dim_client
                          ON CONFLICT (client_id) DO {"UPDATE SET "+setc if setc else "NOTHING"};"""
    )
    c.exec_driver_sql(
        "INSERT INTO prod.fact_ingest(dataset,rows_loaded,status) VALUES (%s,%s,%s)",
        ("clients", int(len(df)), "success"),
    )
print("loaded", len(df))
