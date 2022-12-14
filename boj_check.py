import json
import requests


# def get_solved(user_id):
#     """
#     정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 총 문제수, 문제들 정보(level 높은 순)를 튜플(int, list)로 반환해줌.
#     :param str user_id: 사용자id
#     :return: 내가 푼 문제수, 내가 푼 문제들 정보
#     :rtype: int, list
#     """
#     solved_problems = []

#     while True:
#         i = 1
#         url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&page={i}"
#         r_solved = requests.get(url)

#         if r_solved.status_code == requests.codes.ok:
#             solved = json.loads(r_solved.content.decode("utf-8"))


#             # print(solved)
#             count = solved.get("count")
#             items = solved.get("items")
#             # print(items)

#             for item in items:
#                 solved_problems.append(
#                     item.get("problemId"),
#                 )
#             i += 1
#         else:
#             print("푼 문제들 요청 실패")
#             return count, solved_problems


# user_id = "9776mk"

# count, sovled_list = get_solved(user_id)
# print(f"11111========{user_id}님이 푼 문제들({count})========")
# print(sovled_list)


import json
import requests


def get_solved(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 총 문제수, 문제들 정보(level 높은 순)를 튜플(int, list)로 반환해줌.
    :param str user_id: 사용자id
    :return: 내가 푼 문제수, 내가 푼 문제들 정보
    :rtype: int, list
    """
    solved_problems = []
    i = 1

    while True:
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&page={i}"
        r_solved = requests.get(url)
        solved = json.loads(r_solved.content.decode("utf-8"))

        items = solved.get("items")
        print(i)
        print(items)

        if items:
            for item in items:
                solved_problems.append(
                    item.get("problemId"),
                )
            i += 1
        else:
            return solved_problems


user_id = "9776mk"

sovled_list = get_solved(user_id)
# print(f"11111========{user_id}님이 푼 문제들({count})========")
print(sovled_list)
