import sqlite3
import os
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.units import cm

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def obtener_arbol(db_path, ave_uuid):
    conn = get_db_connection(db_path)
    query = """
    SELECT 
        hijo.uuid AS hijo_uuid, 
        hijo.anilla AS hijo_anilla,
        
        padre.uuid AS padre_uuid, 
        padre.anilla AS padre_anilla,
        
        madre.uuid AS madre_uuid, 
        madre.anilla AS madre_anilla,
        
        abuelo_paterno.uuid AS abuelo_paterno_uuid, 
        abuelo_paterno.anilla AS abuelo_paterno_anilla,
        
        abuela_paterna.uuid AS abuela_paterna_uuid, 
        abuela_paterna.anilla AS abuela_paterna_anilla,
        
        abuelo_materno.uuid AS abuelo_materno_uuid, 
        abuelo_materno.anilla AS abuelo_materno_anilla,
        
        abuela_materna.uuid AS abuela_materna_uuid, 
        abuela_materna.anilla AS abuela_materna_anilla
        
    FROM pajaros hijo 
    LEFT JOIN pajaros padre ON hijo.padre_uuid = padre.uuid 
    LEFT JOIN pajaros madre ON hijo.madre_uuid = madre.uuid 
    LEFT JOIN pajaros abuelo_paterno ON padre.padre_uuid = abuelo_paterno.uuid 
    LEFT JOIN pajaros abuela_paterna ON padre.madre_uuid = abuela_paterna.uuid 
    LEFT JOIN pajaros abuelo_materno ON madre.padre_uuid = abuelo_materno.uuid 
    LEFT JOIN pajaros abuela_materna ON madre.madre_uuid = abuela_materna.uuid 
    WHERE hijo.uuid = ?;
    """
    row = conn.execute(query, (ave_uuid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def obtener_detalles_ave(db_path, ave_uuid):
    conn = get_db_connection(db_path)
    # Basic info
    query = """
    SELECT p.*, e.nombre_comun as especie_nombre, v.nombre as variedad_nombre
    FROM pajaros p
    LEFT JOIN especies e ON (p.id_especie = e.id_especie OR p.id_especie = e.uuid)
    LEFT JOIN variedades v ON (p.variety_uuid = v.uuid OR p.variety_uuid = v.nombre)
    WHERE p.uuid = ?
    """
    ave = conn.execute(query, (ave_uuid,)).fetchone()
    if not ave:
        conn.close()
        return None
    
    ave = dict(ave)
    
    # Mutations (Joining with pajaros and mutaciones since bird_mutations uses IDs)
    mut_query = """
    SELECT m.nombre, bm.genotipo, bm.expresion 
    FROM bird_mutations bm 
    JOIN mutaciones m ON (bm.id_mutacion = m.uuid OR m.nombre = bm.id_mutacion)
    JOIN pajaros p ON bm.id_ave = p.id_ave
    WHERE p.uuid = ?
    """
    mutaciones = conn.execute(mut_query, (ave_uuid,)).fetchall()
    ave['mutaciones'] = [dict(m) for m in mutaciones]
    
    conn.close()
    return ave

def generar_qr(ave_uuid, output_path):
    # Dummy URL for now, can be configured
    url = f"https://aviario.app/bird/{ave_uuid}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

def generar_certificado_pdf(ave, arbol, output_path, qr_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=1, fontSize=24, spaceAfter=20, textColor=colors.darkblue)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], fontSize=16, spaceAfter=10, textColor=colors.darkblue)
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph("CERTIFICADO GENEALÓGICO", title_style))
    elements.append(Spacer(1, 12))
    
    # Main Info & Photo Table
    photo_part = "🐦"
    if ave.get('foto_path') and os.path.exists(ave.get('foto_path')):
        try:
            img = RLImage(ave['foto_path'], 4*cm, 4*cm)
            photo_part = img
        except:
            photo_part = "🐦"
    
    info_data = [
        [Paragraph(f"<b>Anilla:</b> {ave.get('anilla') or 'S/A'}", normal_style), photo_part],
        [Paragraph(f"<b>Especie:</b> {ave.get('especie_nombre') or 'N/A'}", normal_style), ""],
        [Paragraph(f"<b>Variedad:</b> {ave.get('variedad_nombre') or 'N/A'}", normal_style), ""],
        [Paragraph(f"<b>Fecha Nac.:</b> {ave.get('fecha_nacimiento') or 'N/A'}", normal_style), ""],
    ]
    
    info_table = Table(info_data, colWidths=[10*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('SPAN', (1, 0), (1, 3)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Mutations
    elements.append(Paragraph("Genética y Mutaciones", header_style))
    if ave.get('mutaciones'):
        mut_list = []
        for m in ave['mutaciones']:
            line = f"{m['nombre']} ({m['genotipo'] or 'Visual'})"
            mut_list.append(Paragraph(f"• {line}", normal_style))
        for item in mut_list:
            elements.append(item)
    else:
        elements.append(Paragraph("Sin mutaciones registradas.", normal_style))
    elements.append(Spacer(1, 20))
    
    # Genealogy Tree Table
    # Genealogy Tree Table
    elements.append(Paragraph("Árbol Genealógico", header_style))
    
    # Standard Pedigree Format: Bird (Left) -> Parents (Middle) -> Grandparents (Right)
    tree_data = [
        ["Ave", "Padres", "Abuelos"],
        [ave.get('anilla') or 'S/A', arbol.get('padre_anilla') or 'S/A', arbol.get('abuelo_paterno_anilla') or 'S/A'],
        ["",                          "",                              arbol.get('abuela_paterna_anilla') or 'S/A'],
        ["",                          arbol.get('madre_anilla') or 'S/A', arbol.get('abuelo_materno_anilla') or 'S/A'],
        ["",                          "",                              arbol.get('abuela_materna_anilla') or 'S/A'],
    ]
    
    tree_table = Table(tree_data, colWidths=[5*cm, 5*cm, 5*cm], rowHeights=[1*cm]*5)
    tree_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        
        # Merge Ave (Column 0, Rows 1-4)
        ('SPAN', (0, 1), (0, 4)),
        
        # Merge Padre (Column 1, Rows 1-2)
        ('SPAN', (1, 1), (1, 2)),
        
        # Merge Madre (Column 1, Rows 3-4)
        ('SPAN', (1, 3), (1, 4)),
    ]))
    elements.append(tree_table)
    elements.append(Spacer(1, 30))
    
    # QR Code
    if os.path.exists(qr_path):
        qr_img = RLImage(qr_path, 3*cm, 3*cm)
        elements.append(qr_img)
        elements.append(Paragraph("Escanea para ver más detalles", ParagraphStyle('QRNote', fontSize=8, alignment=1)))
    
    doc.build(elements)
