from django.shortcuts import render
from .models import Ice_Cream, Comments, Statistics
from .forms import CommentForm, IceForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout

# Create your views here.
CART = {}
BUY = {}
TOTAL_PRICE = 0


def home(request):
    context = {
        'user': request.user,
        'ice_cream': Ice_Cream.objects.all(),
    }
    return render(request, 'order/home.html', context)


def search(request):
    if request.method == "POST":
        check_product = False
        name = request.POST['name']
        if name == '':
            return HttpResponseRedirect(reverse('home'))
        context = {
            'user': request.user,
            'ice_cream': Ice_Cream.objects.all(),
        }
        for i in range(len(context['ice_cream'])):
            if name == context['ice_cream'][i].name:
                context['ice_cream'] = context['ice_cream'][i]
                check_product = True
                break
        if check_product == True:
            return render(request, 'order/search.html', context)
        else:
            check_product = False
            name = name.lower()
            cart_search = []
            if name == '':
                return HttpResponseRedirect(reverse('home'))
            context = {
                'user': request.user,
            }
            tmp = {}
            tmp['ice'] = Ice_Cream.objects.all()
            for i in range(len(tmp['ice'])):
                t = tmp['ice'][i].name.lower()
                if t.find(name) != -1:
                    cart_search.append(tmp['ice'][i])
                    check_product = True
            if check_product == True:
                context['ice_cream'] = cart_search
                return render(request, 'order/search.html', context)
            else:
                return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


def user_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    context = {
        'user': request.user,
    }
    return render(request, 'order/profile.html', context)


def view_detail(request):
    if request.method == 'POST':

        item_id = request.POST['id']
        product_size = request.POST['size']
        try:
            item = Ice_Cream.objects.get(id=item_id)
        except Ice_Cream.DoesNotExist:
            raise Http404("item does not exist")
        item.size = product_size
        if product_size == 'S':
            item.price = item.price
        elif product_size == 'M':
            item.price = item.price * 1.25
        elif product_size == 'L':
            item.price = item.price * 1.5
        form = CommentForm(request.POST, author=request.user, post=item)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('detail'))
        context = {
            'item': item,
            "form": form,
            "size": product_size,
        }
        return render(request, 'order/detail_product.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))


# //add to cart
def cart(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.method == "POST":
        item_id = int(request.POST['item_id'])
        item_size = request.POST['item_size']
        item_price = request.POST['item_price']
        try:
            item = Ice_Cream.objects.get(id=item_id)
        except Ice_Cream.DoesNotExist:
            raise Http404("item does not exist")
        item.size = item_size
        item.price = item_price
        if request.user.id in CART.keys():
            pass
        else:
            CART[request.user.id] = []
        CART[request.user.id].append(item)
        return HttpResponseRedirect(reverse("show_cart"))
    else:
        return HttpResponseRedirect(reverse('home'))


def show_cart(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.user.id in CART.keys():
        pass
    else:
        CART[request.user.id] = []
    mycart = []
    for i in range(len(CART[request.user.id])):
        mycart.append({
            "item": CART[request.user.id][i],
            "idx": i
        })

    return render(request, 'order/cart.html', {"mycart": mycart})


def buy(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.user.id in BUY.keys():
        pass
    else:
        BUY[request.user.id] = []
    global TOTAL_PRICE
    current_price = 0
    item_id = ''
    item_size = ''
    if request.user.id in CART.keys():
        pass
    else:
        CART[request.user.id] = []
    if CART[request.user.id] == []:
        return render(request, 'order/buy.html', {'mybuy': BUY[request.user.id], 'total_price': TOTAL_PRICE})
    for i in range(len(CART[request.user.id])):
        BUY[request.user.id].append(CART[request.user.id][i])
        current_price += float(CART[request.user.id][i].price)
        TOTAL_PRICE += float(CART[request.user.id][i].price)
        if i < len((CART[request.user.id])) - 1:
            item_id += str(CART[request.user.id][i].id) + ' '
            item_size += str(CART[request.user.id][i].size) + ' '
        elif i == len((CART[request.user.id])) - 1:
            item_id += str(CART[request.user.id][i].id)
            item_size += str(CART[request.user.id][i].size)
    CART[request.user.id] = []
    customer = Statistics.objects.create(customer=request.user, price=current_price, items=item_id,
                                         items_size=item_size)
    customer.save()
    return render(request, 'order/buy.html', {'mybuy': BUY[request.user.id], 'total_price': TOTAL_PRICE})


def show_buy(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.user.id in BUY.keys():
        pass
    else:
        BUY[request.user.id] = []
    global TOTAL_PRICE
    return render(request, 'order/buy.html', {'mybuy': BUY[request.user.id], 'total_price': TOTAL_PRICE})


def delete_item(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.method == "POST":

        item_id = int(request.POST['idx'])
        CART[request.user.id].pop(item_id)
        return HttpResponseRedirect(reverse('show_cart'))
    else:
        return HttpResponseRedirect(reverse('home'))


def change_pass(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if request.method == "POST":
        password = request.POST['password']
        newpassword = request.POST['newpassword']
        renewpassword = request.POST['renewpassword']
        context = {
            'user': request.user,
            "message": "",
        }
        currentpassword = request.user.password
        matchcheck = check_password(renewpassword, currentpassword)
        if not matchcheck:
            context['message'] = "Password incorrect!"
        if password == '' or newpassword == '' or renewpassword == '':
            context['message'] = "Not empty pass!"
        elif renewpassword != newpassword:
            context['message'] = "Not confirm!"
        else:
            user = request.user
            user.set_password(newpassword)
            user.save()
            context['message'] = "Change password Successful!"
            t = authenticate(request, username=user.username, password=newpassword)
            login(request, t)
        return render(request, 'order/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('profile'))


def category_filter(request):

    if request.method == "POST":
        cate = request.POST["cate"]
        frequency = request.POST["frequency"]
        if cate != 'Z' and frequency != 'Z':
            context = {
                'user': request.user,
                'ice_cream': Ice_Cream.objects.filter(categories=cate, frequencies=frequency),
            }
        elif cate == 'Z' and frequency != 'Z':
            context = {
                'user': request.user,
                'ice_cream': Ice_Cream.objects.filter(frequencies=frequency),
            }
        elif cate != 'Z' and frequency == 'Z':
            context = {
                'user': request.user,
                'ice_cream': Ice_Cream.objects.filter(categories=cate),
            }
        else:
            context = {
                'user': request.user,
                'ice_cream': '',
            }
        return render(request, 'order/cate.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))


def statistics_manager(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    context = {
        'statistics': Statistics.objects.all(),
    }
    return render(request, 'order/statistics.html', context)


def view_statistics(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    if request.method == "POST":
        items_id = request.POST['id']
        items_size = request.POST['size']
        list_item = items_id.split()
        list_size = items_size.split()
        context = {}
        context['ice_cream'] = []
        for i in range(len(list_item)):
            try:
                item = Ice_Cream.objects.get(id=list_item[i])
            except Ice_Cream.DoesNotExist:
                raise Http404("item does not exist")
            context['ice_cream'].append(item)
            context['ice_cream'][i].size = list_size[i]
            if list_size[i] == 'S':
                context['ice_cream'][i].price = context['ice_cream'][i].price
            elif list_size[i] == 'M':
                context['ice_cream'][i].price = context['ice_cream'][i].price * 1.25
            elif list_size[i] == 'L':
                context['ice_cream'][i].price = context['ice_cream'][i].price * 1.5
        return render(request, 'order/view_statistics.html', context)
    else:
        return HttpResponseRedirect(reverse('statistics'))

def add_form(request):
    return render(request, 'order/manage_ice_cream.html')

def add_ice(request):
    if request.method == "POST":
        # form = IceForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponseRedirect(reverse('home'))
        # else:
        #     return HttpResponseRedirect(reverse('add_form'))
        name = request.POST['name']
        images = request.POST['images']
        price = float(request.POST['price'])
        size = request.POST['size']
        categories = request.POST['categories']
        frequencies = request.POST['frequencies']
        description = request.POST['description']
        ice = Ice_Cream.objects.create(name=name, images=images, price=price, size=size, categories=categories, frequencies=frequencies, description=description)
        ice.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))