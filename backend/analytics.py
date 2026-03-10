from collections import Counter
try:
    import psycopg2  # type: ignore
except ImportError:
    raise ImportError("psycopg2 is required; install it with: pip install psycopg2-binary")

def issue_stats():

    conn = psycopg2.connect(
        database="jira_reports",
        user="postgres",
        password="sassy",   # use the same password you set in PostgreSQL
        host="localhost",
        port="5432"
    )

    query = "SELECT status FROM issues"

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            statuses = [r[0] if r[0] is not None else "UNKNOWN" for r in rows]
            result = Counter(statuses)
            return dict(result)
    finally:
        conn.close()