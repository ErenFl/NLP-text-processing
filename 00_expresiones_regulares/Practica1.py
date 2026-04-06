import csv
import re
import emoji

from tabulate import tabulate
from collections import Counter

def encontrar_patrones(texto):
    # Patrón para buscar hashtags (palabras que comienzan con #)
    hashtags = re.findall(r'#\w+', texto)

    # Patrón para buscar usuarios (palabras que comienzan con @)
    usuarios = re.findall(r'@\w+', texto)

    # Patrón para buscar URLs (cadenas que comienzan con http:// o https://)
    urls = re.findall(r'https?://\S+', texto)

    # Patrón para buscar tiempos en varios formatos (por ejemplo, 18:30, 5 hrs, 3 am, etc.)
    #Teniendo como limite 23 en horas y 59 en minutos
    tiempos = re.findall(r'\b(?:[0-1]?[0-9]|2[0-3]):[0-5][0-9]\b|\b\d+\s*(?:hrs|am|pm)\b', texto)

    # Patrón para encontrar emoticonos en ASCII (por ejemplo, :))
    emoticonos_completos = re.findall(r'(?::|;|=)(?:-)?(?:\)|\(|D|d|P|p|O|o|c|3|\/|\\)', texto)

    return hashtags, usuarios, urls, tiempos, emoticonos_completos

def encontrar_emojis(texto):
    patron_emoji = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U00002639\U00002640\U00002642\U00002648\U00002649\U0000264A\U0000264B\U0000264C\U0000264D\U0000264E\U0000264F\U0001F170-\U0001F251\U0001F600-\U0001F64F\U0001F1E0-\U0001F1FF]+', flags=re.UNICODE)

    emojis_encontrados = patron_emoji.findall(texto)
    return emojis_encontrados

nombre_archivo = 'C:\Users\cruz_\OneDrive\Escritorio\ML\00_expresiones_Regulares\Tweets 2.csv'

# Lista para almacenar los resultados de cada enunciado
resultados = []

# Listas para almacenar los resultados totales de cada categoría
hashtags_totales = []
usuarios_totales = []
urls_totales = []
tiempos_totales = []
emoticonos_completos_totales = []
emojis_totales = []

# Abre el archivo CSV y aplica las expresiones regulares a cada enunciado
with open(nombre_archivo, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader, 1):  # Enumera las filas, comenzando desde 1
        enunciado = row[0]  # Lee el enunciado que se encuentra en la primera columna

        # Llama a la función para encontrar patrones en cada enunciado
        hashtags, usuarios, urls, tiempos, emoticonos_completos = encontrar_patrones(enunciado)

        # Convierte los emoticonos en emojis
        emojis = encontrar_emojis(enunciado)

        # Almacena los resultados en una lista
        resultados.append({
            "Hashtags encontrados": hashtags,
            "Usuarios encontrados": usuarios,
            "URLs encontradas": urls,
            "Tiempos encontrados": tiempos,
            "Emoticonos encontrados": emoticonos_completos,
            "Emojis encontrados": emojis
        })

        # Agrega los resultados a las listas totales para cada categoría
        hashtags_totales.extend(hashtags)
        usuarios_totales.extend(usuarios)
        urls_totales.extend(urls)
        tiempos_totales.extend(tiempos)
        emoticonos_completos_totales.extend(emoticonos_completos)
        emojis_totales.extend(emojis)
        
# Calcula las frecuencias totales de cada categoría
frecuencia_hashtags = len(hashtags_totales)
frecuencia_usuarios = len(usuarios_totales)
frecuencia_urls = len(urls_totales)
frecuencia_tiempos = len(tiempos_totales)
frecuencia_emoticon = len(emoticonos_completos_totales)
frecuencia_emojis = len(emojis_totales)

# Calcula los top 10 elementos más frecuentes de cada categoría
top10_hashtags = Counter(hashtags_totales).most_common(10)
top10_usuarios = Counter(usuarios_totales).most_common(10)
top10_urls = Counter(urls_totales).most_common(10)
top10_tiempos = Counter(tiempos_totales).most_common(10)
top10_emoticonos = Counter(emoticonos_completos_totales).most_common(10)
top10_emojis = Counter(emojis_totales).most_common(10)

# Imprime la tabla con los resultados totales y los top 10
tabla_filas_totales = [
    ["Hashtags", frecuencia_hashtags, '\n'.join([f"#Tendencia {i+1}: {hashtag}" for i, (hashtag, _) in enumerate(top10_hashtags)])],
    ["Usuarios", frecuencia_usuarios, '\n'.join([f"#Puesto {i+1}: {usuario}" for i, (usuario, _) in enumerate(top10_usuarios)])],
    ["URLs", frecuencia_urls, '\n'.join([f"#Puesto {i+1}: {url}" for i, (url, _) in enumerate(top10_urls)])],
    ["Tiempos", frecuencia_tiempos, '\n'.join([f"#Puesto {i+1}: {tiempo}" for i, (tiempo, _) in enumerate(top10_tiempos)])],
    ["Emoticones ASCII", frecuencia_emoticon, '\n'.join([f"#Puesto {i+1}: {emoticono}" for i, (emoticono, _) in enumerate(top10_emoticonos)])],
    ["Emojis", frecuencia_emojis, '\n'.join([f"#Puesto {i+1}: {emoji}" for i, (emoji, _) in enumerate(top10_emojis)])]
]

print("\nTabla de resultados totales:")
print(tabulate(tabla_filas_totales, headers=["Categoría", "Frecuencia  ", "   Top10"], tablefmt="grid"))