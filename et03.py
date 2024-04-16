import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import styles
from reportlab.platypus import Paragraph
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import landscape, legal
import streamlit as st
from io import BytesIO

# Registra la fuente Arial
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
# Define un estilo de párrafo con texto justificado
#style = styles.getSampleStyleSheet()['Normal']
#style.alignment = styles.TA_JUSTIFY
style = ParagraphStyle(name='Centered', alignment=TA_CENTER, fontName='Arial', fontSize=12, leading=14)

# Tamaño de la página oficio en paisaje
pagina_ancho, pagina_alto = landscape((34*cm, 21.6*cm))

# Dimensiones especificadas para cada sección
ancho_etiqueta = 7.0 * cm
alto_etiqueta = 4.0 * cm
alto_seccion_superior_inferior = 0.25 * cm
ancho_seccion_superior_inferior = 7.0 * cm
ancho_seccion_1 = 1.8 * cm
alto_seccion_1 = 2.0 * cm
ancho_seccion_2 = 5.2 * cm
alto_seccion_2 = 2.0 * cm
ancho_seccion_3 = 7.0 * cm
alto_seccion_3 = 1.5 * cm
espacio = 0.5 * cm

# Define la ruta al logo
logo_path = 'logoUPP.jpg'

# Función para crear la etiqueta personalizada sin marcos
def create_custom_label(pdf, x, y, name, educational_program, logo_path):
    pdf.drawImage(logo_path, x, y + alto_seccion_superior_inferior + alto_seccion_3, ancho_seccion_1, alto_seccion_1, preserveAspectRatio=True, anchor='c')
 
    paragraph = Paragraph(name, style)
    w_text, h_text = paragraph.wrap(ancho_seccion_2 - 0.2 * cm, alto_seccion_2 - 0.15 * cm)  # Prepara el párrafo para que se ajuste al ancho y alto definidos
    paragraph.drawOn(pdf, x + ancho_seccion_1, y + alto_seccion_superior_inferior + alto_seccion_3 + alto_seccion_2/2 - h_text/2)  # Dibuja el párrafo en el canvas, posicionado en (x, y)

    paragraph = Paragraph(educational_program, style)
    w_text, h_text = paragraph.wrap(ancho_seccion_3 - 0.2 * cm, alto_seccion_3 - 0.1 * cm)  # Prepara el párrafo para que se ajuste al ancho y alto definidos
    paragraph.drawOn(pdf, x, y + alto_seccion_superior_inferior + alto_seccion_3/2 - h_text/2)  # Dibuja el párrafo en el canvas, posicionado en (x, y)
    
    pdf.setLineWidth(2)
    pdf.rect(x, y, ancho_etiqueta, alto_etiqueta)

def create_pdf(bytes_data):
    df = pd.read_excel(bytes_data)
    #pdf_filename = 'etiquetas.pdf'
    pdf_buffer = BytesIO()
    pdf = Canvas(pdf_buffer, pagesize=(pagina_ancho, pagina_alto))
    
    x = espacio
    y = landscape(legal)[1] - alto_etiqueta - espacio
    for index, row in df.iterrows():
        create_custom_label(pdf, x, y, row['NOMBRE'], row['P.E.'], logo_path)
        
        x += ancho_etiqueta + espacio
        if x + ancho_etiqueta > pagina_ancho:
            x = espacio
            y -= alto_etiqueta + espacio
        
        if y < 0:
            pdf.showPage()
            y = pagina_alto - alto_etiqueta - espacio
    
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Título del app
st.title('Cargador y Descargador de PDF')
# Cargador de archivos
uploaded_file = st.file_uploader("Elige un archivo PDF", type=['xlsx'])
if uploaded_file is not None:
    # Para leer el archivo PDF
    bytes_data = uploaded_file.getvalue()
    pdf_etiquetas = create_pdf(bytes_data)
     # Botón de descarga para el PDF generado
    st.download_button(
        label="Descargar PDF",
        data=pdf_etiquetas,
        file_name="etiquetas.pdf",
        mime='application/pdf'
    )
