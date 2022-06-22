from aiohttp import ClientSession
from asyncio import ensure_future, run, gather
from logger import error, info

"""
Simple code for crawling leetcode.com
"""

query_string = '''
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

one_problem_query_string = """
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

LEETCODE_GRAPHQL_ENDPOINT = 'https://leetcode.com/graphql'

query = {
    "query": query_string,
    "variables": {"categorySlug": "", "skip": 0, "limit": 50, "filters": {}}}

one_problem_query = {
    "query": one_problem_query_string,
    "operationName": "questionData"
}


async def fetch_list(session):
    async with session.post(LEETCODE_GRAPHQL_ENDPOINT, json=query) as resp:
        data = await resp.json()
        return data['data']['problemsetQuestionList']['questions']


async def fetch_one(session, title_slug):
    info('Fetching {}'.format(title_slug))
    try:
        async with session.post(LEETCODE_GRAPHQL_ENDPOINT,
                                json=one_problem_query | {"variables": {"titleSlug": title_slug}}) as resp:
            data = await resp.json()
            info('Fetched {}'.format(title_slug))
            return data['data']['question']
    except Exception as e:
        error('Failed to fetch {}'.format(title_slug))
        return None


async def fetch_paged(limit, skip):
    async with ClientSession() as session:
        questions = await fetch_list(session)
        tasks = []
        for question in questions:
            tasks.append(ensure_future(fetch_one(session, question['titleSlug'])))
        results = await gather(*tasks)
        return results


async def sequential_fetch(limit, skip):
    async with ClientSession() as session:
        print('Fetching page {}'.format(skip))
        questions = await fetch_list(session)
        results = []
        for question in questions:
            print(question['titleSlug'])
            results.append(await fetch_one(session, question['titleSlug']))
        return results


if __name__ == '__main__':
    from time import time

    start = time()
    run(fetch_paged(50, 0))
    print(time() - start)
