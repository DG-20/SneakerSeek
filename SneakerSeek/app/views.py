from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout, get_user_model
from django.contrib import messages
from .models import Shoe
import requests
import json

sneakerseek_url = "http://127.0.0.1:8000/"

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("search_view")
        else:
            messages.info(
                request, "The Username and/or Password Entered are Incorrect!"
            )
            return redirect("index")
    else:
        return render(request, "index.html")


def register(request):
    if request.method == "POST":
        fname = request.POST["f_name"]
        lname = request.POST["l_name"]
        username = request.POST["username"]
        password = request.POST["pass"]
        verifypass = request.POST["confirmpass"]
        email = request.POST["email"]

        if password == verifypass:
            # User is the thing being imported, filter goes in the db and checks
            # if the email entered already exists.
            if User.objects.filter(email=email).exists():
                messages.info(
                    request, "Email already in use! Please go back and log in!"
                )
                # Send em back to register
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username not available! Try a different one!")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fname,
                    last_name=lname,
                )
                user.save()
                return redirect("index")
        else:
            messages.info(request, "Passwords did not match!")
            return redirect("register")

    else:
        return render(request, "register.html")


@login_required
def search_view(request):
    if request.user.is_superuser == True:
        return redirect("profile")
    if request.method != "POST":
        url = f"{sneakerseek_url}get_all_cities/"
        json_string_return = requests.get(url).json()
        json_acceptable_string = json_string_return.replace("'", '"')
        dict_cities = json.loads(json_acceptable_string)
        cities = dict_cities["Cities"]
        context = {"cities": cities}
        return render(request, "search.html", context)
    else:
        brand = request.POST["brand"]
        size = request.POST["size"]
        type = request.POST["type"]
        max_price = request.POST["max_price"]
        gender = request.POST["gender"]
        condition = request.POST["condition"]
        quadrant = request.POST["quadrant"]
        city = request.POST["city"]

        return redirect(
            f"results/brand={brand},size={size},type={type},max_price={max_price},gender={gender},condition={condition},quadrant={quadrant},city={city}"
        )


@login_required
def results(request, pk):
    if request.user.is_superuser == True:
        return redirect("profile")
    if request.method != "POST":
        list_params = pk.split(",")
        search = {}
        for pair in list_params:
            search[pair[0 : pair.find("=")]] = pair[pair.find("=") + 1 :]

        url = f"{sneakerseek_url}get_shoes_by_params/{search['brand']}/{search['gender']}/{search['type']}/{search['size']}/{search['condition']}/{search['max_price']}/{search['city']}/{search['quadrant']}/"
        json_return = requests.get(url).json()
        if len(json_return) > 0:
            shoes = convert_to_shoe(json_return)
            empty = False
        else:
            shoes = None
            empty = True
        return render(request, "results.html", {"shoes": shoes, "empty": empty})

    else:
        id = request.POST["id"]
        return redirect(f"../product/{id}")


@login_required
def product(request, pk):
    if request.method != "POST":
        url = f"{sneakerseek_url}get_interested_by_shoe_id/{pk}/"
        json_return = requests.get(url).json()
        buyers = []

        for ret in json_return:
            username_val = ret["username"]
            if User.objects.filter(username=username_val).exists():
                user_interested = User.objects.get(username=username_val)
                buyers.append(
                    {
                        "username": user_interested.username,
                        "f_name": user_interested.first_name,
                        "l_name": user_interested.last_name,
                        "email": user_interested.email,
                    }
                )

        url = f"{sneakerseek_url}get_shoe_by_id/{pk}/"
        json_return = requests.get(url).json()

        shoe = convert_to_shoe(json_return)[0]
        return render(
            request,
            "product.html",
            {"product": shoe, "buyers": buyers},
        )

    else:
        name = request.POST["name"]
        email = request.POST["email"]
        product_id = request.POST["product_id"]

        post_data = {"shoe_id": product_id, "username": request.user.username}
        json_product = json.dumps(post_data)
        response = requests.post(
            f"{sneakerseek_url}interested_in/",
            data=json_product,
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        return redirect("search_view")


@login_required
def sell_shoe(request):
    if request.user.is_superuser == True:
        return redirect("profile")
    if request.method != "POST":
        return render(request, "sell_shoe.html")
    else:
        brand = request.POST["brand"]
        size = request.POST["size"]
        type = request.POST["type"]
        brand = request.POST["brand"]
        collection = request.POST["collection"]
        name = request.POST["title"]
        price = request.POST["price"]
        gender = request.POST["gender"]
        year = request.POST["year"]
        condition = request.POST["condition"]
        city = request.POST["city"]
        image_url = request.POST["image_url"]
        quadrant = request.POST["quadrant"]

        post_data = {
            "brand": brand,
            "collection": collection,
            "size": size,
            "type": type,
            "title": name,
            "price": float(price),
            "gender": gender,
            "year": year,
            "condition": condition,
            "city": city,
            "quadrant": quadrant,
            "seller": request.user.username,
            "image": image_url,
        }

        json_product = json.dumps(post_data)

        response = requests.post(
            f"{sneakerseek_url}upload_shoe/",
            data=json_product,
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        return redirect("search_view")


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def settings(request):
    if request.method != "POST":
        return render(request, "settings.html")

    else:
        firstName = request.POST["f_name"]
        lastName = request.POST["l_name"]
        # username = request.POST["username"]
        # email = request.POST["email"]
        currentPassword = request.POST["currentPassword"]
        newPassword = request.POST["newPassword"]
        confirmPassword = request.POST["confirmPassword"]
        print(currentPassword, newPassword, confirmPassword)

        if firstName.strip() and firstName:
            request.user.first_name = firstName
            request.user.save()

        if lastName.strip() and lastName:
            request.user.last_name = lastName
            request.user.save()

        if currentPassword.strip() and currentPassword:
            if newPassword.strip() and newPassword:
                if confirmPassword.strip() and confirmPassword:
                    if request.user.check_password(currentPassword) == True:
                        if newPassword == confirmPassword:
                            request.user.set_password(newPassword)
                            request.user.save()
                            return redirect("profile")

                        else:
                            messages.info(
                                request,
                                "The new password was not confirmed correctly!",
                            )
                        return redirect("settings")
                    else:
                        messages.info(
                            request, "The current password entered was incorrect!"
                        )
                        return redirect("settings")
                else:
                    messages.info(request, "Please enter all three password fields!")
                    return redirect("settings")
            else:
                messages.info(request, "Please enter all three password fields!")
                return redirect("settings")
    return redirect("profile")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def my_shoes(request):
    if request.method != "POST":
        if request.user.is_superuser == False:
            url = f"{sneakerseek_url}get_shoes_by_username/{request.user.username}/"
            json_return = requests.get(url).json()
            if len(json_return) > 0:
                shoes = convert_to_shoe(json_return)
                empty = False
            else:
                shoes = None
                empty = True
        else:
            url = f"{sneakerseek_url}get_all_shoes/"
            json_return = requests.get(url).json()
            if len(json_return) > 0:
                shoes = convert_to_shoe(json_return)
                empty = False
            else:
                shoes = None
                empty = True
        return render(request, "my_shoes.html", {"products": shoes, "empty": empty})
    else:
        shoe_id_to_delete = request.POST["shoe_id"]
        post_data = {"_id": shoe_id_to_delete}

        json_delete = json.dumps(post_data)

        response = requests.delete(
            f"{sneakerseek_url}delete_shoe/",
            data=json_delete,
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        return redirect("my_shoes")


@login_required
def manage_users(request):
    if request.user.is_superuser == False:
        return redirect("search_view")
    if request.method != "POST":
        all_users = get_user_model().objects.all()
        site_users = []
        for all_user in all_users:
            if all_user != request.user:
                site_users.append(all_user)
        return render(request, "manage_users.html", {"site_users": site_users})
    else:
        user_to_delete = request.POST["username_del"]
        user_del = User.objects.get(username=user_to_delete)
        user_del.delete()
        url = f"{sneakerseek_url}get_shoes_by_username/{user_to_delete}/"
        json_return = requests.get(url).json()
        shoe_ids_to_delete = []
        for ret in json_return:
            shoe_ids_to_delete.append(ret["_id"])
        for id in shoe_ids_to_delete:
            post_data = {"_id": id}

            json_delete = json.dumps(post_data)

            response = requests.delete(
                f"{sneakerseek_url}delete_shoe/",
                data=json_delete,
                headers={
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
            )
        return redirect(manage_users)


@login_required
def edit_shoe(request, pk):
    if request.method != "POST":
        url = f"{sneakerseek_url}get_shoe_by_id/{pk}/"
        json_return = requests.get(url).json()

        product = convert_to_shoe(json_return)[0]
        Brands = [
            "Air Jordan",
            "Nike",
            "Adidas",
            "Under Armour",
            "New Balance",
            "Converse",
            "Common Projects",
            "Puma",
            "Vans",
            "Reebok",
            "Balenciaga",
            "Asics",
            "Gucci",
            "Sketchers",
            "Fila",
        ]
        Type = ["Highs", "Lows", "Mids", "Slides", "High Heels", "Slippers", "Oxfords"]
        Gender = ["Male", "Female", "Unisex"]
        Condition = ["Deadstock", "Rarely Used", "Gently Used", "Worn", "Heavily Worn"]
        Quadrant = ["SW", "SE", "NE", "NW"]
        return render(
            request,
            "edit_shoe.html",
            {
                "shoe": product,
                "Brands": Brands,
                "range": range(6, 15),
                "type": Type,
                "gender": Gender,
                "condition": Condition,
                "quadrant": Quadrant,
                "years": range(1990, 2023),
            },
        )
    else:
        shoe_id_to_update = request.POST["shoe_id"]
        brand_updated = request.POST["brand"]
        collection_updated = request.POST["collection"]
        size_updated = request.POST["size"]
        type_updated = request.POST["type"]
        name_updated = request.POST["title"]
        price_updated = request.POST["price"]
        gender_updated = request.POST["gender"]
        year_updated = request.POST["year"]
        condition_updated = request.POST["condition"]
        city_updated = request.POST["city"]
        quadrant_updated = request.POST["quadrant"]

        post_data = {
            "_id": shoe_id_to_update,
            "brand_updated": brand_updated,
            "collection_updated": collection_updated,
            "size_updated": size_updated,
            "type_updated": type_updated,
            "title_updated": name_updated,
            "price_updated": float(price_updated),
            "gender_updated": gender_updated,
            "year_updated": int(year_updated),
            "condition_updated": condition_updated,
            "city_updated": city_updated,
            "quadrant_updated": quadrant_updated,
        }

        json_product_updated = json.dumps(post_data)

        response = requests.put(
            f"{sneakerseek_url}update_shoe/",
            data=json_product_updated,
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )

        return redirect("my_shoes")


def convert_to_shoe(shoe_dicts):
    shoes = []
    for shoe in shoe_dicts:
        shoes.append(
            Shoe(
                brand=shoe["brand"],
                collection=shoe["collection"],
                size=int(shoe["size"]),
                shoe_type=shoe["type"],
                price=float(shoe["price"]),
                gender=shoe["gender"],
                year_manufactured=int(shoe["year"]),
                condition=shoe["condition"],
                quadrant=shoe["quadrant"],
                seller=shoe["seller"],
                image_url=shoe["image"],
                title=shoe["title"],
                product_id=shoe["_id"],
                city=shoe["city"],
            )
        )
    return shoes
