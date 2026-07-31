import io
import os

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

LARGURA_MAXIMA = 1200
QUALIDADE_WEBP = 82


def converter_para_webp(arquivo, largura_maxima=LARGURA_MAXIMA, qualidade=QUALIDADE_WEBP):
    arquivo.seek(0)
    imagem = Image.open(arquivo)
    imagem = ImageOps.exif_transpose(imagem)

    tem_transparencia = imagem.mode in ('RGBA', 'LA') or 'transparency' in imagem.info
    imagem = imagem.convert('RGBA' if tem_transparencia else 'RGB')

    imagem.thumbnail((largura_maxima, largura_maxima), Image.LANCZOS)

    buffer = io.BytesIO()
    imagem.save(buffer, format='WEBP', quality=qualidade, method=6)

    nome = os.path.splitext(os.path.basename(arquivo.name))[0] + '.webp'
    return ContentFile(buffer.getvalue(), name=nome)
