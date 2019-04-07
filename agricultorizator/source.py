from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import col, expr, when
from pyspark import SparkContext, SparkConf
from globals import spark
import json

sc = SparkContext()
sqlContext = SQLContext(sc)
spark_instance = spark.get_instance()

def open_csv(name):
    path = "./data/" + name + ".csv"
    df = spark_instance.read.csv(
        path,
        sep = ";",
        header = True,
        schema = get_schema(name)
    )
    return df

def get_schema(schema_name):
    
    schema_path = './schema/'
    
    with open(schema_path + schema_name + ".json", 'r') as file:
        data = json.load(file)

        params = []
        for _ in range(len(data["columns"])):
            if data["columns"][_]["column_type"] == "int":
                params.append(StructField(data["columns"][_]["name"].lower(), IntegerType(), data["columns"][_]["null"]))
            elif data["columns"][_]["column_type"] == "float":
                params.append(StructField(data["columns"][_]["name"].lower(), DoubleType(), data["columns"][_]["null"]))
            elif data["columns"][_]["column_type"] == "string":
                params.append(StructField(data["columns"][_]["name"].lower(), StringType(), data["columns"][_]["null"]))
            elif data["columns"][_]["column_type"] == "bool":
                params.append(StructField(data["columns"][_]["name"].lower(), BooleanType(), data["columns"][_]["null"]))

    return StructType(params)

def drop_column(df, name):
    df = df.drop(name)
    return df
