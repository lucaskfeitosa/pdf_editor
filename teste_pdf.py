import pikepdf
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    # Usando pikepdf apenas para verificar se o PDF pode ser aberto
    with pikepdf.open(pdf_path) as pdf:
        print(f"O PDF contém {len(pdf.pages)} páginas.")

    # Usando pdfminer para extrair texto
    text = extract_text(pdf_path)
    return text

# Exemplo de uso
pdf_file = 'relatorio.pdf'
extracted_text = extract_text_from_pdf(pdf_file)
print(extracted_text)

import fitz  # PyMuPDF

def remove_specific_text(input_pdf, output_pdf, text_to_remove):
    # Abrir o arquivo PDF
    document = fitz.open(input_pdf)

    for page in document:
        # Extrair texto da página
        text = page.get_text("text")

        # Dividir o texto em linhas
        lines = text.split('\n')
        new_lines = []

        # Filtrar linhas que não contêm o texto a ser removido
        for line in lines:
            if text_to_remove not in line:
                new_lines.append(line)

        # Criar um novo texto sem as linhas indesejadas
        new_text = "\n".join(new_lines)

        # Limpar a página e adicionar o novo texto
        page.clean_contents()  # Limpa conteúdo anterior

        # Adicionar o novo texto na mesma posição original
        page.insert_text((0, 0), new_text, fontsize=12)

    # Salvar o novo PDF sem as descrições
    document.save(output_pdf)
    document.close()

# Exemplo de uso
text_to_remove = "- 151612P - MINI SAIA\nCARGO CÓS ELÁSTICO\nP VERDE MILITAR"
remove_specific_text("relatorio.pdf", "saida.pdf", text_to_remove)