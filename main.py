from pipeline.eia_client import fetch_data
from pipeline.transform import create_dataframe, clean_data, transform_data
from pipeline.loader import save_parquet



df = create_dataframe(fetch_data("TX","2026-01","2026-01"))

df=clean_data(df)

df = transform_data(df)

save_parquet(df,"TX","2026-01","2026-01")
