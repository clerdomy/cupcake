import hashlib
import os
import string
from random import choices, randint

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from core.models import Cupcake, CupcakeImage, Profile, Order
from core import tasks
from libs import utils


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)
    


# @receiver(post_save, sender=Cupcake)
# def add_default_cupcake_image(sender, instance, created, **kwargs):
#     if created:
#         # Adiciona uma imagem padrão ao cupcake recém-criado
#         CupcakeImage.objects.create(
#             cupcake=instance,
#             normal="cupcakes-fotos/default_cupcakes.jpeg",  # Caminho para a imagem padrão
#             descricao="Imagem padrão",
#         )


@receiver(post_save, sender=CupcakeImage)
def resize_and_rename_images(sender, instance, **kwargs):
    if instance._processed:
        return

    if instance.normal:
        image_path = instance.normal.path
        img = Image.open(image_path)

        if img.mode == "RGBA":
            img = img.convert("RGB")

        # Processar imagem normal
        normal_img, normal_img_name = tasks.process_image.delay(img, (400, 400), instance.pk, 'normal')
        normal_img_path = os.path.join("cupcakes-fotos", normal_img_name)
        normal_img.save(normal_img_path, format="PNG")
        instance.normal.name = normal_img_path

        # Processar imagem large_size
        large_img, large_img_name = tasks.process_image.delay(img, (600, 600), instance.pk, 'large')
        large_img_path = os.path.join("cupcakes-fotos/large-size", large_img_name)
        large_img.save(large_img_path, format="PNG")
        instance.large_size.name = large_img_path

        # Processar imagem small_size
        small_img, small_img_name = tasks.process_image.delay(img, (140, 140), instance.pk, 'small')
        small_img_path = os.path.join("cupcakes-fotos/small-size", small_img_name)
        small_img.save(small_img_path, format="PNG")
        instance.small_size.name = small_img_path

        # Remover a imagem original, se não for a padrão
        utils.delete_image_if_not_default(image_path)

        # Sinaliza que o processamento foi feito
        instance._processed = True
        instance.save()