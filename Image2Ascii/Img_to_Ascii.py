import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import string
import os
import shutil

def hue_char(character):
  ''' Função que abstrai a tonalidade do caracter, contando o número de espaços não brancos. 
      Objetivo: Verificar o melhor ajuste de tonalidade na conversão de imagem para art ASCII.
      Porque numpy? Operações matriciais eficientes e otima compatibilidade com biblioteca PIL.
  '''
  tamanho = (10, 10)  # Tamanho arbitrário para o caractere
  imagem_temporaria = Image.new('L', tamanho, color=255)
  draw = ImageDraw.Draw(imagem_temporaria)
  fonte = ImageFont.load_default()

  # Desenhe o caractere na imagem temporária
  draw.text((0, 0), character, font=fonte, fill=0)

  # Converta a imagem para um array NumPy
  array_imagem = np.array(imagem_temporaria)

  # Conte os pixels não brancos (preenchidos)
  quantidade_preenchida = np.sum(array_imagem < 255)

  return quantidade_preenchida


def image_to_ASCII(image_path, output_width=900):
    ''' Função que converte imagem para tons de cinza e, depois, para arte ASCII com caracteres '''
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Imagem não encontrada: {image_path}")
        return

    # Redimensionar imagem
    aspect_ratio = img.height / img.width
    new_height = aspect_ratio * output_width * 0.5
    img = img.resize((output_width, int(new_height)))

    # Converter para a escala de cinza
    img = img.convert('L')

    # Caracteres de mapeamento de intensidade
    chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", ".", "M",
             "!", "#", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
             ":", " "]

    # criando uma lista com a tonalidade (numericamente) dos caracteres
    chars_hue = [hue_char(char) for char in chars]
    # reordene 'chars' em relação à tonalidade do caracter
    chars_sorted_by_hue = [char for _, char in sorted(zip(chars_hue, chars), reverse=True)]
    # Intervalo de valores baseado em qtd de chars do intervalo de pixel = [0, 255]
    pixel_range = min(255 // (len(chars_sorted_by_hue) - 1), 255)

    # Mapeamento dos pixels para caracteres
    pixels = img.getdata()
    new_pixels = [chars_sorted_by_hue[pixel // pixel_range] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # Criação da arte ASCII
    ascii_image = [new_pixels[index:index + output_width] for index in range(0, len(new_pixels), output_width)]
    ascii_image = "\n".join(ascii_image)

    # Salva a arte ASCII em um arquivo
    archive_name = image_path.split("\\")[-1].split(".")[0]
    timestamp = int(dt.datetime.now().timestamp())
    output_filename = f"{archive_name}_ASCII_art_{timestamp}.txt"
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(ascii_image)

    print(f"Arte ASCII salva em {output_filename}")


#ex: C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\5° Semestre - UnB\\Projeto de Algoritimo\\Asciiart\\Jackdaw-daily-tema.jpg
#ex: C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\5° Semestre - UnB\\Projeto de Algoritimo\\Asciiart\\luffy_test.png
#ex: C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\5° Semestre - UnB\\Projeto de Algoritimo\\Asciiart\\spyder_test.jpg
#ex: C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\5° Semestre - UnB\\Projeto de Algoritimo\\Asciiart\\GTA6_test.jpg
image_to_ASCII('C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\5° Semestre - UnB\\Projeto de Algoritimo\\Asciiart\\kimestu.jpg')


def criar_pasta(nome_pasta:any, arquivos):
    # define por padrão que o nome da pasta é o mesmo do primeiro arquivo
    if(nome_pasta == any):
        nome_pasta = os.path.basename(arquivos[0]).split('.')[0]
    try:
        # Verifica se a pasta já existe
        if os.path.exists(nome_pasta):
            print(f"A pasta '{nome_pasta}' já existe.")
        else:
            # Cria a pasta
            os.mkdir(nome_pasta)
            print(f"Pasta '{nome_pasta}' criada com sucesso!")

        # Anexa os arquivos dentro da pasta
        for arquivo in arquivos:
            nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
            caminho_destino = os.path.join(nome_pasta, nome_arquivo)

            # Verifica se o arquivo já existe na pasta
            if os.path.exists(caminho_destino):
                print(f"O arquivo '{nome_arquivo}' já existe na pasta.")
            else:
                shutil.copy(arquivo, caminho_destino)
                print(f"Arquivo '{nome_arquivo}' anexado com sucesso!")

    except Exception as e:
        print(f"Erro ao criar a pasta ou anexar arquivos: {e}")

def hue_info_chars():
    ''' Função de Teste para verificar 'quantida de pigmentação' referente a cada caracter '''
    list_chars = list(string.ascii_letters + string.punctuation)
    dict_dif_hue = {}
    for ch in list_chars:
        char_ton = hue_char(ch)
        if (char_ton not in dict_dif_hue.values()):
            dict_dif_hue.update({ch:char_ton})
        #print(ch, ' - ', hue_char(ch),'; ')
    return dict_dif_hue

#print(len(hue_info_chars()))