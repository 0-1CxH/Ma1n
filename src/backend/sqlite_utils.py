import sqlite3

def sqlite_connect_and_execute(db_path, sql, args=None, fetch="none"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if args is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, args)
    if fetch == "one":
        result = cursor.fetchone()
    elif fetch == "all":
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    cursor.close()
    conn.close()
    return result

