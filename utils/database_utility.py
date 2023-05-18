import pickledb


def get_db(database):
    db = pickledb.load(database, auto_dump=True)
    return db


def add_to_db(key, value):
    db = get_db("chat_db")
    db.set(key, value)


def get_from_db(key):
    db = get_db("chat_db")
    return db.get(key)
