import sqlite3


class ChatHistory:
    def __init__(self, db_path: str = "chat_history.db"):
        # Connettiamoci al database (se non esiste, lo crea)
        # check_same_thread=False è essenziale per FastAPI perché usa thread multipli
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def add_message(self, session_id: str, role: str, content: str):
        # TO-DO: Esegui un INSERT per salvare il messaggio. Usa le query parametrizzate (?)
        # per evitare SQL injection, es: self.cursor.execute("INSERT INTO...", (var1, var2, var3))
        self.cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )
        self.conn.commit()

    def get_messages(self, session_id: str) -> list[dict]:
        # TO-DO: Fai una SELECT filtrando per session_id e restituendo
        # una lista di dizionari nel formato [{"role": "user", "content": "ciao"}, ...]
        self.cursor.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        )
        rows = self.cursor.fetchall()
        return [{"role": row[0], "message": row[1]} for row in rows]

    def close(self):
        self.conn.close()
