from cx_Freeze import setup, Executable

# Dependências que precisam ser incluídas
build_exe_options = {
    "packages": ["tkinter", "reportlab"],
    "include_files": ["unnamed2.jpeg"],  # Inclua qualquer arquivo adicional necessário
}

setup(
    name="Gerador de Etiquetas",
    version="0.1",
    description="Um aplicativo para gerar etiquetas em PDF.",
    options={"build_exe": build_exe_options},
    executables=[Executable("gerador_etiqueta.py", base=None)],  # base=None para Windows
)