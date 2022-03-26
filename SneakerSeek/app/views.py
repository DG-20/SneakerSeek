from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from .models import Shoe

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
        # endpoint to grab all cities
        cities = ["Calgary", "Edmonton", "Airdrie", "Red Deer", "Fort Mac"]
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

        shoes = sample_data()
        return render(request, "results.html", {"shoes": shoes})

    else:
        id = request.POST["id"]
        return redirect(f"../product/{id}")


@login_required
def product(request, pk):
    if request.method != "POST":

        return render(
            request, "product.html", {"product": sample_data()[0], "seller_view": False}
        )

    else:
        a = 2


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
    return render(request, "my_shoes.html")


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
        title="Nike Highs Brand New",
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
        city="Edmonton",
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
        title="Jordan 1s Brand New",
        product_id="34563456",
        city="Chicago",
    )

    return [
        shoe1,
        shoe2,
        shoe3,
        shoe1,
        shoe2,
        shoe3,
        shoe1,
        shoe2,
        shoe3,
        shoe1,
        shoe2,
        shoe3,
    ]
