import os
from datetime import datetime

def generar_reporte_pdf(datos: dict, ruta_salida: str = "reporte_devsecops_liverpool.pdf") -> str:
    """
    Genera un archivo PDF con un formato estandarizado para reportar hallazgos de seguridad.
    
    :param datos: Diccionario con las métricas de seguridad a incluir.
    :param ruta_salida: Ruta relativa donde se guardará el PDF.
    :return: Ruta del archivo generado.
    """
    # V07: Validación estricta de entrada
    if not isinstance(datos, dict):
        raise TypeError("Los datos del reporte deben ser proporcionados como un diccionario.")
    
    # V03: Control de seguridad para evitar rutas absolutas riesgosas
    if os.path.isabs(ruta_salida):
        ruta_salida = os.path.basename(ruta_salida)
        
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        raise ImportError("La librería 'reportlab' es requerida para generar el PDF. Instálela con 'pip install reportlab'.")
        
    doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    story = []
    styles = getSampleStyleSheet()
    
    # Título Principal (Encabezado)
    titulo_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#002B49'), # Azul marino corporativo de Liverpool TI
        alignment=1 # Centrado
    )
    story.append(Paragraph("Reporte de Seguridad DevSecOps - Liverpool TI", titulo_style))
    story.append(Spacer(1, 12))
    
    # Subtítulo con Fecha
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    subtitulo_style = ParagraphStyle(
        name='SubTitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        alignment=1 # Centrado
    )
    story.append(Paragraph(f"Fecha de Generación: {fecha_actual}", subtitulo_style))
    story.append(Spacer(1, 24))
    
    # Cuerpo de texto introductorio
    cuerpo_style = ParagraphStyle(
        name='CuerpoStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#333333')
    )
    parrafo_intro = (
        "El presente documento detalla el estado actual de la auditoría de seguridad "
        "y DevSecOps aplicada al componente bajo evaluación. Las métricas que se presentan "
        "a continuación representan la postura de seguridad del software analizado, "
        "incluyendo hallazgos de herramientas SAST, análisis de vulnerabilidades y dependencias."
    )
    story.append(Paragraph(parrafo_intro, cuerpo_style))
    story.append(Spacer(1, 20))
    
    # Tabla de Datos (Métricas de seguridad)
    tabla_datos = [["Métrica de Seguridad", "Estado / Valor"]]
    for k, v in datos.items():
        tabla_datos.append([str(k), str(v)])
        
    t = Table(tabla_datos, colWidths=[250, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#002B49')),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (1,0), 8),
        ('TOPPADDING', (0,0), (1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F4F6F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F4F6F9')]),
    ]))
    story.append(t)
    
    # V08: Manejo seguro de excepciones en la escritura de disco
    try:
        doc.build(story)
    except Exception:
        raise IOError("Error al escribir el archivo de reporte PDF en disco.")
        
    # V09: Establecer permisos seguros del archivo (lectura/escritura solo para el dueño: 600)
    try:
        os.chmod(ruta_salida, 0o600)
    except OSError:
        pass
        
    return ruta_salida
