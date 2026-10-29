import requests as rq
# import polars as prs
import gzip
import shutil

#   fonction pour récupérer l'url et mettre le fichier csv dans le disque
def download_file(url,destination):
    
    headers = {"User-agent" : "Mozilla/5.0"}
    resp = rq.get(url,headers=headers)
    with open(destination,"wb") as file:

        file.write(resp.content)
        
    return destination


print(download_file(f" https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz",f"/home/ilyes/projects/pipeline-etl-01/data/food2.csv.gz"))

# Fonction pour décompresser les fichier de gz --> csv et les copier 
def decompressed_file(source,destination):

    with gzip.open(source,'rb') as f :
        with open(destination, "wb") as d : 
            shutil.copyfileobj(f,d)
        return destination
        

print(decompressed_file(f"data/food2.csv.gz",f"data/food.csv"))