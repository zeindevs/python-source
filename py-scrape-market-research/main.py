import logging
import csv
import json
from curl_cffi import requests
from db import SessionLocal, init_db
from models import Product, Offer
from rich import print
from rich.logging import RichHandler
from extruct.jsonld import JsonLdExtractor
from sqlalchemy.exc import IntegrityError


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


def get_urls():
    with open("urls.csv", "r") as f:
        reader = csv.reader(f)
        urls = [url[0] for url in reader]
        f.close()
    return urls


def get_html(url: str):
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
    # }
    # # resp = httpx.get(url, headers=headers)
    resp = requests.get(url, impersonate="chrome120")
    if resp.status_code != 200:
        logging.info(f"url {url} responded with bad status code {resp.status_code}")
    else:
        jslde = JsonLdExtractor()
        data = jslde.extract(resp.text)
        return data


def load_offers(session, data):
    product = session.query(Product).filter(Product.sku == data["sku"]).first()
    if isinstance(data["offers"], list):
        for offer in data["offers"]:
            if offer["sku"] == product.sku:
                new_offer = Offer(
                    price=offer["highPrice"],
                    availability=offer.get("availability"),
                    product_id=product.id,
                )
                try:
                    session.add(new_offer)
                    session.commit()
                    offerr = session.refresh(new_offer)
                    return offerr
                except IntegrityError as err:
                    logging.warn(f"{err}")
                    session.rollback()
                    return new_offer
    else:
        new_offer = Offer(
            price=data["offers"]["highPrice"],
            availability=data["offers"].get("availability"),
            product_id=product.id,
        )
        try:
            session.add(new_offer)
            session.commit()
            offerr = session.refresh(new_offer)
            return offerr
        except IntegrityError as err:
            logging.warn(f"{err}")
            session.rollback()
            return new_offer


def load_product(session, data):
    exist = session.query(Product).filter(Product.sku == data["sku"]).first()
    if exist:
        return exist
    new_product = Product(
        name=data["name"],
        url=data.get("url"),
        description=data.get("description"),
        sku=data.get("sku"),
        brand=data["brand"]["name"],
    )
    try:
        session.add(new_product)
        session.commit()
        product = session.refresh(new_product)
        return product
    except IntegrityError as err:
        logging.warn(f"{err}")
        session.rollback()
        return new_product


def main():
    urls = get_urls()
    session = SessionLocal()
    for url in urls:
        product_data = get_html(url)
        if product_data:
            for data in product_data:
                with open("data.json", "w") as f:
                    f.write(json.dumps(data, indent=2))
                    f.close()
                if "offers" in data:
                    load_product(session, data)
                    load_offers(session, data)


if __name__ == "__main__":
    init_db()
    main()
