from cassandra.query import SimpleStatement

from pcrawler.data.session import SessionProvider


class Query:
    def __init__(self, session, query, fetch_size=10):
        self.__session = session
        self.__query = query
        self.__fetch_size = fetch_size

    def __enter__(self):
        return self.__session.execute(SimpleStatement(self.__query, fetch_size=self.__fetch_size))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.shutdown()


class ProblemRepository:
    def __init__(self):
        self.session_provider = SessionProvider()

    def insert(self, data):
        if data is None:
            return
        problems = None
        try:
            iter(data)
            problems = data
        except TypeError:
            problems = [data]
        if len(problems) == 0:
            return

        keys = problems[0].__dict__.keys()

        with self.session_provider.get_session() as session:
            insert_into_problem_stmt = session.prepare(
                f"INSERT INTO problem ({', '.join(keys)}) values ({', '.join(['?'] * len(keys))})")
            insert_into_problem_by_tag_stmt = session.prepare(
                "insert into problem_by_tag(tag, uid, time_step, site, title, difficulty, solved, total) "
                "values (?, ?, ?, ?, ?, ?, ?, ?)")

            for problem in problems:
                session.execute(insert_into_problem_stmt, problem.__dict__)
                for tag in problem.tags:
                    values = {'tag': tag, **problem.__dict__}
                    session.execute(insert_into_problem_by_tag_stmt, values)

    def update(self, data):
        if data is None:
            return
        problems = None
        try:
            iter(data)
            problems = data
        except TypeError:
            problems = [data]
        if len(problems) == 0:
            return

        keys = problems[0].__dict__.keys() - {'uid', 'time_step'}

        with self.session_provider.get_session() as session:
            update_stmt = session.prepare(
                f"UPDATE problem SET {', '.join([f'{key} = ?' for key in keys])} WHERE uid = ? and time_step = ?")
            for problem in problems:
                session.execute(update_stmt, problem.__dict__)

    def delete(self, data):
        if data is None:
            return
        problems = None
        try:
            iter(data)
            problems = data
        except TypeError:
            problems = [data]
        if len(problems) == 0:
            return

        keys = problems[0].__dict__.keys() - {'uid', 'time_step'}

        with self.session_provider.get_session() as session:
            delete_stmt = session.prepare(
                f"DELETE FROM problem WHERE uid = ? and time_step = ?")
            for problem in problems:
                session.execute(delete_stmt, problem.__dict__)


    def query(self, query, fetch_size=10):
        return Query(self.session_provider.get_session(), query, fetch_size)

    def unpaged_query(self, query):
        with self.session_provider.get_session() as session:
            return session.execute(SimpleStatement(query))
