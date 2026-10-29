import polars as pl
import numpy as np 
import polars.selectors as cs
import polars.lazyframe


lazy_df = pl.scan_csv(f"data/raw/food_sample.csv",separator='\t',ignore_errors=True,truncate_ragged_lines=True,quote_char=None)  # l'échantillon
# lazy_df = pl.scan_csv(f"data/food.csv",separator='\t',ignore_errors=True,truncate_ragged_lines=True,quote_char=None) 


# print(lazy_df.schema)

# print(list(lazy_df.schema.keys()))


df = lazy_df.select(cs.by_name("product_name","nutriscore_grade","countries_en","energy-kcal_100g","proteins_100g","carbohydrates_100g","fiber_100g","sugars_100g",'fat_100g'))

# df_test = df.head(20)
# df_test = df.collect()
# print(df_test)

# Supprimer les lgnes où il n'a pas de nom de produit
df_prodName = df.select(cs.by_name('product_name')).drop_nulls()
print('les null ont été supprimé')
# df_test = df.head(20).collect()
nb_null = df_prodName.null_count().collect()
# print(nb_null)


df_kcalorie = lazy_df.select(cs.by_name("energy-kcal_100g"))
df = df.with_columns(pl.when(pl.col("carbohydrates_100g").is_null()).then(pl.col('carbohydrates_100g').median().over(pl.col("nutriscore_grade")).cast(pl.Float64)).otherwise(pl.col("carbohydrates_100g").cast(pl.Float64)))
print("les glucides ont été remplacés")
df = df.with_columns(pl.when(pl.col("energy-kcal_100g").is_null()).then(pl.col("proteins_100g").cast(pl.Float64) *4 + pl.col("carbohydrates_100g").cast(pl.Float64) * 4 + pl.col("fat_100g").cast(pl.Float64) * 9).otherwise(pl.col("energy-kcal_100g").cast(pl.Float64))) 
# print(df.select(cs.by_name("energy-kcal_100g")).head(10000).filter(pl.col("energy-kcal_100g").is_not_null()).collect().count())
# print(df.select(cs.by_name("carbohydrates_100g")).head(1000).collect())
# print(df.select(cs.by_name("nutriscore_grade").filter(pl.col("nutriscore_grade").is_null())).collect().count())
print(df.filter(pl.col("carbohydrates_100g").is_null()).select(cs.by_name("product_name","nutriscore_grade","carbohydrates_100g")).head(10).collect())
print("c'est faittt")