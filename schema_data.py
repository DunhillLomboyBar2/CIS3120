import sqlite3
def build_database(conn):
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Artist (
        artist_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        origin_city TEXT
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Track (
        track_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL,
        artist_id INTEGER NOT NULL
            REFERENCES Artist(artist_id)
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Playlist (
        playlist_id INTEGER PRIMARY KEY,
        playlist_name TEXT NOT NULL,
        owner_name TEXT NOT NULL
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS PlaylistTrack (
        playlist_id INTEGER NOT NULL REFERENCES Playlist(playlist_id),
        track_id INTEGER NOT NULL REFERENCES Track(track_id),
        position INTEGER NOT NULL,
        PRIMARY KEY (playlist_id, track_id)
    );
    """)

    conn.commit()

def seed_database(conn):
    # Artists
    artists = [
        (1, "Drake", "Hip-Hop", "Toronto"),
        (2, "Taylor Swift", "Pop", "Nashville"),
        (3, "The Weeknd", "R&B", "Toronto"),
        (4, "Kendrick Lamar", "Hip-Hop", "Compton"),
        (5, "Bad Bunny", "Reggaeton", "Puerto Rico"),
        (6, "Travis Scott", "Hip-Hop", "Houston"),
    ]

    conn.executemany("INSERT OR IGNORE INTO Artist VALUES (?, ?, ?, ?);", artists)

    # Tracks (18)
    tracks = [
        (1, "God's Plan", 198, 1),
        (2, "Hotline Bling", 267, 1),
        (3, "One Dance", 173, 1),

        (4, "Shake It Off", 242, 2),
        (5, "Blank Space", 231, 2),
        (6, "Love Story", 235, 2),

        (7, "Blinding Lights", 200, 3),
        (8, "Starboy", 230, 3),
        (9, "Save Your Tears", 215, 3),

        (10, "HUMBLE.", 177, 4),
        (11, "DNA.", 185, 4),
        (12, "Alright", 210, 4),

        (13, "Tití Me Preguntó", 240, 5),
        (14, "Moscow Mule", 230, 5),
        (15, "Me Porto Bonito", 210, 5),

        (16, "SICKO MODE", 312, 6),
        (17, "Goosebumps", 243, 6),
        (18, "Antidote", 261, 6),
    ]

    conn.executemany("INSERT OR IGNORE INTO Track VALUES (?, ?, ?, ?);", tracks)

    # Playlists
    playlists = [
        (1, "Workout", "Dunhill"),
        (2, "Chill", "Dunhill"),
        (3, "Hype", "Dunhill"),
        (4, "Late Night", "Dunhill"),
    ]

    conn.executemany("INSERT OR IGNORE INTO Playlist VALUES (?, ?, ?);", playlists)

    # PlaylistTrack (20+ entries)
    playlist_tracks = [
        (1, 1, 1), (1, 10, 2), (1, 16, 3), (1, 17, 4), (1, 11, 5),
        (2, 7, 1), (2, 8, 2), (2, 9, 3), (2, 5, 4), (2, 6, 5),
        (3, 13, 1), (3, 14, 2), (3, 15, 3), (3, 3, 4), (3, 2, 5),
        (4, 4, 1), (4, 6, 2), (4, 12, 3), (4, 18, 4), (4, 9, 5),
    ]

    conn.executemany("INSERT OR IGNORE INTO PlaylistTrack VALUES (?, ?, ?);", playlist_tracks)

    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    build_database(conn)
    seed_database(conn)

    # IntegrityError test
    try:
        conn.execute("INSERT INTO Track VALUES (999, 'Fake Song', 200, 9999)")
    except sqlite3.IntegrityError as e:
        print("IntegrityError caught:", e)

    # Save to file
    target = sqlite3.connect("music.db")
    conn.backup(target)
    target.close()

    print("Database created and saved as music.db")