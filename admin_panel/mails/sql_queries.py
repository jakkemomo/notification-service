SQL_USER_IDS = """
SELECT DISTINCT user_id FROM movies.views WHERE event_time > {0}
UNION ALL
SELECT DISTINCT user_id FROM movies.ratings WHERE event_time > {0}
UNION ALL
SELECT DISTINCT user_id FROM movies.reviews WHERE event_time > {0}
"""

SQL_VIEWS = "SELECT movie_id FROM movies.views WHERE user_id='{0}' AND event_time > {1}"

SQL_RATINGS = (
    "SELECT movie_id FROM movies.ratings WHERE user_id='{0}' AND event_time > {1}"
)

SQL_REVIEWS = (
    "SELECT movie_id FROM movies.reviews WHERE user_id='{0}' AND event_time > {1}"
)
