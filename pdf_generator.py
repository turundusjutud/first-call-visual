import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")
COLOR_DARK = HexColor("#052623")
COLOR_ORANGE = HexColor("#FF7F40")
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")
COLOR_GREY = HexColor("#555555")
COLOR_LIGHT_GREY = HexColor("#F2F2F2")

# --- ABIFUNKTSIOONID ---

def draw_header(c, width, height, logo_data, title, subtitle):
    """Joonistab standardse päise"""
    header_height = 110
    c.setFillColor(COLOR_DARK)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    
    # Logo
    if logo_data is not None:
        try:
            logo = ImageReader(logo_data)
            iw, ih = logo.getSize()
            aspect = ih / float(iw)
            logo_width = 110
            logo_height = logo_width * aspect
            logo_y = height - header_height + (header_height - logo_height) / 2
            c.drawImage(logo, 40, logo_y, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

    # Pealkiri
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 18)
    text_y_center = height - (header_height / 2) - 5
    c.drawRightString(width - 40, text_y_center + 10, title)
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, text_y_center - 10, subtitle)

def draw_footer(c, width):
    """Joonistab standardse jaluse"""
    footer_height = 60
    c.setFillColor(COLOR_DARK)
    c.rect(0, 0, width, footer_height, fill=1, stroke=0)
    
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 25, "reimo.arm@turundusjutud.ee  |  www.turundusjutud.ee  |  Turundusjutud OÜ")

# --- HINNASTUSE PDF LOOJA ---

def create_pricing_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Taust
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    draw_header(c, width, height, logo_file, "TEENUSTE HINNASTUS", "Läbipaistev ja tulemustele suunatud")

    # --- PÕHIPAKETT (RETAINER) ---
    start_y = height - 150
    
    c.setFillColor(COLOR_TEAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, start_y, "IGAKUINE HALDUSTEENUS (RETAINER)")
    
    # Suur kast
    c.setFillColor(COLOR_WHITE)
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(2)
    c.roundRect(50, start_y - 220, 495, 205, 10, fill=1, stroke=1)
    
    # Hind ja tingimus
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(80, start_y - 50, "1500€")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(190, start_y - 40, "/ kuu")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(80, start_y - 70, "(Arveldatakse kuu alguses ettemaksuna)")
    
    # Maht
    c.setFillColor(COLOR_TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, start_y - 50, "MAHT: 20 TUNDI")
    
    # Eraldusjoon
    c.setStrokeColor(HexColor("#EEEEEE"))
    c.line(80, start_y - 85, 515, start_y - 85)
    
    # Mis sisaldub (Vasak tulp)
    col1_x = 80
    list_y = start_y - 110
    
    items_included = [
        "Google, Meta & TikTok kampaaniate haldus",
        "Reklaamide seadistamine ja optimeerimine",
        "Eksperimentide läbiviimine (A/B testimine)",
        "Google Search reklaamtekstide copywriting",
        "Iganädalane monitooring",
        "Igakuine raport ja strateegiakõne"
    ]
    
    c.setFillColor(COLOR_TEAL)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col1_x, list_y + 10, "PAKETIS SISALDUB:")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    for item in items_included:
        c.drawString(col1_x, list_y - 5, f"•  {item}")
        list_y -= 18

    # --- LISA- JA PROJEKTIPÕHISED TEENUSED ---
    extra_y = start_y - 260
    
    c.setFillColor(COLOR_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, extra_y, "LISA- JA PROJEKTIPÕHISED TEENUSED")
    c.setFont("Helvetica", 10)
    c.drawString(50, extra_y - 15, "(Ei sisaldu igakuises haldustasus, arveldatakse kuu lõpus vastavalt kulule)")
    
    # Kast lisadele
    c.setFillColor(COLOR_LIGHT_GREY) 
    c.setStrokeColor(COLOR_GREY)
    c.setLineWidth(1)
    c.roundRect(50, extra_y - 180, 495, 150, 10, fill=1, stroke=1)
    
    # Lisa 1: Loovlahendused
    row1_y = extra_y - 60
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, row1_y, "LOOVLAHENDUSED (Creative)")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(80, row1_y - 15, "Pildid, videod, bännerid (Partner-tiim)")
    
    # HIND 1
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row1_y, "alates 70€ / tund")
    
    # Eraldusjoon
    c.setStrokeColor(HexColor("#DDDDDD"))
    c.line(80, row1_y - 30, 515, row1_y - 30)
    
    # Lisa 2: Tehniline seadistus
    row2_y = row1_y - 50
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, row2_y, "ANALÜÜTIKA & TRACKING")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(80, row2_y - 15, "GA4 server-side, GTM, Pixel seadistused")
    
    # HIND 2
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row2_y, "100 - 150€ / tund")
    
    # Lisa 3: Lisatunnid
    row3_y = row2_y - 50
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, row3_y, "LISAMAHT (>20h)")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(80, row3_y - 15, "Kui töömaht ületab paketis sisalduvat aega")
    
    # HIND 3
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row3_y, "kokkuleppel al. 100€ / tund")

    # --- TINGIMUSED ---
    terms_y = 110
    c.setFillColor(COLOR_TEAL)
    c.setStrokeColor(COLOR_TEAL)
    c.roundRect(50, terms_y, 495, 50, 5, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(70, terms_y + 32, "MAKSETINGIMUSED:")
    c.setFont("Helvetica", 9)
    c.drawString(70, terms_y + 18, "• Haldustasu (1500€) arve väljastatakse kuu alguses.")
    c.drawString(70, terms_y + 8, "• Lisatööd ja loovlahendused arveldatakse kuu lõpus tehtud töö alusel.")

    draw_footer(c, width)
    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.set_page_config(page_title="Turundusjutud Hinnastus", page_icon="💶")
st.title("💶 Hinnastuse Lehe Generaator")
st.write("Genereeri uuendatud hindadega teenuste hinnakiri.")

logo = st.file_uploader("Lae üles logo (PNG)", type=['png'])

if st.button("Loo Hinnakirja PDF"):
    pdf = create_pricing_pdf(logo)
    
    st.success("Hinnakiri valmis!")
    st.download_button(
        label="⬇️ Lae alla: Turundusjutud_Hinnastus.pdf",
        data=pdf,
        file_name="Turundusjutud_Hinnastus.pdf",
        mime="application/pdf"
    )
