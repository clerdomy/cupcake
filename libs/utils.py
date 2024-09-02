from core.models import Cupcake, Review
from django.shortcuts import get_object_or_404
import hashlib
import string
import random
import re
import os


def delete_image_if_not_default(image_path):
    # Verifica se o caminho da imagem existe e se a imagem não é a padrão
    if os.path.exists(image_path) and not image_path.endswith("default_cupcakes.jpeg"):
        try:
            os.remove(image_path)
            print(f"Imagem {image_path} removida com sucesso.")
        except Exception as e:
            print(f"Erro ao remover a imagem {image_path}: {e}")
    else:
        print(f"A imagem {image_path} não foi removida, pois é a padrão ou não existe.")


def html_star(qtd):
    product_rating = ""
    for _ in range(qtd):
        product_rating += '<i class="fa fa-star"></i>'
    for _ in range(abs(qtd - 5)):
        product_rating += '<i class="fa fa-star-o"></i>'
    return product_rating


def cupcake_rating_median(cupcake: Cupcake):
    reviews = Review.objects.filter(cupcake=cupcake)

    if reviews:
        media = sum([review.avaliacao for review in reviews]) // len(reviews)
    else:
        media = 0
    avaliacao_html = html_star(media)

    return avaliacao_html


def cupcake_rating(cupcake_id):
    cupcake = get_object_or_404(Cupcake, id=cupcake_id)
    reviews = Review.objects.filter(cupcake=cupcake).order_by("-data")
    for review in reviews:
        review.avaliacao_html = html_star(review.avaliacao)
    return {"reviews": reviews}

def generate_user_token(username):
    return hashlib.md5(username.encode()).hexdigest()[:5]


def generate_random_code(N=62):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def generate_number(size=100):
    numbers = random.randint(0, size)
    letters = letters = "".join(random.choices(string.ascii_letters, k=size))

    hexdigest = hashlib.md5(f"{letters}-{numbers}".encode()).hexdigest()
    return hexdigest

def validar_email(email):
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email) is not None


def sku_code(N=10):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(N))
