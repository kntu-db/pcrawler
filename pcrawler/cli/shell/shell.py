from typer import echo, colors, secho
from cmd import Cmd
from prettytable import PrettyTable

from pcrawler.data import Problem
from pcrawler.data.repository import ProblemRepository


def parse(line):
    return line.split()


def echo_row(columns, row):
    for i in range(len(columns)):
        echo(f"{columns[i]}: {row[i]}")


def echo_paged(result, start, length, key=None):
    t = PrettyTable(result.column_names)
    itr = iter(result)
    try:
        for _ in range((start - 1) * length):
            next(itr)
    except StopIteration:
        pass
    rows = []
    try:
        for _ in range(length):
            rows.append(next(itr))
    except StopIteration:
        pass
    if key:
        rows = sorted(rows, key=key, reverse=True)
    t.add_rows(rows)
    secho(t, fg=colors.MAGENTA)


class Shell(Cmd):
    intro = "Welcome to the PCrawler interactive shell. Type help or ? to list commands.\n"
    prompt = "PCrawler> "
    ruler = "-"

    def __init__(self):
        super().__init__()
        self.__repository = ProblemRepository()

    def do_problem_details(self, line):
        args = parse(line)
        if len(args) != 1:
            secho("Usage: problem_details <uid>", fg=colors.RED)
            return
        uid = args[0]
        echo(f"Fetching problem details for problem {uid}")
        with self.__repository.query("select * from problem where uid = '{}'".format(uid)) as rows:
            columns = rows.column_names
            for row in rows:
                echo_row(columns, row)
                secho("-" * 80, fg=colors.BLUE)

    # 1
    def do_problems_by_tag(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: problems_by_tag <tag>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        start = int(args[1]) if len(args) > 1 else 1
        length = int(args[2]) if len(args) > 2 else 10
        with self.__repository.query("select uid, tags "
                                     "from problem "
                                     "where tags contains '{}'".format(tag), length) as result:
            echo_paged(result, start, length)

    # 2
    def do_problems_by_solved_between(self, line):
        """
        View all problems that have solved count between specific numbers 
        """
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_solved_between <start> <end>[ <page> <len>]", fg=colors.RED)
            return
        start = int(args[0])
        end = int(args[1])
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems solved between {start} and {end}")
        with self.__repository.query("select uid, solved "
                                     "from problem "
                                     "where solved > {} and solved < {} "
                                     "allow filtering".format(start, end), length) as result:
            echo_paged(result, page, length)

    # 3
    def do_problems_by_difficulty_between(self, line):
        """
        View all problems that have difficulty between specific numbers
        """
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_difficulty_between <start> <end>[ <page> <len>]", fg=colors.RED)
            return
        start = int(args[0])
        end = int(args[1])
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems difficulty between {start} and {end}")
        with self.__repository.query("select uid, difficulty "
                                     "from problem "
                                     "where difficulty > {} and difficulty < {} "
                                     "allow filtering".format(start, end), length) as result:
            echo_paged(result, page, length)

    # 4
    def do_problems_by_tag_and_difficulty(self, line):
        """
        View all problems that have a specific tag and difficulty
        """
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_tag_and_difficulty <tag> <difficulty>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        difficulty = int(args[1])
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems with tag {tag} and difficulty {difficulty}")
        with self.__repository.query("select * "
                                     "from problem_by_tag_difficulty "
                                     "where tag = '{}' and difficulty = {}".format(tag, difficulty), length) as result:
            echo_paged(result, page, length)

    # 5
    def do_submit_statistics_by_tag_and_difficulty(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: difficulty_statistics_by_tag_and_difficulty <tag> <difficulty>", fg=colors.RED)
            return
        tag = args[0]
        difficulty = int(args[1])
        echo(f"Fetching difficulty statistics for tag {tag} and difficulty {difficulty}")
        with self.__repository.query("select min(total) as min, avg(total) as avg, max(total) as max "
                                     "from problem_by_tag_difficulty "
                                     "where tag='{}' and difficulty={}".format(tag, difficulty)) as result:
            echo_paged(result, 1, 1)

    # 6
    def do_accept_ratio_by_tag(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: accept_ratio_by_tag <tag>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        page = int(args[1]) if len(args) > 1 else 1
        length = int(args[2]) if len(args) > 2 else 10
        echo(f"Fetching accept ratio for tag {tag}")
        with self.__repository.query("select uid, solved * 100 / total as accept_ratio "
                                     "from problem_by_tag "
                                     "where tag='{}'".format(tag), length) as result:
            echo_paged(result, page, length)

    # 7
    def do_average_accept_ratio_by_site(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: average_accept_ratio_by_site <site>", fg=colors.RED)
            return
        site = args[0]
        echo(f"Fetching average accept ratio for site {site}")
        with self.__repository.query("select avg(solved * 100 / total) as average_accept_ratio "
                                     "from problem_by_site "
                                     "where site='{}'".format(site)) as result:
            echo_paged(result, 1, 1)

    # 7
    def do_average_accept_ratio_by_site_tag(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: average_accept_ratio_by_site_tag <site> <tag>", fg=colors.RED)
            return
        site = args[0]
        tag = args[1]
        echo(f"Fetching average accept ratio for site {site} and tag {tag}")
        with self.__repository.query("select avg(solved * 100 / total) as average_accept_ratio "
                                     "from problem_by_site_tag "
                                     "where site='{}' and tag='{}'".format(site, tag)) as result:
            echo_paged(result, 1, 1)

    # 8
    def do_tags_by_site(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: tags_by_site <site>[ <page> <len>]", fg=colors.RED)
            return
        site = args[0]
        page = int(args[1]) if len(args) > 1 else 1
        length = int(args[2]) if len(args) > 2 else 10
        echo(f"Fetching tags for site {site}")
        with self.__repository.query("select distinct site, tag "
                                     "from problem_by_site_tag "
                                     "where site='{}' "
                                     "allow filtering".format(site), length) as result:
            echo_paged(result, page, length)

    # 9
    def do_update_difficulty_by_uid(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: update_difficulty_by_uid <uid> <difficulty>", fg=colors.RED)
            return
        uid = args[0]
        difficulty = int(args[1])
        rows = self.__repository.unpaged_query("select time_step from problem where uid='{}'".format(uid))
        problems = []
        for row in rows:
            p = Problem()
            p.uid = uid
            p.difficulty = difficulty
            p.time_step = row[0]
            problems.append(p)

        echo(f"Updating difficulty for uid {uid} to {difficulty}")
        self.__repository.update(problems)

    # 10
    def do_update_difficulty_by_site_tags(self, line):
        args = parse(line)
        if len(args) < 3:
            secho("Usage: update_difficulty_by_site_tags <site> <tag> <difficulty>", fg=colors.RED)
            return
        site = args[0]
        tags = args[1:-1]
        difficulty = int(args[-1])
        rows = self.__repository.unpaged_query("select uid, time_step "
                                               "from problem_by_site_tag "
                                               "where site = '{}' "
                                               "and tag in ({})".format(site, ", ".join([f"'{tag}'" for tag in tags])))
        problems = []
        for row in rows:
            p = Problem()
            p.uid = row[0]
            p.difficulty = difficulty
            p.time_step = row[1]
            problems.append(p)
        echo(f"Updating difficulty for site {site} and tags {tags} to {difficulty}")
        self.__repository.update(problems)

    # 11
    def do_delete_by_site(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: delete_by_site <site>", fg=colors.RED)
            return
        site = args[0]

        rows = self.__repository.unpaged_query("select uid, time_step from problem_by_site where site='{}'".format(site))
        problems = []
        for row in rows:
            p = Problem()
            p.uid = row[0]
            p.time_step = row[1]
            problems.append(p)

        echo(f"Deleting problems for site {site}")
        self.__repository.delete(problems)

    # 13
    def do_problems_by_tag_order_by_solved(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: problems_by_tag_order_by_solved <tag>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        page = int(args[1]) if len(args) > 1 else 1
        length = int(args[2]) if len(args) > 2 else 10
        echo(f"Fetching problems for tag {tag}")
        with self.__repository.query("select * "
                                     "from problem_by_tag_solved "
                                     "where tag='{}'".format(tag), length) as result:
            echo_paged(result, page, length)

    # 13
    def do_problems_by_tag_and_difficulty_order_by_total(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_tag_and_difficulty_order_by_total <tag> <difficulty>[ <page> <len>]",
                  fg=colors.RED)
            return
        tag = args[0]
        difficulty = int(args[1])
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems for tag {tag} and difficulty {difficulty}")
        with self.__repository.query("select * "
                                     "from problem_by_tag_solved "
                                     "where tag='{}' and difficulty={} "
                                     "allow filtering".format(tag, difficulty), length) as result:
            echo_paged(result, page, length)

    # 14
    def do_problems_by_tag_order_by_total(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: problems_by_tag_order_by_total <tag>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        page = int(args[1]) if len(args) > 1 else 1
        length = int(args[2]) if len(args) > 2 else 10
        echo(f"Fetching problems for tag {tag}")
        with self.__repository.query("select * "
                                     "from problem_by_tag_total "
                                     "where tag='{}'".format(tag), length) as result:
            echo_paged(result, page, length)

    # 14
    def do_problems_by_tag_and_difficulty_order_by_total(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_tag_and_difficulty_order_by_total <tag> <difficulty>[ <page> <len>]", fg=colors.RED)
            return
        tag = args[0]
        difficulty = int(args[1])
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems for tag {tag} and difficulty {difficulty}")
        with self.__repository.query("select * "
                                     "from problem_by_tag_total "
                                     "where tag='{}' and difficulty={} "
                                     "allow filtering".format(tag, difficulty), length) as result:
            echo_paged(result, page, length)

    # 15
    def do_difficulty_statistics_by_tag(self, line):
        args = parse(line)
        if len(args) < 1:
            secho("Usage: difficulty_statistics_by_tag <tag>", fg=colors.RED)
            return
        tag = args[0]
        echo(f"Fetching difficulty statistics for tag {tag}")
        with self.__repository.query("select min(difficulty) as min_difficulty, avg(difficulty) as avg_difficulty, max(difficulty) as max_difficulty "
                                     "from problem_by_tag "
                                     "where tag = '{}'".format(tag)) as result:
            echo_paged(result, 1, 1)

    # 16
    def do_tags_order_by_average_difficulty(self, line):
        args = parse(line)
        page = int(args[0]) if len(args) > 0 else 1
        length = int(args[1]) if len(args) > 1 else 10
        echo(f"Fetching tags ordered by average difficulty")
        with self.__repository.query("select tag, avg(difficulty) as average_difficulty "
                                     "from problem_by_tag "
                                     "group by tag", length) as result:
            echo_paged(result, page, length, key=lambda row: row[1])

    # 17
    def do_sites_order_by_average_difficulty(self, line):
        args = parse(line)
        page = int(args[0]) if len(args) > 0 else 1
        length = int(args[1]) if len(args) > 1 else 10
        echo(f"Fetching sites ordered by average difficulty")
        with self.__repository.query("select site, avg(difficulty) as average_difficulty "
                                     "from problem_by_site "
                                     "group by site", length) as result:
            echo_paged(result, page, length, lambda row: row[1])

    # 18
    def do_tags_order_by_accept_ratio(self, line):
        args = parse(line)
        page = int(args[0]) if len(args) > 0 else 1
        length = int(args[1]) if len(args) > 1 else 10
        echo(f"Fetching tags ordered by accept ratio")
        with self.__repository.query("select tag, sum(solved) / sum(total) as ratio "
                                     "from problem_by_tag "
                                     "where total > 0"
                                     "group by tag "
                                     "allow filtering", length) as result:
            echo_paged(result, page, length, key=lambda row: row[1])

    # 19
    def do_problems_by_sites_tag(self, line):
        args = parse(line)
        if len(args) < 2:
            secho("Usage: problems_by_sites_tag <sites> <tag>[ <page> <len>]", fg=colors.RED)
            return
        sites = args[0].split(",")
        tag = args[1]
        page = int(args[2]) if len(args) > 2 else 1
        length = int(args[3]) if len(args) > 3 else 10
        echo(f"Fetching problems for site {sites} and tag {tag}")
        with self.__repository.query("select * "
                                     "from problem_by_site_tag "
                                     "where site in ({}) and tag = '{}'".format(', '.join([f"'{site}'" for site in sites]), tag), length) as result:
            echo_paged(result, page, length)
