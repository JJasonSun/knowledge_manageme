import sys
import os
import json
import csv
from sqlalchemy import text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import QuestionsSessionLocal


def normalize_metadata(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def summarize_metadata(metadata):
    if metadata is None:
        return {"type": "null"}
    if isinstance(metadata, dict):
        summary = {"keys": sorted(metadata.keys())}
        for key in ["options", "questions", "blanks"]:
            if key not in metadata:
                continue
            value = metadata.get(key)
            if isinstance(value, list):
                if not value:
                    summary[key] = {"item_type": "empty"}
                    continue
                first = value[0]
                if isinstance(first, dict):
                    summary[key] = {"item_type": "object", "item_keys": sorted(first.keys())}
                else:
                    summary[key] = {"item_type": type(first).__name__}
            else:
                summary[key] = {"item_type": type(value).__name__}
        return summary
    return {"type": type(metadata).__name__}


def fetch_type_rows(db, schema, exercise_table, type_table, sample_per_type):
    sql = text(
        f"""
        WITH type_list AS (
            SELECT id, name, display_name
            FROM {schema}.{type_table}
        ),
        ranked AS (
            SELECT
                et.name AS type_name,
                et.display_name AS type_display_name,
                e.id AS exercise_id,
                e.metadata AS metadata,
                ROW_NUMBER() OVER (PARTITION BY et.name ORDER BY e.id) AS rn
            FROM {schema}.{exercise_table} e
            JOIN type_list et ON e.exercise_type_id = et.id
            WHERE e.metadata IS NOT NULL
        )
        SELECT
            t.name AS type_name,
            t.display_name AS type_display_name,
            r.exercise_id AS exercise_id,
            r.metadata AS metadata,
            r.rn AS rn
        FROM type_list t
        LEFT JOIN ranked r ON r.type_name = t.name AND r.rn <= :sample_per_type
        ORDER BY t.name, r.rn
        """
    )
    return db.execute(sql, {"sample_per_type": sample_per_type}).fetchall()


def write_csv(rows, output_path, delimiter):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["type_name", "display_name", "exercise_id", "metadata_summary", "metadata_json"])
        for row in rows:
            type_name, display_name, exercise_id, metadata, _ = row
            normalized = normalize_metadata(metadata)
            summary = summarize_metadata(normalized)
            writer.writerow(
                [
                    type_name,
                    display_name or "",
                    str(exercise_id) if exercise_id else "",
                    json.dumps(summary, ensure_ascii=False),
                    json.dumps(normalized, ensure_ascii=False),
                ]
            )


def main():
    sample_per_type = 2
    if len(sys.argv) > 1:
        try:
            sample_per_type = int(sys.argv[1])
        except Exception:
            sample_per_type = 2
    if not QuestionsSessionLocal:
        print("QuestionsSessionLocal 未初始化，请检查 SSH 隧道与题目数据库配置")
        return
    db = QuestionsSessionLocal()
    try:
        content_rows = fetch_type_rows(db, "content_new", "exercises", "exercise_types", sample_per_type)
        content_output = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "docs", "题型_content.csv")
        )
        write_csv(content_rows, content_output, "\t")
        print(f"已输出题型 metadata 样例到: {content_output}")

        scenario_rows = fetch_type_rows(db, "scenario_learning_v2", "sl_exercises", "sl_exercise_types", sample_per_type)
        scenario_output = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "docs", "题型_sl.csv")
        )
        write_csv(scenario_rows, scenario_output, ",")
        print(f"已输出情境题型 metadata 样例到: {scenario_output}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
