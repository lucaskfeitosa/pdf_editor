from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.barcode import code128

class EtiquetaPDF:
    # Definições de tamanho em pontos
    ETIQUETA_LARGURA = 35 * 2.83465  # Largura em pontos
    ETIQUETA_ALTURA = 60 * 2.83465   # Altura em pontos
    LARGURA_PAGINA = ETIQUETA_LARGURA * 3  # Largura total para 3 etiquetas

    def __init__(self, nome_arquivo, descricao, tamanho, cor, referencia):
        self.c = canvas.Canvas(nome_arquivo, pagesize=(self.LARGURA_PAGINA, self.ETIQUETA_ALTURA))
        self.width, self.height = (self.LARGURA_PAGINA, self.ETIQUETA_ALTURA)
        self.__descricao = descricao
        self.__tamanho = tamanho
        self.__cor = cor
        self.__referencia = referencia

    @staticmethod
    def mm2p(milimetros):
        """Converte milímetros para pontos."""
        return milimetros / 0.352777

    def draw_label(self, x_offset):
        """Desenha uma etiqueta no canvas."""
        # Adicionar imagem
        image_path = 'unnamed.jpg'  # Caminho da sua imagem
        image_width = 35  # Largura da imagem em pontos
        image_height = 35  # Altura da imagem em pontos

        # Centralizar imagem na etiqueta
        x_position = x_offset + (self.ETIQUETA_LARGURA - image_width) / 2
        y_position = self.height - 45  
        self.c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height, preserveAspectRatio=True)

        # Desenhar descrição na etiqueta
        font_size = 10
        self.c.setFont('Helvetica-Bold', font_size)
        
        max_width = self.ETIQUETA_LARGURA - 10  
        self.draw_multiline_text(self.__descricao, x_offset + 5, self.height - 60, max_width)

        # Desenhar outros textos com ajuste de fonte e posição
        self.draw_text('REF:', x_offset + 5, self.height - (80 + (font_size + 2)), font_size=9)
        self.draw_text(self.__referencia, x_offset + 28, self.height - (80 + (font_size + 2)), font_size=11)

        self.draw_text('TAM:', x_offset + 5, self.height - (95 + (font_size + 2)), font_size=9)
        self.draw_text(self.__tamanho, x_offset + 28, self.height - (95 + (font_size + 2)), font_size=11)

        # Ajuste do tamanho da fonte para a cor
        cor_font_size = self.adjust_font_size_for_color(self.__cor)
        
        self.draw_text('COR:', x_offset + 5, self.height - (110 + (font_size + 2)), font_size=9)
        
        # Desenhar a cor na etiqueta com o tamanho de fonte ajustado
        self.draw_text(self.__cor, x_offset + 28, self.height - (110 + (font_size + 2)), font_size=cor_font_size)

        # Código de barras com aumento de tamanho
        barcode_value = self.__referencia  
        barcode = code128.Code128(barcode_value)

        barcode.barWidth = self.mm2p(0.3)   
        barcode_height = self.mm2p(20)       

        barcode_x_position = x_offset + (self.ETIQUETA_LARGURA - barcode.width) / 2
        barcode_y_position = self.height - (150)

        barcode.drawOn(self.c, barcode_x_position, barcode_y_position)

        self.c.setFont('Helvetica-Bold', 8)   

        # Desenhar número abaixo do código de barras centralizado
        self.c.drawString(barcode_x_position + (barcode.width / 2) - (self.c.stringWidth(barcode_value) / 2), 
                          barcode_y_position - barcode_height - 5,
                          barcode_value)

    def adjust_font_size_for_color(self, color):
        """Ajusta o tamanho da fonte com base no comprimento do texto da cor."""
        base_font_size = 11
        max_width_available = self.ETIQUETA_LARGURA - 40  # Largura disponível para o texto da cor

        while True:
            text_width = self.c.stringWidth(color, "Helvetica-Bold", base_font_size)
            if text_width <= max_width_available:
                break
            base_font_size -= 1
            
            if base_font_size < 6:  # Limite mínimo para a fonte
                break
        
        return base_font_size

    def draw_multiline_text(self, text, x, y, max_width):
        """Desenha texto multilinha no canvas."""
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
        """Salva o PDF gerado."""
        for i in range(3):
            self.draw_label(i * self.ETIQUETA_LARGURA)
        
        # Salvar o PDF
        self.c.save()

    def inserir_referencia(self):
        referencia = input('digite a referência: ')
        return referencia

    def inserir_tamanho(self):
        tamanho = input('digite o tamanho: ')
        return tamanho
    
    def inserir_cor(self):
        cor = input('digite a cor: ')
        return cor

# Exemplo de uso da classe EtiquetaPDF com informações personalizadas incluindo referência e cor responsiva
if __name__ == "__main__":
    descricao_produto = 'JAQUETA MASCULINA'
    tamanho_produto = 'P'
    cor_produto = 'VERDE'
    referencia_produto = '800612P'   
    
    etiqueta_pdf = EtiquetaPDF('meu_pdf.pdf', descricao_produto,
                                tamanho_produto,
                                cor_produto,
                                referencia_produto)
    etiqueta_pdf.salvar_pdf()