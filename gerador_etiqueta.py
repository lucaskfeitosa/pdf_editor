import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128

class EtiquetaPDF:
    ETIQUETA_LARGURA = 35 * 2.83465
    ETIQUETA_ALTURA = 60 * 2.83465
    LARGURA_PAGINA = ETIQUETA_LARGURA * 3

    def __init__(self, nome_arquivo):
        self.c = canvas.Canvas(nome_arquivo, pagesize=(self.LARGURA_PAGINA, self.ETIQUETA_ALTURA))
        self.width, self.height = (self.LARGURA_PAGINA, self.ETIQUETA_ALTURA)
        self.descricao = ""
        self.tamanhos_quantidades = []
        self.cor = ""
        self.referencia = ""

    @staticmethod
    def mm2p(milimetros):
        return milimetros / 0.352777

    def set_descricao(self, descricao):
        self.descricao = descricao

    def set_tamanhos_quantidades(self, tamanhos_quantidades):
        self.tamanhos_quantidades = tamanhos_quantidades

    def set_cor(self, cor):
        self.cor = cor

    def set_referencia(self, referencia):
        self.referencia = referencia

    def draw_label(self, x_offset, tamanho, referencia_com_tamanho):
        image_path = 'unnamed2.jpeg'
        image_width = 60
        image_height = 60

        x_position = x_offset + (self.ETIQUETA_LARGURA - image_width) / 2
        y_position = self.height - 65
        self.c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height, preserveAspectRatio=True)

        font_size = 10
        self.c.setFont('Helvetica-Bold', font_size)
        max_width = self.ETIQUETA_LARGURA - 10
        self.draw_multiline_text(self.descricao, x_offset + 7, self.height - 70, max_width)

        self.draw_text('REF:', x_offset + 7, self.height - 90, font_size=9)
        self.draw_text(referencia_com_tamanho, x_offset + 30, self.height - 90, font_size=11)

        self.draw_text('TAM:', x_offset + 7, self.height - 105, font_size=9)
        self.draw_text(tamanho, x_offset + 30, self.height - 105, font_size=11)

        self.draw_text('COR:', x_offset + 7, self.height - 120, font_size=9)
        self.draw_text(self.cor, x_offset + 30, self.height - 120, font_size=11)

        barcode = code128.Code128(referencia_com_tamanho)
        barcode.barWidth = self.mm2p(0.2)
        barcode_height = self.mm2p(1)
        barcode_x_position = x_offset + (self.ETIQUETA_LARGURA - barcode.width) / 2
        barcode_y_position = self.height - 160
        barcode.drawOn(self.c, barcode_x_position, barcode_y_position)

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
        self.c.setFont('Helvetica-Bold', font_size)
        self.c.drawString(x, y, text)

    def salvar_pdf(self):
        x_offset = 0
        for tamanho, quantidade in self.tamanhos_quantidades:
            referencia_com_tamanho = f"{self.referencia}{tamanho}"
            for _ in range(quantidade):
                self.draw_label(x_offset, tamanho, referencia_com_tamanho)
                x_offset += self.ETIQUETA_LARGURA
                if x_offset >= self.LARGURA_PAGINA:
                    x_offset = 0
                    self.c.showPage()
        self.c.save()

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Etiquetas")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")

        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        main_frame.pack(expand=True)

        title_label = tk.Label(main_frame, text="Gerador de Etiquetas", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(main_frame, text="Descrição:", font=("Helvetica", 10), fg="white", bg="#1e1e1e").grid(row=1, column=0, sticky="e", pady=5)
        self.descricao_entry = tk.Entry(main_frame, width=40, bg="#333333", fg="white", insertbackground="white", font=("Helvetica", 10))
        self.descricao_entry.grid(row=1, column=1, pady=5)

        tk.Label(main_frame, text="Cor:", font=("Helvetica", 10), fg="white", bg="#1e1e1e").grid(row=2, column=0, sticky="e", pady=5)
        self.cor_entry = tk.Entry(main_frame, width=40, bg="#333333", fg="white", insertbackground="white", font=("Helvetica", 10))
        self.cor_entry.grid(row=2, column=1, pady=5)

        tk.Label(main_frame, text="Referência:", font=("Helvetica", 10), fg="white", bg="#1e1e1e").grid(row=3, column=0, sticky="e", pady=5)
        self.referencia_entry = tk.Entry(main_frame, width=40, bg="#333333", fg="white", insertbackground="white", font=("Helvetica", 10))
        self.referencia_entry.grid(row=3, column=1, pady=5)

        tk.Button(main_frame, text="Selecionar Tamanhos e Quantidades", command=self.selecionar_tamanhos, bg="#5a5a5a", fg="white", font=("Helvetica", 10)).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Gerar PDF", command=self.gerar_pdf, bg="#5a5a5a", fg="white", font=("Helvetica", 10)).grid(row=5, column=0, columnspan=2, pady=10)

        # Créditos no canto inferior direito
        credits_label = tk.Label(self.root, text="Feito por Lucas Feitosa", font=("Helvetica", 8), fg="white", bg="#1e1e1e")
        credits_label.pack(side="bottom", anchor="e", pady=5, padx=5)

        self.root.mainloop()

    def selecionar_tamanhos(self):
        top = tk.Toplevel(self.root)
        top.title("Tamanhos e Quantidades")
        top.geometry("500x500")
        top.configure(bg="#1e1e1e")

        tk.Label(top, text="Selecione as Quantidades para cada Tamanho", font=("Helvetica", 12, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

        frame_tamanhos = tk.Frame(top, bg="#1e1e1e")
        frame_tamanhos.pack(pady=10)

        tamanhos_numericos = [str(i) for i in range(34, 47)]
        tamanhos_letras = ["PP", "P", "M", "G", "GG"]
        self.entries = []

        for idx, tamanho in enumerate(tamanhos_numericos + tamanhos_letras):
            row = idx // 4
            col = idx % 4

            sub_frame = tk.Frame(frame_tamanhos, bg="#1e1e1e", pady=5, padx=5)
            sub_frame.grid(row=row, column=col, padx=10, pady=5)

            tk.Label(sub_frame, text=tamanho, fg="white", bg="#1e1e1e", font=("Helvetica", 10)).pack()
            quantidade_entry = tk.Entry(sub_frame, width=5, bg="#333333", fg="white", insertbackground="white", font=("Helvetica", 10))
            quantidade_entry.pack()
            self.entries.append((tamanho, quantidade_entry))

        tk.Button(top, text="Salvar", command=lambda: self.salvar_tamanhos(top), bg="#5a5a5a", fg="white", font=("Helvetica", 10)).pack(pady=20)

    def salvar_tamanhos(self, top):
        self.tamanhos_quantidades = []
        for tamanho, quantidade_entry in self.entries:
            try:
                quantidade = int(quantidade_entry.get())
                if quantidade > 0:
                    self.tamanhos_quantidades.append((tamanho, quantidade))
            except ValueError:
                continue
        top.destroy()

    def gerar_pdf(self):
        descricao = self.descricao_entry.get()
        cor = self.cor_entry.get()
        referencia = self.referencia_entry.get()

        if not descricao or not cor or not referencia or not self.tamanhos_quantidades:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos e selecione os tamanhos.")
            return

        etiqueta_pdf = EtiquetaPDF('etiquetas.pdf')
        etiqueta_pdf.set_descricao(descricao)
        etiqueta_pdf.set_cor(cor)
        etiqueta_pdf.set_referencia(referencia)
        etiqueta_pdf.set_tamanhos_quantidades(self.tamanhos_quantidades)
        etiqueta_pdf.salvar_pdf()

        messagebox.showinfo("Sucesso", "Etiquetas geradas no arquivo etiquetas.pdf!")

if __name__ == "__main__":
    App()
