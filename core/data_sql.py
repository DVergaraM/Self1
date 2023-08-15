from .SQL import Icons, Activities, Urls
_sql = Icons()
_conn = _sql.create_connection()
with _conn:
    Second_Brain = _sql.get_path(_sql.get_id("Second_Brain"))
    Discord = _sql.get_path(_sql.get_id("Discord"))
del _sql, _conn

_sql = Urls()
_conn = _sql.create_connection()
with _conn:
    urls = _sql.get_all()

del _sql, _conn

activities_dict: dict[int, dict] = {
    0: {},
    1: {},
    2: {},
}

_sql = Activities()
_conn = _sql.create_connection()
with _conn:
    for key in activities_dict.keys():
        activities_dict[key]["Image_URL"] = _sql.get_imageurl(key+1)
        activities_dict[key]["Description"] = _sql.get_description(key+1)
        activities_dict[key]["Small_text"] = _sql.get_smalltext(key+1)

del _sql, _conn

