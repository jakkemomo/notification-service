SQL_USER_IDS = """
SELECT DICTINCT user_id FROM views WHERE event_time < {0}
UNION
SELECT DICTINCT user_id FROM favorites WHERE event_time < {0}
UNION
SELECT DICTINCT user_id FROM reviews WHERE event_time < {0}
"""

SQL_VIEWS = "SELECT COUNT(*) FROM views WHERE user_id={0} AND event_time < {1}"

SQL_RATINGS = "SELECT COUNT(*) FROM ratings WHERE user_id={0} AND event_time < {1}"

SQL_REVIEWS = "SELECT COUNT(*) FROM reviews WHERE user_id={0} AND event_time < {1}"
