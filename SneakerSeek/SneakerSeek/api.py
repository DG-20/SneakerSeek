from re import search
from pymongo import MongoClient
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from bson.json_util import dumps
from bson import ObjectId

HOST_Link = "mongodb+srv://SneakerSeek:CPSC471@cluster0.jtwmo.mongodb.net/Sneakerseek?retryWrites=true&w=majority"


def connect_to_db():
    return MongoClient(HOST_Link).Sneakerseek


def check_for_injections(parameters):
    for param in parameters:
        if "{" in param or "}" in param or "$" in param:
            return True
    return False


# api_view([INSERT: "POST", retrieve: "GET", update: "PATCH"])
@api_view(["GET"])
def get_all_cities(request):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        db_access = connect_to_db()
        val = db_access.Shoe.distinct("city")
        val_dict = {"Cities": val}
        return_val = dumps(val_dict)
        return JsonResponse(return_val, safe=False)


@api_view(["GET"])
def get_shoes_by_params(
    request, brand, gender, type, size, condition, max_price, city, quadrant
):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        injection_exists = check_for_injections(
            [brand, gender, type, size, condition, max_price, city, quadrant]
        )

        if injection_exists == True:
            return HttpResponse("Unauthorized query!")

        search_criteria = {}

        if brand != "all":
            search_criteria["brand"] = brand
        if gender != "all":
            search_criteria["gender"] = gender
        if type != "all":
            search_criteria["type"] = type
        if size != "all":
            search_criteria["size"] = size
        if condition != "all":
            search_criteria["condition"] = condition
        if max_price != "all":
            search_criteria["price"] = {"$lte": max_price}
        if max_price == "more":
            search_criteria["price"] = {"$gt": "500"}
        if city != "all":
            search_criteria["city"] = city
        if quadrant != "all":
            search_criteria["quadrant"] = quadrant

        db_access = connect_to_db()

        if search_criteria:
            search_results = db_access.Shoe.find(search_criteria)
        else:
            search_results = db_access.Shoe.find()

        return_val = []
        for result in search_results:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(result[key])
            return_val.append(result_dict)

        return JsonResponse(return_val, safe=False)


@api_view(["GET"])
def get_shoe_by_id(request, shoe_id):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        injection_exists = check_for_injections([shoe_id])

        if injection_exists == True:
            return HttpResponse("Unauthorized query!")

        db_access = connect_to_db()

        search_critera = {"_id": ObjectId(shoe_id)}

        search_results = db_access.Shoe.find(search_critera)

        return_val = []
        for result in search_results:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(result[key])
            return_val.append(result_dict)

        return JsonResponse(return_val, safe=False)


@api_view(["GET"])
def get_shoes_by_username(request, username):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        injection_exists = check_for_injections([username])

        if injection_exists == True:
            return HttpResponse("Unauthorized query!")

        db_access = connect_to_db()

        search_critera = {"seller": username}

        search_results = db_access.Shoe.find(search_critera)

        return_val = []
        for result in search_results:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(result[key])
            return_val.append(result_dict)

        return JsonResponse(return_val, safe=False)


@api_view(["POST"])
def interested_in(request):
    if request.method == "POST":
        db_access = connect_to_db()
        db_access.Interest.insert_one(request.data)
        return HttpResponse("Success")


@api_view(["GET"])
def get_interested_by_shoe_id(request, shoe_id):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        injection_exists = check_for_injections([shoe_id])

        if injection_exists == True:
            return HttpResponse("Unauthorized query!")

        db_access = connect_to_db()

        search_critera = {"shoe_id": shoe_id}

        search_results = db_access.Interest.find(search_critera)

        return_val = []
        for result in search_results:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(result[key])
            return_val.append(result_dict)

        return JsonResponse(return_val, safe=False)


@api_view(["PATCH"])
def delete_shoe():
    a = 2


@api_view(["GET"])
def get_all_shoes(request):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")

        db_access = connect_to_db()

        search_results = db_access.Shoe.find()

        return_val = []
        for result in search_results:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(result[key])
            return_val.append(result_dict)

        return JsonResponse(return_val, safe=False)


@api_view(["POST"])
def upload_shoe():
    a = 2


@api_view(["PATCH"])
def update_shoe():
    a = 2
