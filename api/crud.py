from . import schemas, database
from typing import List

def get_top_products(limit: int):
    query = '''
        SELECT detected_object_label AS product, COUNT(*) AS count
        FROM fct_image_detections
        GROUP BY detected_object_label
        ORDER BY count DESC
        LIMIT %s
    '''
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
    return [schemas.TopProduct(product=row[0], count=row[1]) for row in rows]

def get_channel_activity(channel_name: str):
    query = '''
        SELECT date::date, COUNT(*) AS count
        FROM fct_messages
        WHERE channel = %s
        GROUP BY date::date
        ORDER BY date::date
    '''
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (channel_name,))
            rows = cur.fetchall()
    if not rows:
        return None
    return schemas.ChannelActivity(
        channel=channel_name,
        activity=[{"date": row[0].strftime("%Y-%m-%d"), "count": row[1]} for row in rows]
    )

def search_messages(query: str):
    sql = '''
        SELECT id, channel, date, message
        FROM fct_messages
        WHERE message ILIKE %s
    '''
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f"%{query}%",))
            rows = cur.fetchall()
    return [
        schemas.MessageSearchResult(
            message_id=row[0],
            channel=row[1],
            date=row[2],
            message=row[3]
        ) for row in rows
    ]
