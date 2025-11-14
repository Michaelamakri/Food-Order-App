from database_manager import DatabaseManager
db=DatabaseManager()
restaurants=[
    ("Rest1","Athens","Greece"),
    ("Rest2","Athens","Greece"),
    ("Rest3","Thessaloniki","Greece"),
    ("Rest4","Thessaloniki","Greece"),
    ("Rest5","Patras","Greece"),
    ("Rest6","Patras","Greece"),
    ("Rest7","Chania","Greece"),
    ("Rest8","Chania","Greece"),
]
for r in restaurants:
    db.execute("""
        INSERT INTO restaurants (name, city, country)
        VALUES (?, ?, ?)
    """, r)
