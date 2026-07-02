from services.memory_service import cursor, conn


def activity_exists(strava_activity_id):
    cursor.execute(
        """
        SELECT 1
        FROM activities
        WHERE strava_activity_id = ?
        """,
        (strava_activity_id,)
    )

    return cursor.fetchone() is not None


def save_activity(phone, activity):

    cursor.execute(
        """
        INSERT INTO activities
        (
            strava_activity_id,
            phone,
            name,
            start_date,
            distance,
            moving_time,
            elapsed_time,
            average_speed,
            max_speed,
            average_heartrate,
            max_heartrate,
            total_elevation_gain,
            activity_type
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            activity["id"],
            phone,
            activity.get("name"),
            activity.get("start_date"),
            activity.get("distance"),
            activity.get("moving_time"),
            activity.get("elapsed_time"),
            activity.get("average_speed"),
            activity.get("max_speed"),
            activity.get("average_heartrate"),
            activity.get("max_heartrate"),
            activity.get("total_elevation_gain"),
            activity.get("type"),
        )
    )

    conn.commit()


def get_last_activity(phone):

    cursor.execute(
        """
        SELECT *
        FROM activities
        WHERE phone = ?
        ORDER BY start_date DESC
        LIMIT 1
        """,
        (phone,)
    )

    row = cursor.fetchone()

    return dict(row) if row else None


def get_recent_runs(phone, limit=10):

    cursor.execute(
        """
        SELECT *
        FROM activities
        WHERE phone = ?
        ORDER BY start_date DESC
        LIMIT ?
        """,
        (phone, limit)
    )

    return [dict(row) for row in cursor.fetchall()]


def get_unanalyzed_activities():

    cursor.execute(
        """
        SELECT *
        FROM activities
        WHERE analyzed = 0
        ORDER BY start_date ASC
        """
    )

    return [dict(row) for row in cursor.fetchall()]


def mark_analyzed(strava_activity_id):

    cursor.execute(
        """
        UPDATE activities
        SET analyzed = 1
        WHERE strava_activity_id = ?
        """,
        (strava_activity_id,)
    )

    conn.commit()


def delete_activity(strava_activity_id):

    cursor.execute(
        """
        DELETE
        FROM activities
        WHERE strava_activity_id = ?
        """,
        (strava_activity_id,)
    )

    conn.commit()


def activity_count(phone):

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM activities
        WHERE phone = ?
        """,
        (phone,)
    )

    return cursor.fetchone()["total"]