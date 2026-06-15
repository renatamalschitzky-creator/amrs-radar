import feedparser
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

FEEDS = {
    "amrs_social": {
        "label": "Social Media & Plataformas",
        "tab": "amrs",
        "color": "orange",
        "keywords": [
            "social media","mídias sociais","mídias digitais","instagram","facebook",
            "threads","linkedin","tiktok","whatsapp","meta","rede social","redes sociais",
            "negócios digitais","negocios digitais"
        ],
        "sources": [
            "https://www.meioemensagem.com.br/feed/",
            "https://resultadosdigitais.com.br/feed/",
            "https://rockcontent.com/br/blog/feed/",
            "https://marketingdeconteudo.com/feed/",
            "https://www.b9.com.br/feed/",
            "https://exame.com/feed/",
        ]
    },
    "amrs_ia": {
        "label": "Inteligência Artificial",
        "tab": "amrs",
        "color": "purple",
        "keywords": [
            "inteligência artificial","inteligencia artificial","ia ","claude","chatgpt",
            "anthropic","openai","gemini","llm","machine learning","gpt"
        ],
        "sources": [
            "https://exame.com/feed/",
            "https://tecnoblog.net/feed/",
            "https://www.canaltech.com.br/rss/",
            "https://olhardigital.com.br/feed/",
            "https://www.meioemensagem.com.br/feed/",
        ]
    },
    "amrs_empreende": {
        "label": "Empreendedorismo & Liderança",
        "tab": "amrs",
        "color": "teal",
        "keywords": [
            "empreendedorismo","empreendedor","liderança","lideranca","micro empresa",
            "pequena empresa","mpe","mei","startup","gestão","negócio","negocio"
        ],
        "sources": [
            "https://exame.com/feed/",
            "https://www.sebraepr.com.br/feed/",
            "https://epocanegocios.globo.com/rss/0,,AS0,00.xml",
            "https://www.meioemensagem.com.br/feed/",
            "https://revistapegn.globo.com/rss/0,,AS0,00.xml",
        ]
    },
    "criterio": {
        "label": "Critério Seguros",
        "tab": "clientes",
        "color": "blue",
        "keywords": [
            "seguro","seguros","seguradora","corretor de seguros","apólice",
            "paraná","curitiba","sinistro","vida seguro","auto seguro"
        ],
        "sources": [
            "https://www.cqcs.com.br/feed/",
            "https://www.sonaseg.com.br/feed/",
            "https://exame.com/feed/",
            "https://g1.globo.com/rss/g1/economia/",
            "https://www.gazetadopovo.com.br/rss/ultimas-noticias.xml",
        ]
    },
    "patins": {
        "label": "ECPA & Spin Patins",
        "tab": "clientes",
        "color": "pink",
        "keywords": [
            "patinação artística","patinacao artistica","patinação","patins","figura no gelo",
            "skate artístico","patinação no brasil","cbhp"
        ],
        "sources": [
            "https://ge.globo.com/rss/ge/esportes-olimpicos/",
            "https://www.uol.com.br/esporte/rss.xml",
            "https://exame.com/feed/",
            "https://www.terra.com.br/esportes/?output=rss",
        ]
    },
    "sierra": {
        "label": "Sierra Móveis",
        "tab": "clientes",
        "color": "amber",
        "keywords": [
            "construção","arquitetura","decoração","moveis","móveis","interiores",
            "guarapuava","design de interiores","reforma","imobiliário","imobiliario",
            "sierra moveis","sierra móveis"
        ],
        "sources": [
            "https://casavogue.globo.com/rss",
            "https://www.gazetadopovo.com.br/rss/ultimas-noticias.xml",
            "https://exame.com/feed/",
            "https://www.archdaily.com.br/br/feed",
            "https://revistacasaejardim.globo.com/rss",
        ]
    },
    "marcos": {
        "label": "Marcos Esquadrias",
        "tab": "clientes",
        "color": "gray",
        "keywords": [
            "esquadria","esquadrias","pvc","alumínio","aluminio","janela","porta",
            "arquitetura alto padrão","construção alto padrão","fachada","revestimento",
            "tendência arquitetura","tendencia arquitetura"
        ],
        "sources": [
            "https://www.archdaily.com.br/br/feed",
            "https://casavogue.globo.com/rss",
            "https://www.gazetadopovo.com.br/rss/ultimas-noticias.xml",
            "https://exame.com/feed/",
        ]
    },
    "tpm": {
        "label": "TPM — Umbanda",
        "tab": "clientes",
        "color": "coral",
        "keywords": [
            "umbanda","candomblé","candomble","religiões afro","religioes afro",
            "espiritismo","terreiro","orixá","orixa","religiões de matriz africana"
        ],
        "sources": [
            "https://www.uol.com.br/vivabem/rss.xml",
            "https://g1.globo.com/rss/g1/",
            "https://exame.com/feed/",
        ]
    }
}

def fetch_and_filter(section_key, section):
    keywords = [k.lower() for k in section["keywords"]]
    seen_titles = set()
    items = []

    for url in section["sources"]:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:30]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                text = (title + " " + summary).lower()

                if not any(kw in text for kw in keywords):
                    continue

                title_clean = title.strip()
                if title_clean in seen_titles:
                    continue
                seen_titles.add(title_clean)

                pub = entry.get("published_parsed") or entry.get("updated_parsed")
                if pub:
                    dt = datetime(*pub[:6])
                else:
                    dt = datetime.now()

                # só últimos 7 dias
                if datetime.now() - dt > timedelta(days=7):
                    continue

                source_name = feed.feed.get("title", url.split("/")[2])

                items.append({
                    "title": title_clean,
                    "link": entry.get("link", "#"),
                    "source": source_name,
                    "date": dt.strftime("%Y-%m-%d"),
                    "date_label": format_date(dt),
                    "datetime": dt.isoformat(),
                    "day_of_week": dt.strftime("%a"),
                })
        except Exception as e:
            print(f"  Erro em {url}: {e}")

    items.sort(key=lambda x: x["datetime"], reverse=True)
    return items[:40]

def format_date(dt):
    days_pt = {"Mon":"Seg","Tue":"Ter","Wed":"Qua","Thu":"Qui","Fri":"Sex","Sat":"Sáb","Sun":"Dom"}
    day_en = dt.strftime("%a")
    return f"{days_pt.get(day_en, day_en)} {dt.strftime('%d/%m')}"

def main():
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)

    all_data = {
        "generated_at": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        "sections": {}
    }

    for key, section in FEEDS.items():
        print(f"Coletando: {section['label']}...")
        items = fetch_and_filter(key, section)
        print(f"  → {len(items)} notícias encontradas")
        all_data["sections"][key] = {
            "label": section["label"],
            "tab": section["tab"],
            "color": section["color"],
            "items": items
        }

    output_path = output_dir / "news.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\nSalvo em {output_path}")
    print(f"Total de seções: {len(all_data['sections'])}")

if __name__ == "__main__":
    main()
