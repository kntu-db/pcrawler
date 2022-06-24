from .base import AbstractApiExplorer
from ..data import Problem
from json import loads
from asyncio import gather, ensure_future


class LeetCodeApiExplorer(AbstractApiExplorer):
    __GRAPHQL_ENDPOINT = 'https://leetcode.com/graphql'

    __GRAPHQL_PROBLEM_SET_QUERY = '''
query problemsetQuestionList(
  $categorySlug: String
  $limit: Int
  $skip: Int
  $filters: QuestionListFilterInput
) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      acRate
      difficulty
      freqBar
      frontendQuestionId: questionFrontendId
      isFavor
      paidOnly: isPaidOnly
      status
      title
      titleSlug
      topicTags {
        name
        id
        slug
      }
      hasSolution
      hasVideoSolution
    }
  }
}
'''

    __GRAPHQL_PROBLEM_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    boundTopicId
    title
    titleSlug
    content
    translatedTitle
    translatedContent
    isPaidOnly
    difficulty
    likes
    dislikes
    isLiked
    similarQuestions
    exampleTestcases
    categoryTitle
    contributors {
      username
      profileUrl
      avatarUrl
      __typename
    }
    topicTags {
      name
      slug
      translatedName
      __typename
    }
    companyTagStats
    codeSnippets {
      lang
      langSlug
      code
      __typename
    }
    stats
    hints
    solution {
      id
      canSeeDetail
      paidOnly
      hasVideoSolution
      paidOnlyVideo
      __typename
    }
    status
    sampleTestCase
    metaData
    judgerAvailable
    judgeType
    mysqlSchemas
    enableRunCode
    enableTestMode
    enableDebugger
    envInfo
    libraryUrl
    adminUrl
    challengeQuestion {
      id
      date
      incompleteChallengeCount
      streakCount
      type
      __typename
    }
    __typename
  }
}
"""

    PAGE_SIZE = 50

    @staticmethod
    def __json_to_problem(data):
        p = Problem()
        p.id = data['questionId']
        p.title = data['title']
        p.tags = [tag['name'] for tag in data['topicTags']]
        p.difficulty_class = data['difficulty']
        status = loads(data['stats'])
        p.solved = status['totalAcceptedRaw']
        p.total = status['totalSubmissionRaw']
        return p

    async def __fetch_problem(self, title_slug):
        query = {
            "query": self.__GRAPHQL_PROBLEM_QUERY,
            "operationName": "questionData",
            "variables": {"titleSlug": title_slug}
        }
        async with self.post(self.__GRAPHQL_ENDPOINT, json=query) as resp:
            data = await resp.json()
        return LeetCodeApiExplorer.__json_to_problem(data['data']['question'])

    async def __fetch_list(self, skip, limit):
        query = {
            "query": self.__GRAPHQL_PROBLEM_SET_QUERY,
            "variables": {"categorySlug": "", "skip": skip, "limit": limit, "filters": {}}
        }
        async with self.post(self.__GRAPHQL_ENDPOINT, json=query) as resp:
            data = await resp.json()
            return data['data']['problemsetQuestionList']['questions']

    async def page(self, page_number):
        questions = await self.__fetch_list((page_number - 1) * self.PAGE_SIZE, self.PAGE_SIZE)
        tasks = []
        for question in questions:
            tasks.append(ensure_future(self.__fetch_problem(question['titleSlug'])))
        results = await gather(*tasks)
        return results
