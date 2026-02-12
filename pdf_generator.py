import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import textwrap

# --- BRÄNDI VÄRVID ---
COLOR_TEAL = HexColor("#1A776F")
COLOR_DARK = HexColor("#052623")
COLOR_ORANGE = HexColor("#FF7F40")
COLOR_BG = HexColor("#FAFAFA")
COLOR_WHITE = HexColor("#FFFFFF")
COLOR_TEXT = HexColor("#2E3A39")
COLOR_GREY = HexColor("#555555")

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

# --- 1. ONBOARDING VISUAALI GENEREERIMINE ---

def create_process_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1)

    draw_header(c, width, height, logo_file, "KOOSTÖÖ TEEKAART", "Ideest teostuseni: Kuidas me töötame")

    steps = [
        {
            "num": "1", "title": "ESMANE KONTAKT", "sub": "Sobivuse hindamine",
            "text": "Vastame päringule kiirelt. Eesmärk on välja selgitada, kas oleme potentsiaalselt sobivad partnerid, enne kui liigume süvitsi."
        },
        {
            "num": "2", "title": "AVASTUSKÕNE (DISCOVERY)", "sub": "Eesmärgid ja KPI-d",
            "text": "Kaardistame 3, 6 ja 12 kuu eesmärgid. Mis on töötanud, mis mitte? Lepime kokku mõõdikud (KPI-d), millega hindame edu."
        },
        {
            "num": "3", "title": "NDA JA AUDIT", "sub": "Turvaline ligipääs",
            "text": "Allkirjastame konfidentsiaalsuslepingu (NDA). Saame ligipääsud reklaamkontodele ja analüütikale, et teostada tehniline audit."
        },
        {
            "num": "4", "title": "STRATEEGIA JA PAKKUMINE", "sub": "Tegevuskava",
            "text": "Esitleme auditi tulemusi ja 3-6 kuu tegevusplaani. Kui strateegia ja lahendused sobivad, kinnitame hinnastuse ja liigume lepingusse."
        },
        {
            "num": "5", "title": "LEPING JA START", "sub": "Töö algus",
            "text": "Sõlmime lepingu (fikseeritud tasu või tunnipõhine). Arveldamine toimub ettemaksuna. Alustame seadistuste ja kampaaniatega."
        }
    ]

    current_y = height - 160
    line_x = 70
    
    # Ühendav joon
    c.setStrokeColor(COLOR_TEAL)
    c.setLineWidth(2)
    c.line(line_x, current_y, line_x, current_y - (len(steps)-1)*105)

    for step in steps:
        # Kast
        box_height = 85
        c.setFillColor(HexColor("#F7F9F9"))
        c.setStrokeColor(COLOR_TEAL)
        c.setLineWidth(1)
        c.roundRect(line_x + 30, current_y - box_height + 15, 420, box_height, 8, fill=1, stroke=1)

        # Number
        c.setFillColor(COLOR_TEAL)
        c.setStrokeColor(COLOR_BG)
        c.circle(line_x, current_y - 25, 15, fill=1, stroke=1)
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(line_x, current_y - 29, step['num'])

        # Tekst
        c.setFillColor(COLOR_TEAL)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(line_x + 50, current_y - 10, step['title'])
        
        c.setFillColor(COLOR_TEXT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(line_x + 50, current_y - 24, step['sub'])
        
        c.setFont("Helvetica", 9)
        wrapper = textwrap.TextWrapper(width=80)
        text_y = current_y - 40
        for line in wrapper.wrap(step['text']):
            c.drawString(line_x + 50, text_y, line)
            text_y -= 12

        current_y -= 105

    draw_footer(c, width)
    c.save()
    buffer.seek(0)
    return buffer

# --- 2. HINNASTUSE VISUAALI GENEREERIMINE ---

def create_pricing_pdf(logo_file):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
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
    c.setFillColor(HexColor("#F2F2F2")) # Hallikas taust
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
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row1_y, "100 - 150€ / tund")
    
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
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row2_y, "Projektipõhine / 150€ h")
    
    # Lisa 3: Lisatunnid
    row3_y = row2_y - 50
    c.setFillColor(COLOR_ORANGE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, row3_y, "LISAMAHT (>20h)")
    
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(80, row3_y - 15, "Kui töömaht ületab paketis sisalduvat aega")
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(515, row3_y, "150€ / tund")

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
st.set_page_config(page_title="Turundusjutud Dokumendid", page_icon="📄")
st.title("📄 Turundusjutud Dokumentide Generaator")

logo = st.file_uploader("Lae üles logo (PNG)", type=['png'])

# Valikukast: Mida soovid luua?
doc_type = st.radio(
    "Vali dokumendi tüüp:",
    ("Koostöö Teekaart (Onboarding)", "Hinnastuse Leht (Pricing)")
)

if st.button("Loo PDF"):
    if doc_type == "Koostöö Teekaart (Onboarding)":
        pdf = create_process_pdf(logo)
        filename = "Turundusjutud_Onboarding.pdf"
    else:
        pdf = create_pricing_pdf(logo)
        filename = "Turundusjutud_Hinnastus.pdf"
        
    st.success(f"{doc_type} valmis!")
    st.download_button(
        label="⬇️ Lae alla PDF",
        data=pdf,
        file_name=filename,
        mime="application/pdf"
    )
