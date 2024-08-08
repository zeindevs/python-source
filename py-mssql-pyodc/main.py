from sqlalchemy import text
from db import session


if __name__ == "__main__":
    result = session.execute(text("SELECT * FROM tb_offer"))

    for row in result:
        print(row)

    session.close()
