import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
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
        # Para evitar interferencia de usos anteriores:
        self.codigos.clear() # Limpar dicionário de códigos 
        self.codigos_reversos.clear()  # Limpar dicionário de códigos reversos
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
        self.raiz.title("ArtCompress")
        self.raiz.geometry("600x500")
        self.raiz.configure(bg='#f3efef')

        self.titulo_ascii_art = """                                                                                                             .         .                                                                                      
         .8.          8 888888888o. 8888888 8888888888               ,o888888o.        ,o888888o.           ,8.       ,8.          8 888888888o   8 888888888o.   8 8888888888     d888888o.      d888888o.   
        .888.         8 8888    `88.      8 8888                    8888     `88.   . 8888     `88.        ,888.     ,888.         8 8888    `88. 8 8888    `88.  8 8888         .`8888:' `88.  .`8888:' `88. 
       :88888.        8 8888     `88      8 8888                 ,8 8888       `8. ,8 8888       `8b      .`8888.   .`8888.        8 8888     `88 8 8888     `88  8 8888         8.`8888.   Y8  8.`8888.   Y8 
      . `88888.       8 8888     ,88      8 8888                 88 8888           88 8888        `8b    ,8.`8888. ,8.`8888.       8 8888     ,88 8 8888     ,88  8 8888         `8.`8888.      `8.`8888.     
     .8. `88888.      8 8888.   ,88'      8 8888                 88 8888           88 8888         88   ,8'8.`8888,8^8.`8888.      8 8888.   ,88' 8 8888.   ,88'  8 888888888888  `8.`8888.      `8.`8888.    
    .8`8. `88888.     8 888888888P'       8 8888                 88 8888           88 8888         88  ,8' `8.`8888' `8.`8888.     8 888888888P'  8 888888888P'   8 8888           `8.`8888.      `8.`8888.   
   .8' `8. `88888.    8 8888`8b           8 8888                 88 8888           88 8888        ,8P ,8'   `8.`88'   `8.`8888.    8 8888         8 8888`8b       8 8888            `8.`8888.      `8.`8888.  
  .8'   `8. `88888.   8 8888 `8b.         8 8888                 `8 8888       .8' `8 8888       ,8P ,8'     `8.`'     `8.`8888.   8 8888         8 8888 `8b.     8 8888        8b   `8.`8888. 8b   `8.`8888. 
 .888888888. `88888.  8 8888   `8b.       8 8888                    8888     ,88'   ` 8888     ,88' ,8'       `8        `8.`8888.  8 8888         8 8888   `8b.   8 8888        `8b.  ;8.`8888 `8b.  ;8.`8888 
.8'       `8. `88888. 8 8888     `88.     8 8888                     `8888888P'        `8888888P'  ,8'         `         `8.`8888. 8 8888         8 8888     `88. 8 888888888888 `Y8888P ,88P'  `Y8888P ,88P' 
        """

        # Adicionar o título em ASCII Art à interface
        titulo_label = tk.Label(self.raiz, text=self.titulo_ascii_art, font=("Courier", 3), justify=tk.CENTER)
        titulo_label.pack(pady=10, padx=10, anchor='center')

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

        self.botao_codificar = ttk.Button(self.frame, text="Comprimir Arquivo", command=self.codificar_arquivo)
        self.botao_codificar.pack(pady=10, fill=tk.X)

        self.botao_decodificar = ttk.Button(self.frame, text="Descomprimir Arquivo", command=self.decodificar_arquivo)
        self.botao_decodificar.pack(pady=10, fill=tk.X)

        self.botao_ascii = ttk.Button(self.frame, text="Converter Imagem em ASCII art", command=self.converter_imagem_ascii)
        self.botao_ascii.pack(pady=10, fill=tk.X)

        self.botao_abrir_arquivo = ttk.Button(self.raiz, text="Visualizar ASCII art", command=self.abrir_arquivo_ascii)
        self.botao_abrir_arquivo.pack(pady=10)

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
            # obter o tamanho do arquivo original
            tamanho_original = os.path.getsize(self.caminho_arquivo)

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
            
            # Cria uma subpasta para armazenar os arquivos .bin e .tree
            pasta_output = self.criar_diretorio_output(self.caminho_arquivo, 1)

            nome_base = os.path.basename(self.caminho_arquivo)
            self.caminho_arquivo_arvore = os.path.join(pasta_output, nome_base + '.tree')
            self.codificacao_huffman.salvar_arvore(self.caminho_arquivo_arvore)

            # Salvar a árvore e o arquivo comprimido
            caminho_arquivo_codificado = os.path.join(pasta_output, nome_base + '_encoded.bin')
            with open(caminho_arquivo_codificado, 'wb') as arquivo:
                arquivo.write(bytes_codificados)

            # Obter o tamanho do arquivo comprimido = .bin + .tree
            tamanho_comprimido = os.path.getsize(caminho_arquivo_codificado)

            # Calcular o percentual de compressão
            razao_tamanho = tamanho_comprimido/tamanho_original
            percentual_compressao = (1 - razao_tamanho ) * 100

            # Formatar tamanhos para unidades legíveis
            tamanho_original_formatado = self.tamanho_formatado(tamanho_original)
            tamanho_comprimido_formatado = self.tamanho_formatado(tamanho_comprimido)

            messagebox.showinfo("Info", f"Arquivo codificado com sucesso como {caminho_arquivo_codificado}\n")
            messagebox.showinfo(
                "Resultado",
                f"Compressão: {tamanho_original_formatado} -> {tamanho_comprimido_formatado}\n"
                f"Redução de {(percentual_compressao):.2f}%"
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    @staticmethod
    def tamanho_formatado(tamanho_bytes):
        if tamanho_bytes == 0:
            return "0B"
        tamanho_nomes = ("B", "KB", "MB", "GB", "TB")
        i = int(np.floor(np.log(tamanho_bytes) / np.log(1024)))
        p = np.power(1024, i)
        s = round(tamanho_bytes / p, 2)
        return f"{s} {tamanho_nomes[i]}"

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

            # Obter o diretório pai onde a pasta do arquivo codificado e da árvore está localizada
            pasta_pai = os.path.dirname(os.path.dirname(caminho_arquivo_codificado))
        
            caminho_arquivo_decodificado = os.path.join(pasta_pai, os.path.splitext(os.path.splitext(os.path.basename(caminho_arquivo_codificado))[0])[0] + '.txt')

            with open(caminho_arquivo_decodificado, 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto_decodificado)

            messagebox.showinfo("Info", f"Arquivo decodificado com sucesso como {caminho_arquivo_decodificado}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def converter_imagem_ascii(self):
        caminho_imagem = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
        )
        if not caminho_imagem:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada.")
            return

        largura = simpledialog.askinteger("Largura da Arte ASCII", "Insira a largura da arte ASCII (entre 100 e 900):", initialvalue= 720, minvalue=100, maxvalue=900)
        if not largura:
            messagebox.showwarning("Aviso", "Largura não selecionada.")
            return
        if largura < 720:
            resposta = messagebox.askokcancel("Atenção", "Abaixo de 720, pode-se tornar mais dificil a compreensão da imagem. Prosseguir ?")
            if not resposta:
                return # operação cancelada 

        try:
            output_filename, ascii_art = self.image_to_ASCII(caminho_imagem, largura)
            messagebox.showinfo("Info", f"Imagem convertida para ASCII com sucesso. Arquivo salvo em: {output_filename}")
            self.mostrar_ascii_art(ascii_art)
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
    
    @staticmethod
    def criar_diretorio_output(caminho_arquivo, arquivo_compactado= 0):
        # Diretório de saída padrão
        output_root_dir = "outputs"
        if not os.path.exists(output_root_dir):
            os.makedirs(output_root_dir)

        # Nome da subpasta baseado no nome do arquivo
        nome_base = os.path.basename(caminho_arquivo)
        nome_pasta = os.path.splitext(nome_base)[0]
        if arquivo_compactado:
            nome_pasta += ".huff"

        # Caminho completo para a subpasta
        pasta_output = os.path.join(output_root_dir, nome_pasta)
        if not os.path.exists(pasta_output):
            os.makedirs(pasta_output)

        return pasta_output

    def image_to_ASCII(self, image_path, output_width=720):
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f"Imagem não encontrada: {image_path}")
            return

        # Cria uma subpasta para armazenar o arquivo ASCII
        pasta_output = self.criar_diretorio_output(image_path)

        # medidas da tela
        screen_width = self.raiz.winfo_screenwidth()
        screen_height = self.raiz.winfo_screenheight()
        aspect_ratio_screen = screen_height/screen_width # proporção da tela
        
        #medidas adptadas da imagem (altura/largura)
        aspect_ratio = img.height / img.width # proporção da imagem

        # Tem se que as seguinte ajustes são otimos: 720p => 0.7 & 900p => 0.75 & 360p => 0.68
        # Por Regressão quadratica: f(x) = (4.0*10^-7) * x^2+ -0.00039*x + 0,77
        adjustment_factor = (4 * 10**(-7))*(output_width**2) + (-3.9 * 10**(-4)) * output_width + 0.77

        # nova altura calculada com ajustes
        new_height = int(aspect_ratio * output_width * aspect_ratio_screen * adjustment_factor) 

        img = img.resize((output_width, new_height))

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

        # Salvar a arte ASCII no arquivo dentro da subpasta criada
        nome_base = os.path.splitext(os.path.basename(image_path))[0]
        timestamp = int(dt.datetime.now().timestamp())
        output_filename = os.path.join(pasta_output, f"{nome_base}_{timestamp}_artAscii.txt")
        with open(output_filename, "w", encoding='utf-8') as f:
            f.write(ascii_image)

        print(f"Arte ASCII salva in {output_filename}")
        
        return output_filename, ascii_image
    
    def mostrar_ascii_art(self, ascii_art):
        
        # "Lucida Console" => melhorar representação e proporção
        def aumentar_fonte():
            tamanho_atual = text_widget.cget("font").split(" ")[-1]
            novo_tamanho = int(tamanho_atual) + 2
            text_widget.config(font=("Lucida Console", novo_tamanho))

        def diminuir_fonte():
            tamanho_atual = text_widget.cget("font").split(" ")[-1]
            novo_tamanho = max(1, int(tamanho_atual) - 2)  # Limite mínimo de 6 para evitar tamanho muito pequeno
            text_widget.config(font=("Lucida Console", novo_tamanho))

        janela_ascii = tk.Toplevel(self.raiz)
        janela_ascii.title("Visualização ASCII Art")

        largura = self.raiz.winfo_screenwidth()
        altura = self.raiz.winfo_screenheight()
        janela_ascii.geometry(f"{int(largura * 0.4)}x{int(altura * 0.8)}")

        text_widget = tk.Text(janela_ascii, wrap=tk.NONE, font=('Lucida Console', 10))
        text_widget.insert(tk.END, ascii_art)
        text_widget.config(state=tk.DISABLED)  # Tornar o widget de texto somente leitura
        text_widget.pack(expand=True, fill=tk.BOTH)

        scrollbar_y = ttk.Scrollbar(janela_ascii, orient='vertical', command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(janela_ascii, orient='horizontal', command=text_widget.xview)
        text_widget.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        frame_botoes = ttk.Frame(janela_ascii)
        frame_botoes.pack(pady=5)

        botao_zoom_in = ttk.Button(frame_botoes, text="Zoom In", command=aumentar_fonte)
        botao_zoom_in.grid(row=0, column=0, padx=5)

        botao_zoom_out = ttk.Button(frame_botoes, text="Zoom Out", command=diminuir_fonte)
        botao_zoom_out.grid(row=0, column=1, padx=5)

    def abrir_arquivo_ascii(self):
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if not caminho_arquivo:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return

        try:
            with open(caminho_arquivo, "r", encoding='utf-8') as f:
                ascii_art = f.read()
            self.mostrar_ascii_art(ascii_art)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicativoHuffman(raiz)
    raiz.mainloop()
