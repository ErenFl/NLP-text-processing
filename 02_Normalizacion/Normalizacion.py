import csv
import stanza

#Modelo en español
stanza.download('es')


nlp = stanza.Pipeline('es', processors='tokenize,mwt,pos,lemma')


def normalizar_texto(texto):
    # Procesar el texto con Stanza
    doc = nlp(texto)
    
    # Lista de categorías gramaticales
    #'DET': determinante (artículos definidos e indefinidos como "el", "la", "los", "un", "una").
    #'ADP': preposición (como "en", "sobre", "para", "con").
    #'CCONJ': conjunción coordinada (como "y", "pero", "o", "ni").
    #'PRON': pronombre (como "él", "ella", "ellos", "ellas", "nosotros", "usted").
    stopwords_pos = {'DET', 'ADP', 'CCONJ', 'PRON'}
    
    # Lista para almacenar tokens normalizados
    tokens_normalizados = []
    
    for sent in doc.sentences:
        for token in sent.tokens:
            # Verificar si el token no es una stopword
            if token.words[0].upos not in stopwords_pos:
                # Agregar el lema del token normalizado a la lista
                tokens_normalizados.append(token.words[0].lemma)
    
    # Unir los tokens normalizados en una cadena
    texto_normalizado = ' '.join(tokens_normalizados)
    
    return texto_normalizado

ruta_archivo_entrada = '/content/noticias.csv'
ruta_archivo_salida = 'Datacorpus.csv'

# Abrir el archivo CSV de entrada en modo lectura y el archivo de salida en modo escritura
with open(ruta_archivo_entrada, 'r', newline='', encoding='utf-8') as archivo_entrada, \
     open(ruta_archivo_salida, 'w', newline='', encoding='utf-8') as archivo_salida:
    
    # Crear un lector CSV para el archivo de entrada y un escritor CSV para el archivo de salida
    lector_csv = csv.reader(archivo_entrada)
    escritor_csv = csv.writer(archivo_salida)
    
    # Leer los encabezados y escribirlos en el archivo de salida
    encabezados = next(lector_csv)
    escritor_csv.writerow(encabezados)
    
    # Iterar sobre las filas restantes del archivo de entrada
    for fila in lector_csv:
        # Normalizar el título y el contenido de la fila actual
        titulo_normalizado = normalizar_texto(fila[1])
        contenido_normalizado = normalizar_texto(fila[2])
        
        fila_normalizada = [fila[0], titulo_normalizado, contenido_normalizado, fila[3], fila[4], fila[5]]
        escritor_csv.writerow(fila_normalizada)

print("Los datos normalizados se han guardado en 'Datacorpus_normalizado.csv'.")
