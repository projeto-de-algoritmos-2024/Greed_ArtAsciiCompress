import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import heapq
import os
from collections import Counter
import pickle
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import numpy as np

class CodificacaoHuffman:
    def __init__(self):
        self.codigos = {}
        self.codigos_reversos = {}

    def _construir_dicionario_frequencia(self, texto):
        return Counter(texto)

    def _construir_fila_prioridade(self, dicionario_frequencia):
        fila = [[peso, [caracter, ""]] for caracter, peso in dicionario_frequencia.items()]
        heapq.heapify(fila)
        return fila

    def _construir_arvore(self, fila):
        while len(fila) > 1:
            baixo = heapq.heappop(fila)
            alto = heapq.heappop(fila)
            for par in baixo[1:]:
                par[1] = '0' + par[1]
            for par in alto[1:]:
                par[1] = '1' + par[1]
            heapq.heappush(fila, [baixo[0] + alto[0]] + baixo[1:] + alto[1:])
        return fila[0]

    def _construir_codigos(self, arvore):
        for par in arvore[1:]:
            self.codigos[par[0]] = par[1]
            self.codigos_reversos[par[1]] = par[0]

    def codificar(self, texto):
        dicionario_frequencia = self._construir_dicionario_frequencia(texto)
        fila = self._construir_fila_prioridade(dicionario_frequencia)
        arvore = self._construir_arvore(fila)
        self._construir_codigos(arvore)
        texto_codificado = ''.join(self.codigos[char] for char in texto)
        texto_codificado_preenchido = self._preencher_texto_codificado(texto_codificado)
        bytes_codificados = bytearray()
        for i in range(0, len(texto_codificado_preenchido), 8):
            byte = texto_codificado_preenchido[i:i+8]
            bytes_codificados.append(int(byte, 2))
        return bytes_codificados

    def decodificar(self, bytes_codificados):
        string_bits = ''.join(format(byte, '08b') for byte in bytes_codificados)
        string_bits = self._remover_preenchimento(string_bits)
        codigo_atual = ''
        texto_decodificado = ''
        for bit in string_bits:
            codigo_atual += bit
            if codigo_atual in self.codigos_reversos:
                caracter = self.codigos_reversos[codigo_atual]
                texto_decodificado += caracter
                codigo_atual = ''
        return texto_decodificado

    def _preencher_texto_codificado(self, texto_codificado):
        preenchimento = 8 - len(texto_codificado) % 8
        texto_codificado = texto_codificado + '0' * preenchimento
        return f"{preenchimento:08b}" + texto_codificado

    def _remover_preenchimento(self, string_bits):
        preenchimento = int(string_bits[:8], 2)
        string_bits = string_bits[8:]
        return string_bits[:-preenchimento]

    def salvar_arvore(self, nome_arquivo):
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.codigos_reversos, arquivo)

    def carregar_arvore(self, nome_arquivo):
        with open(nome_arquivo, 'rb') as arquivo:
            self.codigos_reversos = pickle.load(arquivo)

class AplicativoHuffman:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Compressão Huffman")
        self.raiz.geometry("600x500")
        self.raiz.configure(bg='#f3efef')

        self.codificacao_huffman = CodificacaoHuffman()

        style = ttk.Style()
        style.configure('TButton',
                        font=('Arial', 12, 'bold'),
                        padding=10,
                        relief='flat',
                        background='#8eb4f2',
                        foreground='black')
        style.map('TButton',
                  background=[('active', '#8c9eff')])
        style.configure('TLabel',
                        font=('Arial', 12),
                        background='#f3efef',
                        foreground='rgb(3, 5, 87)')
        style.configure('TFrame',
                        background='#f3efef')

        self.frame = ttk.Frame(raiz)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.rotulo = ttk.Label(self.frame, text="Escolha um arquivo:")
        self.rotulo.pack(pady=10)

        self.botao_upload = ttk.Button(self.frame, text="Carregar Arquivo", command=self.carregar_arquivo)
        self.botao_upload.pack(pady=10, fill=tk.X)

        self.botao_codificar = ttk.Button(self.frame, text="Codificar Arquivo", command=self.codificar_arquivo)
        self.botao_codificar.pack(pady=10, fill=tk.X)

        self.botao_decodificar = ttk.Button(self.frame, text="Decodificar Arquivo", command=self.decodificar_arquivo)
        self.botao_decodificar.pack(pady=10, fill=tk.X)

        self.botao_ascii = ttk.Button(self.frame, text="Converter Imagem em ASCII", command=self.converter_imagem_ascii)
        self.botao_ascii.pack(pady=10, fill=tk.X)

        self.caminho_arquivo = None
        self.caminho_arquivo_codificado = None
        self.caminho_arquivo_arvore = None

    def carregar_arquivo(self):
        self.caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Binary files", "*.bin")]
        )
        if not self.caminho_arquivo:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
        else:
            messagebox.showinfo("Info", f"Arquivo selecionado: {self.caminho_arquivo}")

    def codificar_arquivo(self):
        if not self.caminho_arquivo:
            messagebox.showwarning("Aviso", "Por favor, carregue um arquivo primeiro.")
            return

        try:
            extensao_arquivo = os.path.splitext(self.caminho_arquivo)[1]
            if extensao_arquivo == '.txt':
                with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    texto = arquivo.read()
            elif extensao_arquivo == '.bin':
                with open(self.caminho_arquivo, 'rb') as arquivo:
                    texto = arquivo.read().decode('utf-8')
            else:
                raise ValueError("Tipo de arquivo não suportado")

            bytes_codificados = self.codificacao_huffman.codificar(texto)
            self.caminho_arquivo_arvore = self.caminho_arquivo + '.tree'
            self.codificacao_huffman.salvar_arvore(self.caminho_arquivo_arvore)

            caminho_arquivo_codificado = self.caminho_arquivo + '_encoded.bin'
            with open(caminho_arquivo_codificado, 'wb') as arquivo:
                arquivo.write(bytes_codificados)

            messagebox.showinfo("Info", f"Arquivo codificado com sucesso como {caminho_arquivo_codificado}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decodificar_arquivo(self):
        caminho_arquivo_codificado = filedialog.askopenfilename(
            filetypes=[("Binary files", "*_encoded.bin")]
        )
        if not caminho_arquivo_codificado:
            messagebox.showwarning("Aviso", "Nenhum arquivo codificado selecionado.")
            return

        caminho_arquivo_arvore = filedialog.askopenfilename(
            filetypes=[("Tree files", "*.tree")]
        )
        if not caminho_arquivo_arvore:
            messagebox.showwarning("Aviso", "Nenhum arquivo de árvore selecionado.")
            return

        try:
            self.codificacao_huffman.carregar_arvore(caminho_arquivo_arvore)

            with open(caminho_arquivo_codificado, 'rb') as arquivo:
                bytes_codificados = arquivo.read()

            texto_decodificado = self.codificacao_huffman.decodificar(bytes_codificados)

            caminho_arquivo_decodificado = caminho_arquivo_codificado.replace('_encoded.bin', '_decoded.txt')
            with open(caminho_arquivo_decodificado, 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto_decodificado)

            messagebox.showinfo("Info", f"Arquivo decodificado com sucesso como {caminho_arquivo_decodificado}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def converter_imagem_ascii(self):
        caminho_imagem = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        if not caminho_imagem:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada.")
            return

        try:
            self.image_to_ASCII(caminho_imagem)
            messagebox.showinfo("Info", "Imagem convertida para ASCII com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def hue_char(self, character):
        tamanho = (10, 10)
        imagem_temporaria = Image.new('L', tamanho, color=255)
        draw = ImageDraw.Draw(imagem_temporaria)
        fonte = ImageFont.load_default()

        draw.text((0, 0), character, font=fonte, fill=0)

        array_imagem = np.array(imagem_temporaria)

        quantidade_preenchida = np.sum(array_imagem < 255)

        return quantidade_preenchida

    def image_to_ASCII(self, image_path, output_width=720):
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f"Imagem não encontrada: {image_path}")
            return

        aspect_ratio = img.height / img.width
        new_height = aspect_ratio * output_width * 0.5
        img = img.resize((output_width, int(new_height)))

        img = img.convert('L')

        chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", ".", "M",
                 "!", "#", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
                 ":", " "]

        chars_hue = [self.hue_char(char) for char in chars]
        chars_sorted_by_hue = [char for _, char in sorted(zip(chars_hue, chars), reverse=True)]
        pixel_range = min(255 // (len(chars_sorted_by_hue) - 1), 255)

        pixels = img.getdata()
        new_pixels = [chars_sorted_by_hue[pixel // pixel_range] for pixel in pixels]
        new_pixels = ''.join(new_pixels)

        ascii_image = [new_pixels[index:index + output_width] for index in range(0, len(new_pixels), output_width)]
        ascii_image = "\n".join(ascii_image)

        archive_name = image_path.split("\\")[-1].split(".")[0]
        timestamp = int(dt.datetime.now().timestamp())
        output_filename = f"{archive_name}_ASCII_art_{timestamp}.txt"
        with open(output_filename, "w", encoding='utf-8') as f:
            f.write(ascii_image)

        print(f"Arte ASCII salva em {output_filename}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicativoHuffman(raiz)
    raiz.mainloop()
