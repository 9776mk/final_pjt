from django.shortcuts import render
from .models import *


def index(request):
    br = BJData_br.objects.order_by("pk")
    si = BJData_si.objects.order_by("pk")

    tags = BJData_br.objects.values("tags")
    print(tags)
    print(type(tags))
    category = []
    for i in tags:
        # print(i["tags"])
        #    category.append(i["tags"])

        for j in i["tags"]:
            print(j)

    # print(type(category))
    # print("categroy 출력")
    # print(category)
    # print("######################################")

    # test = []
    # for list in category:
    #     # print(list)
    #     for i in list:
    #         if i == "[" or i == "]" or i == "," or i == "'":
    #             continue
    #         else:
    #             test.append(i)
    # # print("test 출력")
    # # print(test)
    # # print("######################################")

    # str_ = ""
    # for i in test:
    #     str_ += i

    # print(str_)
    # # print(str_.split())
    # print("str_ 출력")
    # print(str_)
    # print("##############################################################")

    # str_ = str_.split()

    # for tag in str_:
    #     print(tag)

    context = {
        "br": br,
        "si": si,
        "tags": tags,
    }
    return render(request, "algorithm/index.html", context)
