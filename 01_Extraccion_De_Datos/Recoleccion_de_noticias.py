import requests
import re
import csv
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup


def obtener_noticias_expansion(url_feed):
    noticias = []
    feed = feedparser.parse(url_feed)
    fecha_actual = datetime.now().date()  # Obtener la fecha actual
    
    for entrada in feed.entries:
        fecha_publicacion = datetime.strptime(entrada.published[:-4], "%a, %d %b %Y %H:%M:%S").date()  # Eliminar " GMT" al final de la cadena
        if fecha_publicacion == fecha_actual:  # Comprobar si la noticia fue publicada hoy
            titulo = entrada.title
            descripcion = entrada.description
            url_noticia = entrada.link
            seccion = entrada.category if 'category' in entrada else 'Sin categoría'  # Usar 'category' si está disponible, de lo contrario, usar 'Sin categoría'
            noticias.append({
                'Title': titulo,
                'Content': descripcion,
                'Section': seccion,
                'Url': url_noticia,
                'Date': fecha_publicacion.strftime("%d/%m/%Y"),  # Formatear la fecha de publicación
                'Source': 'Expansión'
            })
    
    return noticias


def obtener_noticias_jornada(urls):
    datos = []
    meses = {'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 'mayo': '05', 'junio': '06',
             'julio': '07', 'agosto': '08', 'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'}

    for seccion, url in urls.items():
        respuesta = requests.get(url)
        contenido_html = respuesta.text
        soup = BeautifulSoup(contenido_html, 'html.parser')
        items = soup.find_all('div', class_='item')

        for item in items:
            enlace = item.find('a', class_='cabeza')
            parrafo = item.find('p', class_='s-s')
            fecha_elemento = soup.find(class_='main-fecha')
            seccion_elemento = soup.find(class_='spritemenu')

            if enlace and parrafo and fecha_elemento and seccion_elemento:
                titulo = enlace.get_text()
                contenido = parrafo.get_text()
                seccion = seccion
                fecha_texto = fecha_elemento.get_text().strip()
                coincidencias = re.findall(r'(\d{1,2}) de ([a-zA-Z]+) de (\d{4})', fecha_texto)
                
                for dia, mes, anio in coincidencias:
                    num_mes = meses.get(mes.lower())
                    fecha_formateada = f"{dia}/{num_mes}/{anio}"

                    datos.append({
                        'Title': titulo,
                        'Content': contenido,
                        'Section': seccion,
                        'Url': respuesta.url,
                        'Date': fecha_formateada,
                        'Source': 'La Jornada'
                    })

    return datos

urls_feeds = {
    'Tecnología': 'https://expansion.mx/rss/tecnologia',
    'Economía': 'https://expansion.mx/rss/economia',
    'Deportes': 'https://expansion.mx/rss/deportes'
}

# Noticias de Expansion
noticias_expansion = obtener_noticias_expansion('https://expansion.mx/rss/tecnologia')
noticias_expansion2 = obtener_noticias_expansion('https://expansion.mx/rss/economia')
noticias_expansion3 = obtener_noticias_expansion('https://expansion.mx/rss/deportes')

# Obtener noticias de La Jornada
urls_jornada = {
    'Economia': 'https://www.jornada.com.mx/2024/04/01/economia',
    'Cultura': 'https://www.jornada.com.mx/2024/04/01/cultura',
    'Deportes': 'https://www.jornada.com.mx/2024/04/01/deportes',
    'Ciencias': 'https://www.jornada.com.mx/2024/04/01/ciencias'
}
noticias_jornada = obtener_noticias_jornada(urls_jornada)

# Unir todas las noticias en una lista
todas_las_noticias = noticias_jornada + noticias_expansion + noticias_expansion2 + noticias_expansion3

# Escribir las noticias en un archivo CSV
nombre_archivo = 'Dia_1.csv'
with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
    campos = ['Source','Title', 'Content', 'Section', 'Url', 'Date']
    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)
    escritor_csv.writeheader()
    for noticia in todas_las_noticias:
        escritor_csv.writerow(noticia)

print(f"Las noticias se han guardado en el archivo {nombre_archivo}.")
