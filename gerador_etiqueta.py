import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.barcode import code128

class EtiquetaPDF:
    # Definições de tamanho em pontos
    ETIQUETA_LARGURA = 35 * 2.83465  # Largura em pontos
    ETIQUETA_ALTURA = 60 * 2.83465   # Altura em pontos
    LARGURA_PAGINA = ETIQUETA_LARGURA * 3  # Largura total para 3 etiquetas

    def __init__(self, nome_arquivo):
        self.c = canvas.Canvas(nome_arquivo, pagesize=(self.LARGURA_PAGINA, self.ETIQUETA_ALTURA))
        self.width, self.height = (self.LARGURA_PAGINA, self.ETIQUETA_ALTURA)
        self.descricao = ""
        self.tamanho = ""
        self.cor = ""
        self.referencia = ""

    @staticmethod
    def mm2p(milimetros):
        """Converte milímetros para pontos."""
        return milimetros / 0.352777

    def set_descricao(self, descricao):
        """Define a descrição do produto."""
        self.descricao = descricao

    def set_tamanho(self, tamanho):
        """Define o tamanho do produto."""
        self.tamanho = tamanho

    def set_cor(self, cor):
        """Define a cor do produto."""
        self.cor = cor

    def set_referencia(self, referencia):
        """Define a referência do produto."""
        self.referencia = referencia

    def draw_label(self, x_offset):
        """Desenha uma etiqueta no canvas."""
        image_path = 'unnamed2.jpeg'  # Caminho da sua imagem
        image_width = 60  
        image_height = 60  

        x_position = x_offset + (self.ETIQUETA_LARGURA - image_width) / 2
        y_position = self.height - 65  
        self.c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height, preserveAspectRatio=True)

        font_size = 10
        self.c.setFont('Helvetica-Bold', font_size)
        
        max_width = self.ETIQUETA_LARGURA - 10  
        self.draw_multiline_text(self.descricao, x_offset + 7, self.height - 70, max_width)

        self.draw_text('REF:', x_offset + 7, self.height - (90 + (font_size + 2)), font_size=9)
        self.draw_text(self.referencia, x_offset + 30, self.height - (90 + (font_size + 2)), font_size=11)

        self.draw_text('TAM:', x_offset + 7, self.height - (105 + (font_size + 2)), font_size=9)
        self.draw_text(self.tamanho, x_offset + 30, self.height - (105 + (font_size + 2)), font_size=11)

        cor_font_size = self.adjust_font_size_for_color(self.cor)
        
        self.draw_text('COR:', x_offset + 7, self.height - (120 + (font_size + 2)), font_size=9)
        
        self.draw_text(self.cor, x_offset + 30, self.height - (120 + (font_size + 2)), font_size=cor_font_size)

        barcode_value = self.referencia  
        barcode = code128.Code128(barcode_value)

        barcode.barWidth = self.mm2p(0.2)   
        barcode_height = self.mm2p(1)       

        barcode_x_position = x_offset + (self.ETIQUETA_LARGURA - barcode.width) / 2
        barcode_y_position = self.height - (160)

        barcode.drawOn(self.c, barcode_x_position, barcode_y_position)

    def adjust_font_size_for_color(self, color):
        base_font_size = 11
        max_width_available = self.ETIQUETA_LARGURA - 40  

        while True:
            text_width = self.c.stringWidth(color, "Helvetica-Bold", base_font_size)
            if text_width <= max_width_available:
                break
            base_font_size -= 1
            
            if base_font_size < 6:  
                break
        
        return base_font_size

    def draw_multiline_text(self, text, x, y, max_width):
        words = text.split(' ')
        line = ''
        
        for word in words:
            if self.c.stringWidth(line + word, "Helvetica-Bold", 10) < max_width:
                line += word + ' '
            else:
                self.c.drawString(x, y, line.strip())
                line = word + ' '
                y -= 12

        if line:
            self.c.drawString(x, y, line.strip())

    def draw_text(self, text, x, y, font_size=10):
        """Desenha texto simples no canvas."""
        self.c.setFont('Helvetica-Bold', font_size)
        self.c.drawString(x, y, text)

    def salvar_pdf(self):
       # Salvar o PDF apenas uma vez após desenhar todas as etiquetas.
       for i in range(3):
           self.draw_label(i * self.ETIQUETA_LARGURA)
       self.c.save()
       



class App:
    def __init__(self):
       self.root = tk.Tk()
       self.root.title("Gerador de Etiquetas")
       window_width = 600
       window_height = 400
       screen_width = self.root.winfo_screenwidth()
       screen_height = self.root.winfo_screenheight()
       x_coordinate = int((screen_width / 2) - (window_width / 2))
       y_coordinate = int((screen_height / 2) - (window_height / 2))
       self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
       
       
       

       # Configurar a centralização dos widgets usando grid
       frame = tk.Frame(self.root)
       frame.pack(expand=True)

       # Labels e Entradas para os dados da etiqueta
       tk.Label(frame, text="Descrição:").grid(row=0)
       tk.Label(frame, text="Tamanho:").grid(row=1)
       tk.Label(frame, text="Cor:").grid(row=2)
       tk.Label(frame, text="Referência:").grid(row=3)
       tk.Label(frame, text="Quantidade:").grid(row=4)   # Nova label para quantidade

       # Entradas de texto
       self.descricao_entry = tk.Entry(frame)
       self.tamanho_entry = tk.Entry(frame)
       self.cor_entry = tk.Entry(frame)
       self.referencia_entry = tk.Entry(frame)
       self.quantidade_entry = tk.Entry(frame)   # Nova entrada para quantidade

       # Posicionamento das entradas no frame centralizado
       self.descricao_entry.grid(row=0, column=1)
       self.tamanho_entry.grid(row=1, column=1)
       self.cor_entry.grid(row=2, column=1)
       self.referencia_entry.grid(row=3, column=1)
       self.quantidade_entry.grid(row=4, column=1)   # Posicionamento da nova entrada

       # Botão para gerar o PDF
       tk.Button(frame, text="Gerar PDF", command=self.gerar_pdf).grid(row=5)

       # Iniciar o loop da interface gráfica
       self.root.mainloop()

    def gerar_pdf(self):
       """Gera o PDF com as informações inseridas."""
       descricao = self.descricao_entry.get()
       tamanho = self.tamanho_entry.get()
       cor = self.cor_entry.get()
       referencia = self.referencia_entry.get()
       
       quantidade_str = self.quantidade_entry.get()   # Coletar quantidade inserida
       
       if not descricao or not tamanho or not cor or not referencia or not quantidade_str:
           messagebox.showwarning("Entrada Inválida", "Por favor preencha todos os campos.")
           return

       try:
           quantidade = int(quantidade_str)   # Converter a quantidade para inteiro
           if quantidade <= 0:
               raise ValueError("A quantidade deve ser um número positivo.")
           
           etiqueta_pdf_nome_arquivo = 'etiquetas.pdf'
           etiqueta_pdf = EtiquetaPDF(etiqueta_pdf_nome_arquivo)

           etiqueta_pdf.set_descricao(descricao)
           etiqueta_pdf.set_tamanho(tamanho)
           etiqueta_pdf.set_cor(cor)
           etiqueta_pdf.set_referencia(referencia)   

           for _ in range(quantidade):   # Gerar múltiplas etiquetas conforme solicitado
               etiqueta_pdf.salvar_pdf()

           messagebox.showinfo("Sucesso", f"{quantidade} PDF(s) gerado(s) com sucesso!")

       except ValueError as e:
           messagebox.showerror("Erro", str(e))

# Executar o aplicativo
if __name__ == "__main__":
    App()