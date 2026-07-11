import json
import sqlite3

DB_PATH = r"backend/database/attendance.db"
EXPECTED_SIZE = 512

db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row

rows = db.execute(
    "SELECT id, vector FROM embeddings"
).fetchall()

fixed = 0
deleted = 0

for row in rows:
    embedding_id = row["id"]

    try:
        value = json.loads(row["vector"])

        # Flatten one unnecessary nested list, such as [[...512 values...]]
        if (
            isinstance(value, list)
            and len(value) == 1
            and isinstance(value[0], list)
        ):
            value = value[0]

        if not isinstance(value, list):
            raise ValueError("vector is not a list")

        # Reject irregular nested values
        if any(isinstance(item, (list, dict)) for item in value):
            raise ValueError("vector contains nested values")

        vector = [float(item) for item in value]

        if len(vector) != EXPECTED_SIZE:
            raise ValueError(
                f"expected {EXPECTED_SIZE} values, found {len(vector)}"
            )

        db.execute(
            "UPDATE embeddings SET vector = ? WHERE id = ?",
            (json.dumps(vector), embedding_id),
        )

        fixed += 1
        print(f"Valid embedding {embedding_id}: {len(vector)} values")

    except Exception as error:
        print(f"Deleting embedding {embedding_id}: {error}")

        db.execute(
            "DELETE FROM embeddings WHERE id = ?",
            (embedding_id,),
        )

        deleted += 1

db.commit()
db.close()

print()
print(f"Valid/fixed: {fixed}")
print(f"Deleted malformed: {deleted}")