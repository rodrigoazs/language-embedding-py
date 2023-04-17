import random
import re
import time
import uuid
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

NEWS_WEBSITES = {
    "pt-pt": [
        "https://www.dn.pt/",
        "https://www.jn.pt/",
        "https://www.publico.pt/",
        "https://www.rtp.pt/noticias/",
        "https://www.cmjornal.pt/",
        "https://www.iol.pt/",
        "https://tvi.iol.pt/noticias/",
        "https://www.sapo.pt/",
        "https://expresso.pt/",
        "https://sol.sapo.pt/",
        "https://www.jornaldenegocios.pt/",
        "https://abola.pt/",
        "https://www.jn.pt/",
        "https://sicnoticias.pt/",
        "https://www.lux.iol.pt/",
        "https://ionline.sapo.pt/",
        "https://www.dinheirovivo.pt/",
        "https://www.aeiou.pt/",
        "https://www.tsf.pt/",
        "https://www.sabado.pt/",
        "https://www.dnoticias.pt/",
        "https://jornaleconomico.pt/",
    ],
    "pt-br": [
        "https://noticias.uol.com.br/",
        "https://www.folha.uol.com.br/",
        "https://www.metropoles.com/",
        "https://www.estadao.com.br/",
        "https://istoe.com.br/",
        "https://oglobo.globo.com/",
        "https://www.ig.com.br/",
        "https://veja.abril.com.br/",
        "https://recordtv.r7.com/",
        "https://www.band.uol.com.br/",
        "https://www.globo.com/",
        "https://www.bol.uol.com.br/",
        "https://www.r7.com/",
        "https://www.terra.com.br/",
        "https://exame.com/",
        "https://www.gazetadopovo.com.br/",
        "https://ge.globo.com/",
        "https://oglobo.globo.com/epoca/",
        "https://www.correio24horas.com.br/capa/",
        "https://www.uai.com.br/",
        "https://www.lance.com.br/",
        "https://olhardigital.com.br/",
        "https://www.tecmundo.com.br/",
        "https://www.techtudo.com.br/",
        "https://www.cnnbrasil.com.br/",
    ],
    "es-ar": [
        "https://www.clarin.com/",
        "http://www.lagaceta.com.ar/",
        "https://www.pagina12.com.ar/",
        "https://www.perfil.com/",
        "https://www.lanacion.com.ar/",
        "https://www.elliberal.com.ar/",
        "https://www.ole.com.ar/",
        "https://tn.com.ar/",
        "https://www.cadena3.com/",
        "https://www.ellitoral.com/",
        "https://www.cronista.com/",
        "https://www.ciudad.com.ar/",
        "https://www.minutouno.com/",
        "https://www.lavoz.com.ar/",
        "https://www.mdzol.com/",
        "https://www.telam.com.ar/",
        "https://www.losandes.com.ar/",
        "https://www.losandes.com.ar/",
        "https://www.lacapital.com.ar/",
        "https://www.iprofesional.com/",
        "https://www.eldia.com/",
        "https://www.ambito.com/",
        "https://www.a24.com/",
        "https://www.cronica.com.ar/",
        "https://www.elonce.com/",
    ],
    "es-mx": [
        "https://www.eluniversal.com.mx/",
        "http://www.milenio.com/",
        "https://www.debate.com.mx/",
        "https://www.reforma.com/",
        "https://www.eleconomista.com.mx/",
        "https://www.mediotiempo.com/",
        "https://www.sdpnoticias.com/",
        "https://diario.mx/",
        "https://www.excelsior.com.mx/",
        "https://www.elsiglodetorreon.com.mx/",
        "https://www.elnorte.com/",
        "https://www.informador.mx/",
        "https://www.sinembargo.mx/",
        "https://www.elimparcial.com/",
        "http://www.zocalo.com.mx/",
        "https://www.proceso.com.mx/",
        "https://www.jornada.com.mx/",
        "https://expansion.mx/",
        "https://vanguardia.com.mx/",
        "https://mx.hola.com/",
    ],
    "es-es": [
        "https://elpais.com/",
        "https://www.20minutos.es/",
        "http://www.rtve.es/noticias/",
        "https://www.elmundo.es/",
        "https://www.abc.es/",
        "https://www.hola.com/",
        "https://www.elconfidencial.com/",
        "https://www.eleconomista.es/",
        "https://www.lavanguardia.com/",
        "https://www.expansion.com/",
        "https://www.larazon.es/",
        "https://www.elespanol.com/",
        "https://www.libertaddigital.com/",
        "https://www.publico.es/",
        "https://www.eldiario.es/",
        "https://www.europapress.es/",
        "http://www.huffingtonpost.es/",
        "https://www.elcorreo.com/",
        "https://www.elperiodico.com/es/",
        "https://cadenaser.com/",
        "https://www.lasprovincias.es/",
        "https://www.lne.es/",
        "https://www.lasexta.com/noticias/",
        "https://as.com/",
        "https://www.marca.com/",
    ],
    "en-us": [
        "https://edition.cnn.com/",
        "https://www.foxnews.com/",
        "https://abcnews.go.com/",
        "https://www.nytimes.com/",
        "https://www.huffpost.com/",
        "https://www.yahoo.com/news/",
        "https://eu.usatoday.com/",
        "https://www.latimes.com/",
        "https://www.forbes.com/",
        "https://www.washingtonpost.com/",
        "https://nypost.com/",
        "https://www.nbcnews.com/",
        "https://www.cbsnews.com/",
        "https://time.com/",
        "https://www.chicagotribune.com/",
        "https://www.sfgate.com/",
        "https://www.chron.com/",
        "https://www.wsj.com/",
        "https://www.npr.org/",
    ],
    "en-uk": [
        "https://www.espn.co.uk/",
        "https://www.bbc.co.uk/",
        "https://www.theguardian.com",
        "https://www.independent.co.uk/",
        "https://www.thesun.co.uk/",
        "https://www.dailymail.co.uk/",
        "https://news.sky.com/",
        "https://www.ft.com/",
        "https://www.mirror.co.uk/",
        "https://www.huffingtonpost.co.uk/",
        "https://www.dailystar.co.uk/",
        "https://www.standard.co.uk/",
        "https://www.spectator.co.uk/",
        "https://www.thetimes.co.uk/",
        "https://metro.co.uk/",
        "https://www.express.co.uk/",
        "https://www.dailyrecord.co.uk/",
        "https://www.walesonline.co.uk/",
        "https://www.reuters.com/",
        "https://inews.co.uk/",
    ],
}

def treat_url_and_should_visit(url, website_random):
    clean_website_random = website_random.replace("http://", "").replace("www.", "").replace("https://", "").replace("/", "")
    if url.startswith("http://"):
        if clean_website_random in url:
            return url
    if url.startswith("https://"):
        if clean_website_random in url:
            return url
    if url.startswith("www."):
        return False
    if url.startswith("/"):
        return website_random[:-1] + url
    print("Ignoring url {} {}".format(url, website_random))
    return False

def ignoring_crawling_text(url):
    if url.count("/") < 4 and url.count("-") == 0:
        return True
    return False

def save(data):
    for lang in NEWS_WEBSITES.keys():
        if lang in data:
            uid = str(uuid.uuid4()).split("-")[-1]
            with open(f"news/{lang}/{lang}_{uid}.txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join(data[lang]))

visited = set()
stacks = {}
data = {}
count = 0

try:
    while True:
        try:
            language_random = random.choice(list(NEWS_WEBSITES.keys()))
            website_random = random.choice(NEWS_WEBSITES[language_random])

            url = website_random
            if website_random in stacks:
                if len(stacks[website_random]):
                    url = stacks[website_random].pop()
                    random.shuffle(stacks[website_random])
                    stacks[website_random] = stacks[website_random][:100]

            url = treat_url_and_should_visit(url, website_random)

            if not url:
                continue

            if url in visited:
                continue

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
            }
            requested = requests.get(url, headers=headers, timeout=5)

            if requested.status_code != 200:
                print("{} bad status code {}".format(url, requested.status_code))

            if "text/html" not in requested.headers["content-type"]:
                print("not html {}".format(url))

            print(url)
            try:
                text = requested.text.encode('ISO-8859-1').decode("utf-8")
            except:
                text = requested.text
            soup = BeautifulSoup(text, "html.parser")

            a_elements = soup.find_all("a", href=True)
            hrefs = [x["href"] for x in a_elements]
            stacks.setdefault(website_random, []).extend(hrefs)

            if not ignoring_crawling_text(url):
                print(count, url)
                text = soup.get_text(separator="\n")
                text = re.sub("\n+", "\n", text)
                text = re.sub("\t+", "\n", text)
                text = re.sub("\s{3,}", "\n", text)

                text = text.split("\n")
                text = [line for line in text if len(line.split()) >= 3]
                uniques = set()
                uniques_text = []
                for line in text:
                    if line not in uniques:
                        uniques_text.append(line)
                        uniques.add(line)
                text = "\n".join(uniques_text)

                data.setdefault(language_random, []).append(text)
                count += 1

            visited.add(url)
        except Exception as error:
            print(error)

        if count >= 10000:
            save(data)
            count = 0
            data = {}

        time.sleep(0.1)
except KeyboardInterrupt:
    save(data)
    sys.exit(0)
