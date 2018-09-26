######################################################################
# WEB SCRAPING DE WEB delalonjaalamesa Y ALMACENADO EN TSBD GRAPHITE #
######################################################################


# LIBRERIAS

import requests
from bs4 import BeautifulSoup
import graphyte
import logging


# DECLARACION DE VARIABLES

# Fichero de log:
LOG_FILE = "/var/log/lonja/lonja.log"

# Nivel de log (configurar NOTSET, DEBUG, INFO, WARNING, ERROR o CRITICAL):
LOG_LEVEL = "INFO"

# Direccion web:
URL = "http://www.delalonjaalamesa.es/"

# Tiempo de espera para obtener respuesta de la web (en segundos):
TIMEOUT = 120

# Datos del servidor de Graphite:
GRAPHITE_SERVER = "127.0.0.1"
GRAPHITE_PORT = 2003
GRAPHITE_PREFIX = "datos.lonja"


# PROGRAMA PRINCIPAL

# Inicio:
print()

# Configurar logger a fichero:
logging.basicConfig(level=getattr(logging, LOG_LEVEL),
                    format="[%(asctime)s] [%(levelname)s] - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=LOG_FILE,
                    filemode='a')
logging.info("Inicio del programa")

# Configurar logger a stdout:
console = logging.StreamHandler()
console.setLevel(getattr(logging, LOG_LEVEL))
console.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
logging.getLogger('').addHandler(console)

# Descargar html de la web:
index_html = requests.get(URL, timeout=TIMEOUT)

# Comprobacion del estado de la web:
if index_html.status_code != requests.codes.ok:
    logging.error("Descarga de la pagina web incorrecta")
    print()
    exit(1)
else:
    logging.info("Descarga de la pagina web correcta")

# Web scraping:
soup = BeautifulSoup(index_html.content, "lxml")
product_list = soup.find_all("div", class_="item column-1")
product_list.extend = soup.find_all("div", class_="item column-2")
product_list.extend = soup.find_all("div", class_="item column-3")

# Comprobacion de productos encontrados:
if len(product_list) == 0:
    logging.warning("No se encuentra ningun producto en la web")
    print()
    exit(2)
else:
    logging.info("Productos encontrados: %s", len(product_list))

# Obtencion de productos, precios y unidades, y envio a Graphite:
graphyte.init(GRAPHITE_SERVER, port=GRAPHITE_PORT, prefix=GRAPHITE_PREFIX)
for product_obj in product_list:
    product_txt = product_obj.text.strip()
    name_tmp = product_txt.splitlines()[0]
    name_tmp_2 = name_tmp.lower()
    name = name_tmp_2.replace("\t", "")
    price_tmp = product_txt.splitlines()[3]
    price_tmp_2 = price_tmp.strip("Precio: ")
    price_tmp_3 = price_tmp_2.replace(",", ".")
    price = price_tmp_3.split()[0]
    unit_tmp = product_txt.splitlines()[3]
    if len(unit_tmp.split()) == 4:
        unit = unit_tmp.split()[2] + unit_tmp.split()[3]
    else:
        unit = unit_tmp.split()[2]

    # Visualización de los valores obtenidos:
    logging.debug("Producto: %s", name)
    logging.debug("Precio: %s %s", price, unit)

    # Envio de metricas a Graphite:
    metric_prefix = name.replace(" ", "_")
    graphyte.send(metric_prefix, float(price))

logging.info("Precios registrados en TSDB")

# Fin del programa:
logging.info("Fin del programa")
print()
exit(0)