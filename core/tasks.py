
import rembg
from PIL import Image
from libs import utils

from celery import shared_task





@shared_task
def process_image(image, size, cupcake_pk, suffix):
    """Função auxiliar para redimensionar e remover fundo da imagem"""
    img_resized = image.resize(size, Image.Resampling.LANCZOS)
    
    # Remover fundo
    output_image = rembg.remove(img_resized)

    # Gerar um nome único para a imagem
    code = utils.generate_number()
    img_name = f"cupcake_{cupcake_pk}_{code}_{suffix}.png"
    
    return output_image, img_name