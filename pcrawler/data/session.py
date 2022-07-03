from cassandra.cluster import Cluster


class SessionProvider:
    KEY_SPACE = "problems"

    def __init__(self):
        self.cluster = Cluster()

    def get_session(self):
        return self.cluster.connect(self.KEY_SPACE)



