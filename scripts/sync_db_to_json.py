#!/usr/bin/env python3
"""Regenerar data/mensajes.json desde data/mensajes.db.
Uso: python scripts/sync_db_to_json.py
"""
from __future__ import annotations
import sqlite3
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, 'data', 'mensajes.db')
OUT_PATH = os.path.join(ROOT, 'data', 'mensajes.json')

if not os.path.exists(DB_PATH):
    print(f"Database not found: {DB_PATH}")
    sys.exit(2)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('SELECT * FROM mensajes ORDER BY id ASC')
rows = cur.fetchall()
msgs = []
for row in rows:
    d = {}
    for k in row.keys():
        v = row[k]
        if isinstance(v, bytes):
            try:
                v = v.decode('utf-8')
            except Exception:
                v = v.decode('latin-1', errors='ignore')
        d[k] = v
    msgs.append(d)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(msgs, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(msgs)} messages to {OUT_PATH}')
if len(msgs) > 0:
    print(json.dumps(msgs[:5], ensure_ascii=False, indent=2))

conn.close()
