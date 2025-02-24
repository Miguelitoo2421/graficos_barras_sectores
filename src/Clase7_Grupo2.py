import pandas as pd        # tratar los datos frames (tablas en python)
import altair as alt       # elaborar gráficos
import datapane as dp      # generar informes
import os

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QComboBox, QVBoxLayout, QWidget, QApplication

fichero_csv = "prueba.csv"
df = pd.read_csv(fichero_csv)

def generar_informe(mes):
    datos_mes = df[df['Mes'] == mes]

    ## GRAFICO DE BARRAS
    grafico_barras = alt.Chart(datos_mes).mark_bar().encode(
        x="Nombre:N", y="Importe:Q", color="Nombre:N"
    ).properties(title= f"Ventas por vendedor en {mes}")


    ## GRÁFICO DE SECTORES
    datos_agg = datos_mes.groupby('Nombre')['Unidades'].sum().reset_index()
    grafico_sectores = alt.Chart(datos_agg).mark_arc().encode(
        theta='Unidades:Q', color='Nombre:N'
    ).properties(title= f"Distribución de unidades vendidas en {mes}")

    ## INTRODUCIR HTML
    titulo1 = dp.HTML('<h1 style= "color:blue; text-align: center">Gráfico de Barras</h1>')
    titulo2 = dp.HTML('<h1 style= "color:blue; text-align: center">Gráfico de Sectores</h1>')

    reporte = dp.Report(
        titulo1,
        grafico_barras,
        titulo2,
        grafico_sectores
    )

    ruta_reporte = os.path.abspath("informe_ventas2.html")
    reporte.save(ruta_reporte)

## CLASE VENTANA PRINCIPAL (NO ENTRA AL EXAMEN)
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informe Ventas")

        self.selector_mes = QComboBox()
        self.selector_mes.addItems(df["Mes"].unique())
        self.selector_mes.currentIndexChanged.connect(self.actualizar_reporte)

        self.vista_web = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.selector_mes)
        layout.addWidget(self.vista_web)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

    def actualizar_reporte(self):
        mes_seleccionado = self.selector_mes.currentText()
        generar_informe(mes_seleccionado)
        ruta_reporte = os.path.abspath("informe_ventas2.html")
        if os.path.exists(ruta_reporte):
            with open(ruta_reporte, "r", encoding='utf-8') as file:
                html_content = file.read()
                self.vista_web.setHtml(html_content)



if __name__ == "__main__":
    #generar_informe("Enero") ------> esta llamada es la que va para el examen
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
