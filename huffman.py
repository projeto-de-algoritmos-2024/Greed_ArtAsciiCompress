import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import heapq
import os
from collections import Counter
import pickle

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

        # Estilo para widgets
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

        # Layout da interface
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

        self.caminho_arquivo = None
        self.caminho_arquivo_codificado = None

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
            arquivo_arvore = self.caminho_arquivo + '.tree'
            self.codificacao_huffman.salvar_arvore(arquivo_arvore)

            caminho_arquivo_codificado = self.caminho_arquivo + '_encoded.bin'
            with open(caminho_arquivo_codificado, 'wb') as arquivo:
                arquivo.write(bytes_codificados)

            messagebox.showinfo("Info", f"Arquivo codificado com sucesso como {caminho_arquivo_codificado}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decodificar_arquivo(self):
        if not self.caminho_arquivo:
            messagebox.showwarning("Aviso", "Por favor, carregue um arquivo primeiro.")
            return

        try:
            caminho_arquivo_codificado = filedialog.askopenfilename(
                filetypes=[("Binary files", "*_encoded.bin")]
            )
            if not caminho_arquivo_codificado:
                messagebox.showwarning("Aviso", "Nenhum arquivo codificado selecionado.")
                return

            arquivo_arvore = self.caminho_arquivo + '.tree'
            self.codificacao_huffman.carregar_arvore(arquivo_arvore)

            with open(caminho_arquivo_codificado, 'rb') as arquivo:
                bytes_codificados = arquivo.read()

            texto_decodificado = self.codificacao_huffman.decodificar(bytes_codificados)

            caminho_arquivo_decodificado = self.caminho_arquivo + '_decoded.txt'
            with open(caminho_arquivo_decodificado, 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto_decodificado)

            messagebox.showinfo("Info", f"Arquivo decodificado com sucesso como {caminho_arquivo_decodificado}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicativoHuffman(raiz)
    raiz.mainloop()
