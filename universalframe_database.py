
import sqlite3

class confanddata:

    con = None
    cur = None

    created = False

    def opendb(self):        
        self.con = sqlite3.connect("universalframe_confanddata.sqlite3")
        self.cur = self.con.cursor()
        if not self.created:
            self.con.execute("""CREATE TABLE IF NOT EXISTS configuration (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    ivalue INTEGER,
                    rvalue REAL,
                    tvalue TEXT
                    )""")
            self.con.commit()
            self.con.execute("""CREATE TABLE IF NOT EXISTS dataki1 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    rvalue1 REAL,
                    rvalue2 REAL,
                    rvalue3 REAL,
                    rvalue4 REAL,
                    rvalue5 REAL,
                    rvalue6 REAL,
                    bvalue1 INTEGER,
                    bvalue2 INTEGER
                    )""")
            self.con.commit()
            self.created = True
        
    def closedb(self): self.con.close()

    def droptables(self, tables):
        for table in tables:
            try: res = self.con.execute("DROP TABLE " + table)
            except: pass

    def setvalues(self, table: str, keyandvalues: list, field: str = "") -> int:

        """
        Args:
            table: selbsterklärend
            keyandvalues: list of tuples
                [(key1, ivalue1, rvalue1, tvalue1), (key2, ivalue2, rvalue2, tvalue2), ...]
                [(key1, rvalue11, rvalue21, rvalue31, rvalue41, rvalue51, rvalue61, bvalue11, bvalue21), ...]
            field: wenn Feldname übergeben, dann nur für diesen Update
        Returns:
            int: Anzahl nicht gesetzter Datensätze
        Description:
            zuerst wird versucht einen Tupel als neuen Datensatz zu setzen
            ist der Key aber schon vorhanden, werden dessen Values aktualisiert
        """

        tableavailable = True
        if table == "configuration":
            fields = "(key, ivalue, rvalue, tvalue)"
            values = "(?, ?, ?, ?)"
        elif table == "dataki1":
            fields = "(key, rvalue1, rvalue2, rvalue3, rvalue4, rvalue5, rvalue6, bvalue1, bvalue2)"
            values = "(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        else:
            tableavailable = False
            return len(keyandvalues)

        if tableavailable:
            notset = 0
            for row in keyandvalues:
                if field == "":
                    try:
                        #print(f"INSERT INTO {table}{fields} VALUES{values}")
                        self.con.execute(f"INSERT INTO {table}{fields} VALUES{values}", row)
                        # executemany erst mal gestrichen, weil bei Nicht-Eindeutigkeit crasht das Ganze
                        self.con.commit()
                    except:
                        if table == "configuration": setvalues = f"ivalue={row[1]}, rvalue={row[2]}, tvalue='{row[3]}'"
                        elif table == "dataki1": setvalues = f"rvalue1={row[1]}, rvalue2={row[2]}, rvalue3={row[3]}, rvalue4={row[4]}, rvalue5={row[5]}, rvalue6={row[6]}, bvalue1={row[7]}, bvalue2={row[8]}"
                        else: break
                        try:
                            #print(f"UPDATE {table} SET {setvalues} WHERE key='{row[0]}'")
                            self.con.execute(f"UPDATE {table} SET {setvalues} WHERE key='{row[0]}'")
                            self.con.commit()
                        except: notset += 1
                else:
                    try:
                        self.con.execute(f"INSERT INTO {table}(key,{field}) VALUES(?, ?)", row)
                        self.con.commit()
                    except:
                        if field[:6] == "tvalue": textmarker = "'"
                        else: textmarker = ""
                        try:
                            self.con.execute(f"UPDATE {table} SET {field}={textmarker}{row[1]}{textmarker} WHERE key='{row[0]}'")
                            self.con.commit()
                        except: notset += 1
            return notset

    def getvalues(self, table: str, keys: tuple = "", field: str = ""):
        """
        Args:
            table: selbsterklärend
            keys: leer (gesamte Tabelle ausgeben) oder Tupel of strings (gezielte Ausgabe)
                (key1, key2, ...)
            field:
                "" es wird alles gefundene zurückgegeben (mit Keys)
                    [(key1, ivalue1, rvalue1, tvalue1), (key2, ivalue2, rvalue2, tvalue2), ...]
                "field" es werden die Einzelwerte zurückgegeben
                    [ivalue1, ivalue2, ivalue3, tvalue4, ...]
        """
        if keys == "":
            if table == "configuration": fields = "key, ivalue, rvalue, tvalue"
            elif table == "dataki1": fields = "key, rvalue1, rvalue2, rvalue3, rvalue4, rvalue5, rvalue6, bvalue1, bvalue2"
            else: fields = "*"
            res = self.con.execute(f"SELECT {fields} FROM {table}")
            rows = res.fetchall()
            return rows
        else:
            operation = lambda keys: "=" if isinstance(keys, str) else "in"
            keyvalue = lambda keys: "'" + keys + "'" if isinstance(keys, str) else keys
            if field == "":
                #print(f"SELECT * FROM {table}} WHERE key {operation(keys)} {keyvalue(keys)}")
                res = self.con.execute(f"SELECT * FROM {table} WHERE key {operation(keys)} {keyvalue(keys)}")
                rows = res.fetchall()
                # das gebe ich so aus wie es ist
                return rows
            else:
                #print(f"SELECT {field} FROM {table} WHERE key {operation(keys)} {keyvalue(keys)}")
                res = self.con.execute(f"SELECT {field} FROM {table} WHERE key {operation(keys)} {keyvalue(keys)}")
                rows = res.fetchall()
                # das wandle ich in eine aufgeräumte Liste um
                if rows != []: rows = [x[0] for x in rows]
                return rows

    def getcount(self, table: str, keys: tuple = "", like: bool = False) -> int:
        """
        Args:
            table: selbsterklärend
            keys: leer (Gesamtanzahl ermitteln) oder Tupel of strings (gezielt zählen)
                (key1, key2, ...)
            like: Gleichheitssuche (mit = oder IN)
                  oder Like (Wildcards % oder _ müssen in keys gesetzt sein)
                    %: Stellt eine beliebige Anzahl von Zeichen dar.
                    _: Stellt ein einzelnes Zeichen dar.
        Returns:
            int: Anzahl gefundener Datensätze
        """
        if like:
            query = ""
            for key in keys: query += f"(key LIKE '{key}') OR "
            query = query[:len(query)-4]
            #print(f"SELECT COUNT(*) FROM {table}} WHERE {query}")
            res = self.con.execute(f"SELECT COUNT(*) FROM {table} WHERE {query}")
        elif keys == "":
            #print(f"SELECT COUNT(*) FROM {table}")
            res = self.con.execute(f"SELECT COUNT(*) FROM {table}")
        else:
            operation = lambda keys: "=" if isinstance(keys, str) else "in"
            keyvalue = lambda keys: "'" + keys + "'" if isinstance(keys, str) else keys
            #print(f"SELECT COUNT(*) FROM {table} WHERE key {operation(keys)} {keyvalue(keys)}")
            res = self.con.execute(f"SELECT COUNT(*) FROM {table} WHERE key {operation(keys)} {keyvalue(keys)}")
        rows = res.fetchone()
        # das gebe ich so aus wie es ist
        return rows[0]
