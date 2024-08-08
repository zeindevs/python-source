from sqlalchemy import insert
from db import tb_offer, session, metadata, engine


metadata.create_all(engine)

offer_insert_stmt = insert(tb_offer).values(
    [
        {
            "name": "Full Stack Developer",
            "description": "",
            "location": "Central Jakarta",
            "sallary": 15000000,
        },
        {
            "name": "Front End Developer",
            "description": "",
            "location": "South Jakarta",
            "salary": 12000000,
        },
        {
            "name": "Back End Developer",
            "description": "",
            "location": "West Jakarta",
            "salary": 20000000,
        },
    ]
)

session.execute(offer_insert_stmt)
session.commit()
