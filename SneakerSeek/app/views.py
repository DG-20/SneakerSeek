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
    if request.method != "POST":
        list_params = pk.split(",")
        search = {}
        for pair in list_params:
            search[pair[0 : pair.find("=")]] = pair[pair.find("=") + 1 :]

        url = f"{sneakerseek_url}get_shoes_by_params/{search['brand']}/{search['gender']}/{search['type']}/{search['size']}/{search['condition']}/{search['max_price']}/{search['city']}/{search['quadrant']}/"
        json_return = requests.get(url).json()

        shoes = convert_to_shoe(json_return)
        return render(request, "results.html", {"shoes": shoes})

    else:
        id = request.POST["id"]
        return redirect(f"../product/{id}")


@login_required
def product(request, pk):
    if request.method != "POST":
        url = f"{sneakerseek_url}get_interested_by_shoe_id/{pk}/"
        json_return = requests.get(url).json()

        buyers = [
            {
                "username": "CurtisS",
                "f_name": "Curtis",
                "l_name": "S",
                "email": "curtis@gmail.com",
            },
            {
                "username": "LiamP",
                "f_name": "Liam",
                "l_name": "P",
                "email": "liam@gmail.com",
            },
        ]
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
    if request.method != "POST":
        return render(request, "sell_shoe.html")
    else:
        b = 2


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

        if firstName.strip() and firstName:
            request.user.first_name = firstName
            request.user.save()

        if lastName.strip() and lastName:
            request.user.last_name = lastName
            request.user.save()

        if currentPassword.strip() and currentPassword:
            if newPassword.strip() and newPassword:
                if confirmPassword.strip() and confirmPassword:
                    if currentPassword == request.user.password:
                        matched_users = auth.authentication(
                            username=request.user.username, password=currentPassword
                        )
                        if matched_users is None:
                            messages.info(
                                request, "The current password entered was incorrect!"
                            )
                            return redirect("settings")
                        else:
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
        return redirect("profile")

        # if firstname is empty dont update if it isnt empty then update it
        # if old password is not empty then compare to current password if they match then
        # if newpassword equals renewpassword then update password
        # if old password is incorrect or two new passwords dont match then need to show a message similar to register


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def my_shoes(request):
    if request.user.is_superuser == False:
        url = f"{sneakerseek_url}get_shoes_by_username/{request.user.username}/"
        json_return = requests.get(url).json()

        shoes = convert_to_shoe(json_return)
    else:
        url = f"{sneakerseek_url}get_all_shoes/"
        json_return = requests.get(url).json()

        shoes = convert_to_shoe(json_return)
    return render(request, "my_shoes.html", {"products": shoes})


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
        return redirect(manage_users)


@login_required
def edit_shoe(request, pk):
    product = sample_data()[0]
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


def sample_data():
    shoe1 = Shoe(
        brand="Nike",
        size=10,
        shoe_type="Highs",
        price=189.99,
        gender="Male",
        year_manufactured=2001,
        condition="Deadstock",
        quadrant="SW",
        seller="Div",
        image_url="https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/6f950390-c74c-41dd-90c6-9fae9c6adbdf/air-force-1-high-07-lx-mens-shoes-wTttNP.png",
        title="Nike Air Force 1 High Brand New",
        product_id="12341234",
        city="Calgary",
    )
    shoe2 = Shoe(
        brand="Adidas",
        size=7,
        shoe_type="Mids",
        price=99.99,
        gender="Female",
        year_manufactured=2021,
        condition="Heavily Worn",
        quadrant="NE",
        seller="Curtis",
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQrjAdYWImx34u-AHy1X6hVuseZ_sLBzj3dw&usqp=CAU",
        title="Adidas Mids Used",
        product_id="23452345",
        city="Calgary",
    )
    shoe3 = Shoe(
        brand="Air Jordan",
        size=13,
        shoe_type="Highs",
        price=1100.00,
        gender="Male",
        year_manufactured=1998,
        condition="Deadstock",
        quadrant="SE",
        seller="Liam",
        image_url="https://process.fs.grailed.com/AJdAgnqCST4iPtnUxiGtTz/cache=expiry:max/rotate=deg:exif/resize=width:2400,fit:crop/output=quality:70/compress/https://process.fs.grailed.com/z0qM3P5pR3a9viT9MCon",
        title="Jordan 1 High Bred Brand New",
        product_id="34563456",
        city="Chicago",
    )
    shoe4 = Shoe(
        brand="New Balance",
        size=8,
        shoe_type="Lows",
        price=80.00,
        gender="Male",
        year_manufactured=2009,
        condition="Rarely Used",
        quadrant="NW",
        seller="Curtis",
        image_url="https://nb.scene7.com/is/image/NB/bb550pb1_nb_02_i?$dw_detail_gallery$",
        title="New Balance S550 Rarely Used",
        product_id="45674567",
        city="Calgary",
    )
    shoe5 = Shoe(
        brand="Vans",
        size=11,
        shoe_type="Lows",
        price=110.00,
        gender="Male",
        year_manufactured=2018,
        condition="Deadstock",
        quadrant="SW",
        seller="Div",
        image_url="https://images.vans.com/is/image/Vans/D3HY28-HERO?$583x583$",
        title="Vans Old Skool Skate Shoe Brand New",
        product_id="56785678",
        city="Calgary",
    )
    shoe6 = Shoe(
        brand="Air Jordan",
        size=12,
        shoe_type="Highs",
        price=999.00,
        gender="Male",
        year_manufactured=1998,
        condition="Rarely Used",
        quadrant="NE",
        seller="Liam",
        image_url="https://images.solecollector.com/complex/images/c_crop,h_2921,w_5193,x_772,y_440/f_auto,fl_lossy,q_auto,w_1200/qsdrtn3exos5qn5zkvg8/air-jordan-1-chicago.jpg",
        title="Jordan 1 High Chicago Rarely Used",
        product_id="67896789",
        city="Chicago",
    )

    return [
        shoe1,
    ]


def convert_to_shoe(shoe_dicts):
    shoes = []
    for shoe in shoe_dicts:
        shoes.append(
            Shoe(
                brand=shoe["brand"],
                size=int(shoe["size"]),
                shoe_type=shoe["type"],
                price=float(shoe["price"]),
                gender=shoe["gender"],
                year_manufactured=shoe["year"],
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
