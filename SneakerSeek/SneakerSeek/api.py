from pymongo import MongoClient
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from bson.json_util import dumps

HOST_Link = "mongodb+srv://SneakerSeek:CPSC471@cluster0.jtwmo.mongodb.net/Sneakerseek?retryWrites=true&w=majority"


def connect_to_db():
    return MongoClient(HOST_Link).Sneakerseek


# api_view([INSERT: "POST", retrieve: "GET", update: "PATCH"])
@api_view(["GET"])
def get_all_cities(request, user_username):
    if request.method == "GET":
        # if request.user.username != user_username:
        #    return HttpResponse("Please log in first!")
        db_access = connect_to_db()
        val = db_access.Shoe.distinct("City")
        val_dict = {"Cities": val}
        json_data = dumps(val_dict)
        return JsonResponse(json_data, safe=False)


@api_view(["GET"])
def get_shoes_by_params():
    a = 2


@api_view(["GET"])
def get_shoe_by_id():
    a = 2


@api_view(["GET"])
def get_shoes_by_username():
    a = 2


@api_view(["POST"])
def interested_in():
    a = 2


@api_view(["GET"])
def get_interested_by_shoe_id():
    a = 2


@api_view(["PATCH"])
def delete_shoe():
    a = 2


@api_view(["GET"])
def get_all_shoes():
    a = 2


@api_view(["POST"])
def upload_shoe():
    a = 2


@api_view(["PATCH"])
def update_shoe():
    a = 2
