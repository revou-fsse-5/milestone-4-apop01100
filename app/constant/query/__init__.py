class Query:
    @staticmethod
    def reset_primary_key(table):
        return f"ALTER TABLE {table} AUTO_INCREMENT = 1;"