import feedparser
import pandas as pd
import os
from datetime import datetime

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
RSS_FEEDS = {
    "RPP": "https://rpp.pe/feed",
    "El Comercio": "https://elcomercio.pe/arcio/rss/",
    "Perú21": "https://peru21.pe/arcio/rss/",
    "La República": "https://larepublica.pe/rss/",
    "Gestión": "https://gestion.pe/arcio/rss/",
    "Andina": "https://andina.pe/agencia/rss.aspx",
    "Correo": "https://diariocorreo.pe/arcio/rss/",
    "Expreso": "https://www.expreso.com.pe/feed/",
    "Trome": "https://trome.pe/arcio/rss/",
    "Ojo": "https://ojo.pe/arcio/rss/",
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"noticias_peru_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def fetch_all_news():
    all_news = []

    for source, url in RSS_FEEDS.items():
        print(f"📡 Obteniendo noticias de {source} ...")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            noticia = {
                "titulo": entry.get("title", "Sin título"),
                "enlace": entry.get("link", "Sin enlace"),
                "fecha": entry.get("published", "Sin fecha"),
                "descripcion": entry.get("summary", "Sin descripción"),
                "categoria": entry.get("category", "Sin categoría"),
                "fuente": source,
                "imagen": "",
                "contenido": entry.get("summary", "Sin contenido"),
            }

            # Intentar capturar imágenes si existen
            if "media_content" in entry:
                try:
                    noticia["imagen"] = entry.media_content[0]["url"]
                except Exception:
                    noticia["imagen"] = "Sin imagen"

            elif "links" in entry:
                for l in entry.links:
                    if "image" in l.get("type", ""):
                        noticia["imagen"] = l.get("href", "Sin imagen")
                        break

            all_news.append(noticia)

    # Crear DataFrame y limpiar valores
    df = pd.DataFrame(all_news)
    df = df.fillna("Sin información")

    # Guardar archivo
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\n✅ Noticias guardadas correctamente en: {OUTPUT_FILE}")
    print(f"📰 Total de noticias recolectadas: {len(df)}")

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    fetch_all_news()
