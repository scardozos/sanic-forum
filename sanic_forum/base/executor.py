from mayim import PostgresExecutor


class BaseExecutor(PostgresExecutor):
    @staticmethod
    def is_query_name(name: str):
        """Allows us to use queries that don't start only with
        select, insert, update or delete.
        """
        return True
