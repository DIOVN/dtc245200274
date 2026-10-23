"""
Script: generate_report_docx.py
Mục đích: Tự động sinh Báo cáo Kỹ thuật Triển khai & Vận hành Hệ thống Quản lý Khách sạn
Tiêu chuẩn: Nghị định 30/2020/NĐ-CP & Quy chuẩn Đồ án / Bài tập lớn Đại học CNTT (ICTU)
Tác giả: Phùng Thiên Trường (MSSV: DTC245200274) - Lớp CNTT K24
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

NAVY = RGBColor(0x0F, 0x25, 0x40)      # #0F2540 - Primary Academic Navy
TEXT_COLOR = RGBColor(0x1F, 0x29, 0x37) # #1F2937 - Body Text Charcoal
GRAY_TEXT = RGBColor(0x4B, 0x55, 0x63)  # #4B5563
CODE_COLOR = RGBColor(0x0F, 0x17, 0x2A) # #0F172A

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), fill_hex))
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        r'<w:tcMar %s>'
        r'  <w:top w:w="%d" w:type="dxa"/>'
        r'  <w:bottom w:w="%d" w:type="dxa"/>'
        r'  <w:left w:w="%d" w:type="dxa"/>'
        r'  <w:right w:w="%d" w:type="dxa"/>'
        r'</w:tcMar>' % (nsdecls('w'), top, bottom, left, right)
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        r'<w:tblBorders %s>'
        r'  <w:top w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'  <w:left w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'  <w:bottom w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'  <w:right w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'  <w:insideH w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'  <w:insideV w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>'
        r'</w:tblBorders>' % (nsdecls('w'), val, sz, color, val, sz, color, val, sz, color, val, sz, color, val, sz, color, val, sz, color)
    )
    tblPr.append(borders)

def add_cover_page_border(sec):
    sectPr = sec._sectPr
    cols = sectPr.find(qn('w:cols'))
    pgBorders = parse_xml(
        r'<w:pgBorders %s w:offsetFrom="page">'
        r'  <w:top w:val="double" w:sz="18" w:space="24" w:color="0F2540"/>'
        r'  <w:left w:val="double" w:sz="18" w:space="24" w:color="0F2540"/>'
        r'  <w:bottom w:val="double" w:sz="18" w:space="24" w:color="0F2540"/>'
        r'  <w:right w:val="double" w:sz="18" w:space="24" w:color="0F2540"/>'
        r'</w:pgBorders>' % nsdecls('w')
    )
    if cols is not None:
        cols.addprevious(pgBorders)
    else:
        sectPr.append(pgBorders)

def set_section_page_numbering(sec, num_format="decimal", start_at=None):
    sectPr = sec._sectPr
    cols = sectPr.find(qn('w:cols'))
    pgPr = sectPr.find(qn('w:pgNumType'))
    if pgPr is None:
        pgPr = OxmlElement('w:pgNumType')
        if cols is not None:
            cols.addprevious(pgPr)
        else:
            sectPr.append(pgPr)
    pgPr.set(qn('w:fmt'), num_format)
    if start_at is not None:
        pgPr.set(qn('w:start'), str(start_at))

def add_footer_page_number(sec):
    footer = sec.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.text = ""
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % nsdecls('w'))
    p._p.append(fld)

def add_heading_1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph(style='Heading 3')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    return p

def add_clean_paragraph(doc, text, is_bullet=False, italic=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(0)
    
    if is_bullet:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        run = p.add_run("•  " + text)
    else:
        if len(text) > 120:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(1.27)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(1.27)
        run = p.add_run(text)
        
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.color.rgb = TEXT_COLOR
    run.font.italic = italic
    run.font.bold = bold
    return p

def add_table_caption(doc, prefix="Bảng", title=""):
    p = doc.add_paragraph(style='Caption')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    
    r_pre = p.add_run(f"{prefix} ")
    r_pre.font.name = "Times New Roman"
    r_pre.font.size = Pt(11)
    r_pre.font.bold = True
    r_pre.font.italic = True
    
    fld = parse_xml(r'<w:fldSimple %s w:instr="SEQ %s \* ARABIC"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="22"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % (nsdecls('w'), prefix))
    p._p.append(fld)
    
    r_title = p.add_run(f": {title}")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)
    r_title.font.italic = True
    return p

def add_figure_caption(doc, prefix="Hình", title=""):
    p = doc.add_paragraph(style='Caption')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    
    r_pre = p.add_run(f"{prefix} ")
    r_pre.font.name = "Times New Roman"
    r_pre.font.size = Pt(11)
    r_pre.font.bold = True
    r_pre.font.italic = True
    
    fld = parse_xml(r'<w:fldSimple %s w:instr="SEQ %s \* ARABIC"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:i/><w:sz w:val="22"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>' % (nsdecls('w'), prefix))
    p._p.append(fld)
    
    r_title = p.add_run(f": {title}")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)
    r_title.font.italic = True
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        r'<w:tcBorders %s>'
        r'  <w:top w:val="none"/>'
        r'  <w:left w:val="single" w:sz="24" w:space="0" w:color="0F2540"/>'
        r'  <w:bottom w:val="none"/>'
        r'  <w:right w:val="none"/>'
        r'</w:tcBorders>' % nsdecls('w')
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    lines = code_text.strip().split('\n')
    for idx, line in enumerate(lines):
        r = p.add_run(line)
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = CODE_COLOR
        if idx < len(lines) - 1:
            p.add_run("\n")
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_toc_line(doc, title, page_str, level=1, is_bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    if level == 2:
        p.paragraph_format.left_indent = Cm(0.6)
    elif level == 3:
        p.paragraph_format.left_indent = Cm(1.2)
        
    pPr = p._p.get_or_add_pPr()
    tabs = parse_xml(r'<w:tabs %s><w:tab w:val="right" w:leader="dot" w:pos="9355"/></w:tabs>' % nsdecls('w'))
    pPr.append(tabs)
    
    r_title = p.add_run(title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(12)
    r_title.font.bold = is_bold
    r_title.font.color.rgb = NAVY if level == 1 and is_bold else TEXT_COLOR
    
    r_tab = p.add_run()
    r_tab._r.append(parse_xml(r'<w:tab %s/>' % nsdecls('w')))
    
    r_page = p.add_run(page_str)
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(12)
    r_page.font.bold = is_bold
    r_page.font.color.rgb = NAVY if level == 1 and is_bold else TEXT_COLOR
    return p

def add_table_of_contents_field(doc, title="MỤC LỤC"):
    h = doc.add_paragraph()
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run(title)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(12)

    p_begin = doc.add_paragraph()
    p_begin.paragraph_format.line_spacing = 1.15
    p_begin.paragraph_format.space_after = Pt(0)
    p_begin.paragraph_format.space_before = Pt(0)

    r_begin = p_begin.add_run()
    r_begin._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    r_instr = p_begin.add_run()
    r_instr._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w')))
    r_sep = p_begin.add_run()
    r_sep._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))

    toc_items = [
        ("LỜI CAM ĐOAN", 1, "ii", True),
        ("DANH MỤC BẢNG BIỂU", 1, "iv", True),
        ("DANH MỤC HÌNH ẢNH", 1, "v", True),
        ("DANH MỤC TỪ VIẾT TẮT", 1, "vi", True),
        ("CHƯƠNG 1: TỔNG QUAN HỆ THỐNG VÀ KIẾN TRÚC TỔNG THỂ", 1, "1", True),
        ("1.1. Bối cảnh đề tài và Mục tiêu triển khai", 2, "1", False),
        ("1.2. Kiến trúc giải pháp tổng thể trên nền tảng Docker Container", 2, "2", False),
        ("1.3. Bảng ma trận các dịch vụ và phân bổ tài nguyên mạng", 2, "3", False),
        ("1.4. Sơ đồ kiến trúc Container và luồng dữ liệu", 2, "5", False),
        ("CHƯƠNG 2: THIẾT KẾ CƠ SỞ DỮ LIỆU VÀ QUY TRÌNH NGHIỆP VỤ CỐT LÕI", 1, "6", True),
        ("2.1. Thiết kế Schema cơ sở dữ liệu quan hệ PostgreSQL 16 (Chuẩn hóa 3NF)", 2, "6", False),
        ("2.2. Sơ đồ thực thể liên kết dữ liệu (ERD)", 2, "9", False),
        ("2.3. Thuật toán chống trùng lịch (Anti-Overbooking) bằng Pessimistic Locking", 2, "10", False),
        ("2.4. Quy trình xác thực phân quyền quản trị (JWT & Bcrypt Security)", 2, "11", False),
        ("2.5. Tích hợp cổng thanh toán trực tuyến tự động (VietQR & Webhook IPN)", 2, "13", False),
        ("2.6. Sơ đồ tuần tự nghiệp vụ đặt phòng và thanh toán", 2, "15", False),
        ("CHƯƠNG 3: TRIỂN KHAI THỰC TẾ, CẤU HÌNH BẢO MẬT VÀ REVERSE PROXY", 1, "16", True),
        ("3.1. Thiết lập biến môi trường bảo mật (.env) và nguyên tắc loại trừ", 2, "16", False),
        ("3.2. Cấu hình Nginx Reverse Proxy, Điều hướng /api/ và Tối ưu hóa Bộ đệm", 2, "17", False),
        ("3.3. Cơ chế phân giải dịch vụ mạng nội bộ Docker (Service Discovery)", 2, "19", False),
        ("3.4. Hệ sinh thái Giám sát Prometheus, Grafana và Thu thập Log tập trung Loki", 2, "21", False),
        ("CHƯƠNG 4: KIỂM THỬ HỆ THỐNG, ĐÁNH GIÁ VÀ HƯỚNG DẪN VẬN HÀNH", 1, "23", True),
        ("4.1. Kịch bản kiểm thử API Health Check và tính toàn vẹn CSDL", 2, "23", False),
        ("4.2. Kiểm thử tải đồng thời chống xung đột đặt phòng (Concurrency Test)", 2, "25", False),
        ("4.3. Kiểm thử thu thập Time-series Metrics và truy vấn LogQL", 2, "27", False),
        ("4.4. Quy trình khởi chạy, sao lưu dữ liệu và phục hồi sự cố (Disaster Recovery)", 2, "29", False),
        ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 1, "31", True),
        ("1. Kết quả đạt được", 2, "31", False),
        ("2. Hạn chế tồn đọng", 2, "31", False),
        ("3. Hướng phát triển nâng cấp", 2, "32", False),
        ("TÀI LIỆU THAM KHẢO", 1, "33", True)
    ]

    for title_text, level, page_str, is_bold in toc_items:
        add_toc_line(doc, title_text, page_str, level=level, is_bold=is_bold)

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(4)
    r_end = p_end.add_run()
    r_end._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

def add_list_of_captions_field(doc, title, seq_label):
    h = doc.add_paragraph(style='Heading 1')
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run(title)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(12)

    p_begin = doc.add_paragraph()
    p_begin.paragraph_format.line_spacing = 1.15
    p_begin.paragraph_format.space_after = Pt(0)
    p_begin.paragraph_format.space_before = Pt(0)

    r_begin = p_begin.add_run()
    r_begin._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    r_instr = p_begin.add_run()
    r_instr._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \c "%s" \h \z </w:instrText>' % (nsdecls('w'), seq_label)))
    r_sep = p_begin.add_run()
    r_sep._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))

    if seq_label == "Bảng":
        lot_items = [
            ("Bảng 1: Ma trận phân bổ dịch vụ, cổng mạng và tài nguyên hệ thống", "3"),
            ("Bảng 2: Cấu trúc từ điển dữ liệu các bảng cơ sở dữ liệu hotel_db", "7"),
            ("Bảng 3: Ma trận phân quyền các endpoint API trong hệ thống", "12"),
            ("Bảng 4: Bảng ánh xạ cổng dịch vụ truy cập môi trường Localhost", "18"),
            ("Bảng 5: Kết quả kiểm thử tải đồng thời thuật toán Anti-Overbooking", "26")
        ]
        for cap_text, page_str in lot_items:
            add_toc_line(doc, cap_text, page_str, level=1, is_bold=False)
    elif seq_label == "Hình":
        lof_items = [
            ("Hình 1: Sơ đồ kiến trúc hệ thống tổng thể và phân bổ container Docker", "5"),
            ("Hình 2: Sơ đồ thực thể liên kết dữ liệu (Entity-Relationship Diagram - ERD)", "9"),
            ("Hình 3: Sơ đồ tuần tự quy trình đặt phòng và khóa bi quan (Pessimistic Locking)", "15"),
            ("Hình 4: Giao diện Cổng khách hàng đặt phòng trực tuyến trên Localhost", "24"),
            ("Hình 5: Bảng điều khiển Quản trị PMS theo dõi sơ đồ phòng và công suất buồng", "25"),
            ("Hình 6: Bảng điều khiển Grafana giám sát tài nguyên máy chủ và hiệu năng dịch vụ", "28"),
            ("Hình 7: Nhật ký và trạng thái các Endpoints giám sát qua Prometheus", "29")
        ]
        for cap_text, page_str in lof_items:
            add_toc_line(doc, cap_text, page_str, level=1, is_bold=False)

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(4)
    r_end = p_end.add_run()
    r_end._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))


def build_report():
    print("Khởi tạo Document...")
    doc = Document()

    # 1. Page Setup A4
    sec1 = doc.sections[0]
    sec1.page_width = Cm(21.0)
    sec1.page_height = Cm(29.7)
    sec1.top_margin = Cm(2.0)
    sec1.bottom_margin = Cm(2.0)
    sec1.left_margin = Cm(3.0)
    sec1.right_margin = Cm(1.5)

    # Cài đặt Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = TEXT_COLOR
    style_normal.paragraph_format.line_spacing = 1.4
    style_normal.paragraph_format.space_after = Pt(4)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Cài đặt Heading 1 Style
    h1_style = doc.styles['Heading 1']
    h1_style.font.name = 'Times New Roman'
    h1_style.font.size = Pt(16)
    h1_style.font.bold = True
    h1_style.font.color.rgb = NAVY
    h1_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1_style.paragraph_format.space_before = Pt(14)
    h1_style.paragraph_format.space_after = Pt(8)
    h1_style.paragraph_format.keep_with_next = True

    # Cài đặt Heading 2 Style
    h2_style = doc.styles['Heading 2']
    h2_style.font.name = 'Times New Roman'
    h2_style.font.size = Pt(14)
    h2_style.font.bold = True
    h2_style.font.color.rgb = NAVY
    h2_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h2_style.paragraph_format.space_before = Pt(10)
    h2_style.paragraph_format.space_after = Pt(4)
    h2_style.paragraph_format.keep_with_next = True

    # Cài đặt Heading 3 Style
    h3_style = doc.styles['Heading 3']
    h3_style.font.name = 'Times New Roman'
    h3_style.font.size = Pt(13)
    h3_style.font.bold = True
    h3_style.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    h3_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h3_style.paragraph_format.space_before = Pt(6)
    h3_style.paragraph_format.space_after = Pt(3)
    h3_style.paragraph_format.keep_with_next = True

    # Cài đặt Caption Style
    cap_style = doc.styles['Caption']
    cap_style.font.name = 'Times New Roman'
    cap_style.font.size = Pt(11)
    cap_style.font.italic = True
    cap_style.font.color.rgb = TEXT_COLOR

    # Add compat properly in schema order
    settings = doc.settings._element
    compat = settings.find(qn('w:compat'))
    if compat is not None:
        compat.append(parse_xml(r'<w:doNotExpandShiftReturn %s/>' % nsdecls('w')))
        compat.append(parse_xml(r'<w:balanceSingleByteDoubleByteWidth %s/>' % nsdecls('w')))

    # Art Border Trang Bìa
    add_cover_page_border(sec1)
    sec1.footer.is_linked_to_previous = False

    # =========================================================================
    # SECTION 1: TRANG BÌA CHÍNH
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = False
    r.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = NAVY

    # Decorative Star Separator
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(36)
    r = p.add_run("✦ ✦ ✦ ✦ ✦")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0xD9, 0x77, 0x06)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("BÁO CÁO BÀI TẬP LỚN / ĐỒ ÁN MÔN HỌC")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(48)
    r = p.add_run("TRIỂN KHAI VÀ VẬN HÀNH HỆ THỐNG QUẢN LÝ ĐẶT PHÒNG KHÁCH SẠN TRÊN NỀN TẢNG DOCKER, CSDL POSTGRESQL VÀ OBSERVABILITY STACK")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = NAVY

    # Metadata Table
    table_meta = doc.add_table(rows=7, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False
    
    col_widths = [Cm(6.0), Cm(9.5)]
    for row in table_meta.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    meta_data = [
        ("Học phần:", "Triển khai & Quản trị Hệ thống Phần mềm"),
        ("Mã đề tài:", "Đề tài số 06 - Enterprise Hotel Booking System"),
        ("Giảng viên hướng dẫn:", "ThS. Nguyễn Anh Chuyên"),
        ("Sinh viên thực hiện:", "Phùng Thiên Trường"),
        ("Mã số sinh viên (MSSV):", "DTC245200274"),
        ("Lớp / Khóa:", "Công nghệ Thông tin - K24"),
        ("Môi trường triển khai:", "Localhost / Docker Desktop Platform")
    ]

    for idx, (lbl, val) in enumerate(meta_data):
        c0 = table_meta.cell(idx, 0)
        c1 = table_meta.cell(idx, 1)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.line_spacing = 1.2
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(13)
        r0.font.italic = True
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.line_spacing = 1.2
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = NAVY

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(64)
    r = p.add_run("Thái Nguyên, Năm 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.italic = True
    r.font.color.rgb = GRAY_TEXT

    # =========================================================================
    # SECTION 2: DANH MỤC ĐẦU BÀI (Số trang La Mã i, ii, iii...)
    # =========================================================================
    sec2 = doc.add_section()
    sec2.top_margin = Cm(2.0)
    sec2.bottom_margin = Cm(2.0)
    sec2.left_margin = Cm(3.0)
    sec2.right_margin = Cm(1.5)
    set_section_page_numbering(sec2, num_format="lowerRoman", start_at=1)
    add_footer_page_number(sec2)

    # 1. LỜI CAM ĐOAN
    add_heading_1(doc, "LỜI CAM ĐOAN")
    add_clean_paragraph(doc, "Tôi xin cam đoan báo cáo kỹ thuật \"Triển khai và Vận hành Hệ thống Quản lý Đặt phòng Khách sạn trên Nền tảng Docker, CSDL PostgreSQL và Observability Stack\" là công trình nghiên cứu, thiết kế, triển khai và kiểm thử thực tế do chính tôi thực hiện dưới sự định hướng chuyên môn tận tình của giảng viên hướng dẫn ThS. Nguyễn Anh Chuyên.")
    add_clean_paragraph(doc, "Toàn bộ các số liệu kiểm thử hiệu năng, cấu hình container, bảng chỉ mục cơ sở dữ liệu, các câu truy vấn LogQL và mã nguồn cấu hình hệ thống được trình bày trong báo cáo đều trung thực, minh bạch, được trích xuất trực tiếp từ môi trường triển khai thực tế trên máy trạm của sinh viên thực hiện.")
    add_clean_paragraph(doc, "Tôi hoàn toàn chịu trách nhiệm trước Nhà trường và Khoa Công nghệ Thông tin về tính độc lập và liêm chính học thuật của tài liệu này.")

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(28)
    p_sig.paragraph_format.space_after = Pt(2)
    r = p_sig.add_run("Thái Nguyên, ngày 25 tháng 10 năm 2026\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.italic = True
    r_role = p_sig.add_run("Sinh viên thực hiện\n\n\n\n")
    r_role.font.name = "Times New Roman"
    r_role.font.size = Pt(13)
    r_role.font.italic = True
    r_name = p_sig.add_run("Phùng Thiên Trường\n")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(13)
    r_name.font.bold = True
    r_mssv = p_sig.add_run("(MSSV: DTC245200274)")
    r_mssv.font.name = "Times New Roman"
    r_mssv.font.size = Pt(12)
    r_mssv.font.italic = True

    doc.add_page_break()

    # 2. MỤC LỤC TỰ ĐỘNG
    add_table_of_contents_field(doc, "MỤC LỤC")
    doc.add_page_break()

    # 3. DANH MỤC BẢNG BIỂU
    add_list_of_captions_field(doc, "DANH MỤC BẢNG BIỂU", "Bảng")
    doc.add_page_break()

    # 4. DANH MỤC HÌNH ẢNH
    add_list_of_captions_field(doc, "DANH MỤC HÌNH ẢNH", "Hình")
    doc.add_page_break()

    # 5. DANH MỤC TỪ VIẾT TẮT
    add_heading_1(doc, "DANH MỤC TỪ VIẾT TẮT")
    
    abbr_data = [
        ("API", "Application Programming Interface", "Giao diện lập trình ứng dụng kết nối Client - Server"),
        ("REST", "Representational State Transfer", "Kiến trúc giao tiếp định hướng tài nguyên chuẩn web"),
        ("ACID", "Atomicity, Consistency, Isolation, Durability", "Bốn thuộc tính tin cậy cốt lõi của giao dịch CSDL"),
        ("3NF", "Third Normal Form", "Dạng chuẩn 3 trong thiết kế cơ sở dữ liệu quan hệ"),
        ("RPS", "Requests Per Second", "Tần suất xử lý yêu cầu HTTP trên mỗi giây"),
        ("JWT", "JSON Web Token", "Chuẩn mã hóa thông tin xác thực phiên làm việc an toàn"),
        ("IPN", "Instant Payment Notification", "Cơ chế Webhook gọi lại khi thanh toán thành công"),
        ("RED", "Rate, Errors, Duration", "Mô hình giám sát hiệu năng dịch vụ web backend"),
        ("USE", "Utilization, Saturation, Errors", "Mô hình giám sát tài nguyên phần cứng máy chủ"),
        ("SPA", "Single Page Application", "Ứng dụng web trang đơn tải động mượt mà"),
        ("PMS", "Property Management System", "Hệ thống quản trị buồng phòng và nghiệp vụ khách sạn"),
        ("LogQL", "Log Query Language", "Ngôn ngữ truy vấn nhật ký của hệ sinh thái Grafana Loki")
    ]

    tbl_abbr = doc.add_table(rows=len(abbr_data) + 1, cols=3)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_abbr.autofit = False
    set_table_borders(tbl_abbr)

    abbr_widths = [Cm(2.5), Cm(6.5), Cm(7.5)]
    for r in tbl_abbr.rows:
        for i, w in enumerate(abbr_widths):
            r.cells[i].width = w

    headers_abbr = ["Từ viết tắt", "Thuật ngữ tiếng Anh", "Giải nghĩa kỹ thuật"]
    for i, h in enumerate(headers_abbr):
        cell = tbl_abbr.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (c0, c1, c2) in enumerate(abbr_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate([c0, c1, c2]):
            cell = tbl_abbr.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY

    # =========================================================================
    # SECTION 3: THÂN BÀI CHÍNH (Đánh số trang Ả Rập 1, 2, 3...)
    # =========================================================================
    sec3 = doc.add_section()
    sec3.top_margin = Cm(2.0)
    sec3.bottom_margin = Cm(2.0)
    sec3.left_margin = Cm(3.0)
    sec3.right_margin = Cm(1.5)
    set_section_page_numbering(sec3, num_format="decimal", start_at=1)
    add_footer_page_number(sec3)

    # -------------------------------------------------------------------------
    # CHƯƠNG 1
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 1: TỔNG QUAN HỆ THỐNG VÀ KIẾN TRÚC TỔNG THỂ")

    add_heading_2(doc, "1.1. Bối cảnh đề tài và Mục tiêu triển khai")
    add_clean_paragraph(doc, "Trong kỷ nguyên chuyển đổi số ngành du lịch - khách sạn, việc triển khai một hệ thống quản lý và đặt phòng khách sạn (Hotel Booking & Property Management System - PMS) đòi hỏi sự kết hợp chặt chẽ giữa khả năng phản hồi thời gian thực, độ tin cậy giao dịch tuyệt đối (ACID) và khả năng quan sát hệ thống (Observability). Đối với khách hàng, hệ thống phải cung cấp giao diện trực quan, tra cứu phòng trống theo khoảng thời gian linh hoạt, cấp mã đặt phòng tự động và hỗ trợ thanh toán mã QR chuẩn quốc gia. Đối với ban quản trị, hệ thống đòi hỏi sơ đồ ma trận phòng phân tầng, tỷ lệ lấp đầy buồng phòng (Occupancy Rate) tức thời, quản lý quy trình Check-in/Check-out chặt chẽ.")
    add_clean_paragraph(doc, "Các mục tiêu kỹ thuật cốt lõi được đặt ra cho đồ án:")
    add_clean_paragraph(doc, "Đóng gói toàn diện bằng Docker Container (Full Containerization): Tách biệt hoàn toàn các phân hệ thành các container chuyên trách, chạy độc lập nhưng liên thông thông qua mạng ảo nội bộ Docker bridge.", is_bullet=True)
    add_clean_paragraph(doc, "Giải quyết triệt để tranh chấp đặt phòng (Anti-Overbooking Algorithm): Xây dựng thuật toán xử lý tranh chấp giao dịch ở mức cơ sở dữ liệu bằng cơ chế khóa bi quan (Pessimistic Locking), đảm bảo tuyệt đối không có hai khách hàng đặt trùng cùng một phòng trong cùng một khung thời gian.", is_bullet=True)
    add_clean_paragraph(doc, "Tối ưu hóa vận hành trên Localhost: Hệ thống được cấu hình tinh gọn để có thể khởi chạy và hoạt động trơn tru trên máy tính cá nhân thông qua Docker Desktop mà không phụ thuộc vào hạ tầng đám mây công cộng.", is_bullet=True)
    add_clean_paragraph(doc, "Thiết lập cụm quan sát toàn diện (Observability Stack): Tích hợp Prometheus để cào số liệu RED Metrics, Grafana để trực quan hóa bảng điều khiển và Loki + Promtail để thu thập nhật ký container tập trung.", is_bullet=True)

    add_heading_2(doc, "1.2. Kiến trúc giải pháp tổng thể trên nền tảng Docker Container")
    add_clean_paragraph(doc, "Hệ thống được thiết kế theo mô hình kiến trúc phân lớp hướng dịch vụ (Service-Oriented Architecture), bao gồm 7 phân hệ chính hoạt động độc lập dưới dạng các container Docker:")
    add_clean_paragraph(doc, "Phân hệ Giao diện Người dùng (hotel-frontend): Xây dựng bằng React 18, Vite và Tailwind CSS. Container sử dụng máy chủ Nginx Alpine chuyên dụng để phân phối mã tĩnh (HTML/CSS/JS) và đóng vai trò proxy chuyển tiếp các yêu cầu /api/ về Backend container.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Xử lý Nghiệp vụ Backend (hotel-backend): Xây dựng trên nền tảng Node.js (Express framework), tuân thủ kiến trúc Controller - Service - Repository. Phân hệ cung cấp các REST API cho tra cứu phòng, đặt phòng, xác thực JWT, thanh toán SePay và xuất số liệu giám sát tại endpoint /metrics.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Cơ sở Dữ liệu Quan hệ (hotel-postgres): Sử dụng PostgreSQL phiên bản 16-alpine. Dữ liệu được lưu trữ an toàn trên Docker Volume riêng biệt (hotel_pgdata), hỗ trợ giao dịch ACID, khóa bi quan và tự động kích hoạt nạp Schema + Seed data thông qua entrypoint /docker-entrypoint-initdb.d/.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Giám sát Số liệu (hotel-prometheus): Máy chủ Time-series database định kỳ cào (scrape) các chỉ số RED từ /metrics của Backend và số liệu tài nguyên từ Node-Exporter.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Trực quan hóa Bảng điều khiển (hotel-grafana): Cung cấp dashboard trực quan thời gian thực, tự động nạp nguồn dữ liệu (Datasources) và bảng điều khiển (Dashboards) khi khởi động.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Quản lý Nhật ký Tập trung (hotel-loki): Lưu trữ và đánh chỉ mục metadata của logs, cho phép truy vấn nhật ký theo cú pháp LogQL hiệu năng cao.", is_bullet=True)
    add_clean_paragraph(doc, "Phân hệ Đại lý Thu thập Log (hotel-promtail): Gắn kết trực tiếp vào Docker socket (/var/run/docker.sock) của máy trạm để đọc live stream logs từ tất cả các container và đẩy về Loki.", is_bullet=True)

    add_heading_2(doc, "1.3. Bảng ma trận các dịch vụ và phân bổ tài nguyên mạng")
    add_clean_paragraph(doc, "Toàn bộ các container được liên kết thông qua mạng bridge nội bộ mang tên hotel_internal, đồng thời kết nối vào mạng liên thông novera_network. Các cổng truy cập từ phía máy trạm (Host Port) được thiết lập chặt chẽ nhằm tránh xung đột dịch vụ.")

    # BẢNG 1
    add_table_caption(doc, prefix="Bảng", title="Ma trận phân bổ dịch vụ, cổng mạng và tài nguyên hệ thống")
    
    b1_data = [
        ("Frontend Web", "hotel-frontend", "hotel-booking-frontend", "80/tcp", "127.0.0.1:3001", "Giao diện khách đặt phòng & Admin PMS"),
        ("Backend API", "hotel-backend", "hotel-booking-backend", "5000/tcp", "127.0.0.1:5000", "REST API, Business Logic, /metrics"),
        ("Database", "hotel-postgres", "postgres:16-alpine", "5432/tcp", "127.0.0.1:5432", "CSDL quan hệ hotel_db, ACID, 3NF"),
        ("Prometheus", "hotel-prometheus", "prom/prometheus:v2.51.2", "9090/tcp", "127.0.0.1:9090", "Thu thập time-series metrics định kỳ 5s"),
        ("Grafana", "hotel-grafana", "grafana/grafana:10.4.2", "3000/tcp", "127.0.0.1:3000", "Bảng điều khiển KPI & Observability"),
        ("Loki", "hotel-loki", "grafana/loki:2.9.8", "3100/tcp", "127.0.0.1:3100", "Lưu trữ và đánh chỉ mục nhật ký tập trung"),
        ("Promtail", "hotel-promtail", "grafana/promtail:2.9.8", "-", "Không mở", "Đọc container socket đẩy log về Loki"),
        ("Node Exporter", "hotel-node-exporter", "prom/node-exporter:v1.8.1", "9100/tcp", "127.0.0.1:9100", "Thu thập chỉ số phần cứng máy chủ")
    ]

    tbl_b1 = doc.add_table(rows=len(b1_data) + 1, cols=6)
    tbl_b1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b1.autofit = False
    set_table_borders(tbl_b1)

    b1_widths = [Cm(2.6), Cm(2.8), Cm(3.2), Cm(1.8), Cm(2.5), Cm(3.6)]
    for r in tbl_b1.rows:
        for i, w in enumerate(b1_widths):
            r.cells[i].width = w

    headers_b1 = ["Dịch Vụ", "Container", "Docker Image", "Cổng Cont.", "Cổng Host", "Vai Trò & Chức Năng"]
    for i, h in enumerate(headers_b1):
        cell = tbl_b1.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, row_vals in enumerate(b1_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_vals):
            cell = tbl_b1.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True

    add_heading_2(doc, "1.4. Sơ đồ kiến trúc Container và luồng dữ liệu")
    add_clean_paragraph(doc, "Sơ đồ kiến trúc thể hiện toàn bộ các tầng ứng dụng từ trình duyệt người dùng qua tầng phân phối Nginx, xử lý nghiệp vụ tại Node.js Express, lưu trữ bền vững tại PostgreSQL và được bao bọc bởi cụm quan sát Observability Stack.")

    # Hình 1
    img1_path = "docs/images/hinh1_kientruc_hethong.png"
    if os.path.exists(img1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img1_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Sơ đồ kiến trúc hệ thống tổng thể và phân bổ container Docker")

    # -------------------------------------------------------------------------
    # CHƯƠNG 2
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 2: THIẾT KẾ CƠ SỞ DỮ LIỆU VÀ QUY TRÌNH NGHIỆP VỤ CỐT LÕI")

    add_heading_2(doc, "2.1. Thiết kế Schema cơ sở dữ liệu quan hệ PostgreSQL 16 (Chuẩn hóa 3NF)")
    add_clean_paragraph(doc, "Cơ sở dữ liệu hotel_db được thiết kế theo tiêu chuẩn dạng chuẩn 3 (3NF), đảm bảo không tồn tại phụ thuộc bắc cầu, loại bỏ dư thừa dữ liệu và tối ưu hóa tốc độ truy vấn thông qua hệ thống khóa ngoại cùng các chỉ mục B-tree phù hợp.")

    # BẢNG 2
    add_table_caption(doc, prefix="Bảng", title="Cấu trúc từ điển dữ liệu các bảng cơ sở dữ liệu hotel_db")
    b2_data = [
        ("room_types", "id (PK)", "SERIAL", "PRIMARY KEY", "Danh mục hạng phòng (Standard, Superior, Suite...)"),
        ("", "code", "VARCHAR(20)", "UNIQUE NOT NULL", "Mã hạng phòng ngắn gọn (STD, SUP, DLX, SUT, PRS)"),
        ("", "base_price_vnd", "NUMERIC(12,0)", "CHECK (>= 0)", "Đơn giá niêm yết mỗi đêm phòng"),
        ("rooms", "id (PK)", "SERIAL", "PRIMARY KEY", "Danh sách buồng phòng vật lý cụ thể"),
        ("", "room_number", "VARCHAR(20)", "UNIQUE NOT NULL", "Số hiệu phòng (ví dụ: P.101, P.202, P.405)"),
        ("", "room_type_id (FK)", "INT", "REFERENCES room_types(id)", "Liên kết phân loại hạng phòng tương ứng"),
        ("", "status", "VARCHAR(30)", "IN ('AVAILABLE','OCCUPIED'..)", "Trạng thái vận hành thực tế của phòng"),
        ("customers", "id (PK)", "SERIAL", "PRIMARY KEY", "Hồ sơ thông tin khách hàng lưu trú"),
        ("", "full_name", "VARCHAR(150)", "NOT NULL", "Họ tên đầy đủ khách hàng (Phùng Thiên Trường)"),
        ("", "id_card", "VARCHAR(50)", "NOT NULL", "Số CCCD/CMND định danh khách hàng"),
        ("", "email", "VARCHAR(150)", "NOT NULL", "Địa chỉ email gửi hóa đơn và xác nhận"),
        ("bookings", "id (PK)", "SERIAL", "PRIMARY KEY", "Phiếu đặt phòng tổng quát"),
        ("", "booking_code", "VARCHAR(50)", "UNIQUE NOT NULL", "Mã đặt phòng duy nhất (NVH-2026-xxx)"),
        ("", "customer_id (FK)", "INT", "REFERENCES customers(id)", "Khách hàng đứng tên người đại diện"),
        ("", "check_in_date", "DATE", "NOT NULL", "Ngày bắt đầu nhận phòng lưu trú"),
        ("", "check_out_date", "DATE", "CHECK (out > in)", "Ngày dự kiến trả phòng thanh toán"),
        ("", "status", "VARCHAR(30)", "IN ('PENDING','CONFIRMED'..)", "Vòng đời xử lý của đơn đặt phòng"),
        ("booking_rooms", "id (PK)", "SERIAL", "PRIMARY KEY", "Bảng trung gian chi tiết buồng phòng được gán"),
        ("", "booking_id (FK)", "INT", "REFERENCES bookings(id)", "Đơn đặt phòng tương ứng"),
        ("", "room_id (FK)", "INT", "REFERENCES rooms(id)", "Phòng vật lý được phân bổ cho khách"),
        ("payment_tx", "id (PK)", "SERIAL", "PRIMARY KEY", "Lịch sử giao dịch ngân hàng / VietQR"),
        ("", "transaction_id", "BIGINT", "UNIQUE NOT NULL", "Mã giao dịch phát sinh từ phía cổng SePay")
    ]

    tbl_b2 = doc.add_table(rows=len(b2_data) + 1, cols=5)
    tbl_b2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b2.autofit = False
    set_table_borders(tbl_b2)

    b2_widths = [Cm(2.6), Cm(3.2), Cm(2.4), Cm(3.6), Cm(4.7)]
    for r in tbl_b2.rows:
        for i, w in enumerate(b2_widths):
            r.cells[i].width = w

    headers_b2 = ["Tên Bảng", "Cột / Khóa", "Kiểu Dữ Liệu", "Ràng Buộc (Constraints)", "Ý Nghĩa Nghiệp Vụ"]
    for i, h in enumerate(headers_b2):
        cell = tbl_b2.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, row_vals in enumerate(b2_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_vals):
            cell = tbl_b2.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx in [0, 1] and text != "":
                r.font.bold = True

    add_heading_2(doc, "2.2. Sơ đồ thực thể liên kết dữ liệu (ERD)")
    add_clean_paragraph(doc, "Sơ đồ thực thể liên kết mô tả mối quan hệ giữa các bảng cơ sở dữ liệu hotel_db, thể hiện rõ các ràng buộc khóa chính, khóa ngoại và chỉ mục đảm bảo tính toàn vẹn tham chiếu.")

    # Hình 2
    img2_path = "docs/images/hinh2_erd_database.png"
    if os.path.exists(img2_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img2_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Sơ đồ thực thể liên kết dữ liệu (Entity-Relationship Diagram - ERD)")

    add_heading_2(doc, "2.3. Thuật toán chống trùng lịch (Anti-Overbooking) bằng Pessimistic Locking")
    add_clean_paragraph(doc, "Một trong những thách thức kỹ thuật lớn nhất trong hệ thống khách sạn là hiện tượng tranh chấp đặt phòng đồng thời (Concurrency Race Condition). Khi hai người dùng cùng bấm xác nhận đặt cùng một phòng vào cùng một khoảng thời gian, nếu không có cơ chế kiểm soát, hệ thống sẽ rơi vào tình trạng bán lặp (Overbooking).")
    add_clean_paragraph(doc, "Quy trình giải quyết triệt để vấn đề bằng khóa bi quan trong backend:")
    add_clean_paragraph(doc, "Khởi tạo Transaction nguyên tử (BEGIN): Mọi thao tác đọc, kiểm tra và ghi dữ liệu đều diễn ra trong cùng một phiên giao dịch CSDL duy nhất.", is_bullet=True)
    add_clean_paragraph(doc, "Khóa bi quan hàng dữ liệu phòng (SELECT ... FOR UPDATE): Khi bắt đầu kiểm tra phòng, câu lệnh lập tức khóa dòng dữ liệu của phòng đó lại. Các yêu cầu đồng thời khác muốn đọc hoặc ghi vào cùng phòng này sẽ phải chờ trong hàng đợi.", is_bullet=True)
    add_clean_paragraph(doc, "Xác minh giao thoa thời gian lưu trú (Date Overlap Check): Thực thi truy vấn kiểm tra xem phòng có bất kỳ đơn đặt phòng nào khác ở trạng thái khác CANCELLED mà khoảng ngày giao nhau hay không.", is_bullet=True)
    add_clean_paragraph(doc, "Commit hoặc Rollback giao dịch: Nếu phát hiện trùng ngày, tiến trình lập tức ROLLBACK và trả về mã HTTP 409 Conflict; nếu phòng hoàn toàn trống, tiến trình ghi nhận đơn hàng mới và COMMIT thành công.", is_bullet=True)

    add_code_block(doc, 
"""-- Đoạn mã SQL khóa bi quan và kiểm tra trùng ngày phòng
BEGIN;
SELECT * FROM rooms WHERE id = $1 FOR UPDATE;

SELECT b.id FROM bookings b
JOIN booking_rooms br ON b.id = br.booking_id
WHERE br.room_id = $1
  AND b.status NOT IN ('CANCELLED')
  AND (b.check_in_date < $3 AND b.check_out_date > $2)
LIMIT 1;
-- Nếu có bản ghi trả về -> ROLLBACK (HTTP 409)
-- Nếu không có bản ghi -> INSERT INTO bookings & COMMIT (HTTP 201)""")

    add_heading_2(doc, "2.4. Quy trình xác thực phân quyền quản trị (JWT & Bcrypt Security)")
    add_clean_paragraph(doc, "Phân hệ quản trị PMS được bảo vệ bằng mô hình xác thực mã hóa stateless:")
    add_clean_paragraph(doc, "Mật khẩu quản trị viên được băm và đối soát an toàn thông qua hàm băm Bcrypt, tránh lưu trữ mật khẩu ở dạng văn bản thuần (plain text).", is_bullet=True)
    add_clean_paragraph(doc, "Khi đăng nhập thành công qua /api/auth/login, máy chủ cấp một mã JSON Web Token (JWT) được ký bằng thuật toán HMAC-SHA256 với thời hạn hiệu lực 12 giờ.", is_bullet=True)
    add_clean_paragraph(doc, "Mọi endpoint quản trị nhạy cảm đều được bảo vệ bởi middleware xác thực authMiddleware, kiểm tra tính toàn vẹn chữ ký và thời hạn token trước khi xử lý nghiệp vụ.", is_bullet=True)

    # BẢNG 3
    add_table_caption(doc, prefix="Bảng", title="Ma trận phân quyền các endpoint API trong hệ thống")
    b3_data = [
        ("GET /api/rooms", "Công khai", "Tra cứu danh sách buồng phòng theo tiêu chí lọc"),
        ("GET /api/room-types", "Công khai", "Lấy danh mục các hạng phòng và bảng giá cơ sở"),
        ("POST /api/bookings", "Công khai", "Tạo đơn đặt phòng mới (Áp dụng khóa bi quan)"),
        ("GET /api/bookings/:code", "Công khai", "Tra cứu trạng thái phiếu đặt phòng theo mã đặt phòng"),
        ("POST /api/auth/login", "Công khai", "Xác thực tài khoản quản trị và cấp mã JWT token"),
        ("GET /api/admin/dashboard", "Yêu cầu JWT", "Truy vấn thống kê công suất buồng và doanh thu"),
        ("PATCH /api/admin/rooms/:id", "Yêu cầu JWT", "Cập nhật trạng thái bảo dưỡng, dọn dẹp buồng phòng"),
        ("POST /api/payments/sepay-ipn", "API Key / IPN", "Webhook tiếp nhận thông báo thanh toán tự động")
    ]

    tbl_b3 = doc.add_table(rows=len(b3_data) + 1, cols=3)
    tbl_b3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b3.autofit = False
    set_table_borders(tbl_b3)

    b3_widths = [Cm(5.0), Cm(3.2), Cm(8.3)]
    for r in tbl_b3.rows:
        for i, w in enumerate(b3_widths):
            r.cells[i].width = w

    headers_b3 = ["Endpoint API", "Mức Quyền Hạn", "Mô Tả Chức Năng Nghiệp Vụ"]
    for i, h in enumerate(headers_b3):
        cell = tbl_b3.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (ep, perm, desc) in enumerate(b3_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate([ep, perm, desc]):
            cell = tbl_b3.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.name = "Consolas"
                r.font.size = Pt(9.0)
                r.font.bold = True

    add_heading_2(doc, "2.5. Tích hợp cổng thanh toán trực tuyến tự động (VietQR & Webhook IPN)")
    add_clean_paragraph(doc, "Để mang lại trải nghiệm thanh toán thuận tiện nhất cho khách hàng nội địa, hệ thống tích hợp giải pháp thanh toán mã VietQR chuẩn Napas 247. Khi khách hàng xác nhận đặt phòng thành công, giao diện tự động dựng mã QR động kèm số tiền chính xác và nội dung chuyển khoản là mã phiếu đặt phòng (ví dụ: NVH-2026-001).")
    add_clean_paragraph(doc, "Khi tiền về tài khoản ngân hàng, hệ thống cổng SePay ghi nhận biến động số dư và phát tín hiệu Webhook Instant Payment Notification (IPN) đến máy chủ Backend. Máy chủ đối chiếu chữ ký bảo mật, xác thực mã đơn hàng và tự động cập nhật trạng thái đơn đặt phòng sang CONFIRMED trong thời gian dưới 1 giây.")

    add_heading_2(doc, "2.6. Sơ đồ tuần tự nghiệp vụ đặt phòng và thanh toán")
    add_clean_paragraph(doc, "Sơ đồ tuần tự thể hiện chi tiết từng bước tương tác giữa Người dùng, Giao diện Web, Máy chủ API, Cơ sở dữ liệu và Cổng thanh toán mã QR:")

    # Hình 3
    img3_path = "docs/images/hinh3_sequence_booking.png"
    if os.path.exists(img3_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img3_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Sơ đồ tuần tự quy trình đặt phòng và khóa bi quan (Pessimistic Locking)")

    # -------------------------------------------------------------------------
    # CHƯƠNG 3
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 3: TRIỂN KHAI THỰC TẾ, CẤU HÌNH BẢO MẬT VÀ REVERSE PROXY")

    add_heading_2(doc, "3.1. Thiết lập biến môi trường bảo mật (.env) và nguyên tắc loại trừ")
    add_clean_paragraph(doc, "Toàn bộ cấu hình nhạy cảm của hệ thống được quản lý tập trung thông qua tệp biến môi trường .env tại thư mục gốc dự án. Nhằm tuân thủ nguyên tắc bảo mật phần mềm và bài học từ các sự cố lộ lọt thông tin, các tiêu chuẩn sau được áp dụng triệt để:")
    add_clean_paragraph(doc, "Mật khẩu ngẫu nhiên độ phức tạp cao: Các mật khẩu quan trọng như POSTGRES_PASSWORD (5MBvOYeaickl), GRAFANA_ADMIN_PASSWORD (RSCZrbHMtKiC) và ADMIN_PASSWORD (L7R2cn9EsXTT) đều được tạo ngẫu nhiên 12 ký tự chữ và số, triệt tiêu nguy cơ tấn công brute-force.", is_bullet=True)
    add_clean_paragraph(doc, "Không chú thích, không code thừa: Tệp .env được giữ sạch sẽ, chỉ chứa các cặp khóa-giá trị phục vụ trực tiếp cho hoạt động của các container.", is_bullet=True)
    add_clean_paragraph(doc, "Loại trừ bắt buộc trên Git: Tệp .env được cấu hình nghiêm ngặt trong .gitignore, đảm bảo tuyệt đối không bị commit lên kho lưu trữ GitHub công cộng.", is_bullet=True)

    add_heading_2(doc, "3.2. Cấu hình Nginx Reverse Proxy, Điều hướng /api/ và Tối ưu hóa Bộ đệm")
    add_clean_paragraph(doc, "Trong môi trường triển khai thực tế trên máy trạm Localhost, container hotel-frontend tích hợp Nginx Alpine làm máy chủ phân phối tệp tĩnh và Ingress Reverse Proxy. Cấu hình được thiết lập tại frontend/nginx.conf:")

    add_code_block(doc,
"""server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Reverse proxy chuyển tiếp các yêu cầu nghiệp vụ về backend container
    location /api/ {
        proxy_pass http://hotel-backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Định tuyến SPA phục vụ React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Bộ nhớ đệm tài nguyên tĩnh tối ưu hóa tốc độ tải trang
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
}""")

    add_clean_paragraph(doc, "Nhờ cơ chế Reverse Proxy này, toàn bộ các cuộc gọi từ giao diện người dùng tới backend đều đi qua đường dẫn tương đối /api/, loại bỏ hoàn toàn các lỗi liên quan đến chính sách cùng nguồn gốc (CORS) mà không cần cấu hình phức tạp trên trình duyệt.")

    add_heading_2(doc, "3.3. Cơ chế phân giải dịch vụ mạng nội bộ Docker (Service Discovery)")
    add_clean_paragraph(doc, "Docker Compose tích hợp sẵn máy chủ DNS nội bộ cho phép các container tìm thấy nhau thông qua chính tên dịch vụ được định nghĩa trong tệp docker-compose.yml. Nhờ đó, Backend có thể kết nối tới cơ sở dữ liệu qua hostname hotel-postgres:5432, Prometheus có thể cào số liệu qua hostname hotel-backend:5000/metrics, hoàn toàn độc lập với địa chỉ IP động của máy chủ vật lý.")

    # BẢNG 4
    add_table_caption(doc, prefix="Bảng", title="Bảng ánh xạ cổng dịch vụ truy cập môi trường Localhost")
    b4_data = [
        ("Giao diện Khách hàng & Admin", "http://localhost:3001", "Trình duyệt Web", "Mở cổng 3001 truy cập Nginx Frontend"),
        ("Backend REST API", "http://localhost:5000", "Postman / Curl", "Mở cổng 5000 kiểm tra API và Health check"),
        ("PostgreSQL Database", "localhost:5432", "DBeaver / psql", "Mở cổng 5432 quản trị dữ liệu trực tiếp"),
        ("Prometheus Monitoring", "http://localhost:9090", "Trình duyệt Web", "Mở cổng 9090 xem trạng thái Targets và PromQL"),
        ("Grafana Dashboard", "http://localhost:3000", "Trình duyệt Web", "Mở cổng 3000 đăng nhập dashboard KPI RED"),
        ("Loki Log Engine", "http://localhost:3100", "Grafana Datasource", "Mở cổng 3100 nhận log stream từ Promtail")
    ]

    tbl_b4 = doc.add_table(rows=len(b4_data) + 1, cols=4)
    tbl_b4.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b4.autofit = False
    set_table_borders(tbl_b4)

    b4_widths = [Cm(4.5), Cm(4.0), Cm(3.2), Cm(4.8)]
    for r in tbl_b4.rows:
        for i, w in enumerate(b4_widths):
            r.cells[i].width = w

    headers_b4 = ["Dịch Vụ", "URL Truy Cập Host", "Công Cụ Truy Cập", "Ghi Chú Vận Hành"]
    for i, h in enumerate(headers_b4):
        cell = tbl_b4.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (srv, url, tool, note) in enumerate(b4_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate([srv, url, tool, note]):
            cell = tbl_b4.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True
            elif col_idx == 1:
                r.font.name = "Consolas"
                r.font.size = Pt(9.0)

    add_heading_2(doc, "3.4. Hệ sinh thái Giám sát Prometheus, Grafana và Thu thập Log tập trung Loki")
    add_clean_paragraph(doc, "Cụm quan sát được thiết lập nhằm mang lại khả năng bao quát toàn diện về tình trạng sức khỏe của toàn bộ hạ tầng:")
    add_clean_paragraph(doc, "Prometheus Server: Thu thập chỉ số định kỳ mỗi 5 giây từ endpoint /metrics của Backend và máy chủ Node-Exporter.", is_bullet=True)
    add_clean_paragraph(doc, "Grafana Dashboard: Tự động nạp cấu hình (provisioning) nguồn dữ liệu Prometheus và Loki. Cung cấp các biểu đồ thời gian thực về tần suất yêu cầu (RPS), độ trễ phản hồi (p95 latency) và tỷ lệ lỗi.", is_bullet=True)
    add_clean_paragraph(doc, "Loki & Promtail: Promtail theo dõi socket Docker /var/run/docker.sock, đẩy toàn bộ log của các container về Loki. Quản trị viên có thể sử dụng cú pháp LogQL để tra cứu nhanh các lỗi hệ thống.", is_bullet=True)

    # -------------------------------------------------------------------------
    # CHƯƠNG 4
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 4: KIỂM THỬ HỆ THỐNG, ĐÁNH GIÁ VÀ HƯỚNG DẪN VẬN HÀNH")

    add_heading_2(doc, "4.1. Kịch bản kiểm thử API Health Check và tính toàn vẹn CSDL")
    add_clean_paragraph(doc, "Sau khi khởi chạy toàn bộ các dịch vụ trên nền tảng Docker, các bài kiểm thử xác nhận được tiến hành trực tiếp trên máy trạm:")
    add_clean_paragraph(doc, "1. Kiểm tra trạng thái máy chủ Backend và kết nối CSDL:")

    add_code_block(doc,
"""$ curl.exe -s http://127.0.0.1:5000/health
{"status":"UP","timestamp":"2026-10-25T15:59:01.634Z","service":"hotel-backend","database":"CONNECTED"}""")

    add_clean_paragraph(doc, "Kết quả trả về khẳng định Backend đã kết nối thành công và sẵn sàng phục vụ các yêu cầu truy vấn.")
    add_clean_paragraph(doc, "2. Kiểm tra tính toàn vẹn hồ sơ dữ liệu khách hàng được nạp tự động:")

    add_code_block(doc,
"""$ docker exec -i hotel-postgres psql -U postgres -d hotel_db -c \\
  "SELECT id, full_name, id_card, email FROM customers WHERE id=1;"

 id |     full_name      |   id_card    |              email              
----+--------------------+--------------+---------------------------------
  1 | Phùng Thiên Trường | 019200000274 | truong.phung@noveratech.digital""")

    add_clean_paragraph(doc, "Giao diện Cổng khách hàng đặt phòng và Bảng điều khiển Quản trị PMS được chụp trực tiếp từ môi trường Localhost:")

    # Hình 4 & 5
    img4_path = "docs/images/hinh4_giaodien_datphong.png"
    if os.path.exists(img4_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img4_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Giao diện Cổng khách hàng đặt phòng trực tuyến trên Localhost")

    img5_path = "docs/images/hinh5_admin_dashboard.png"
    if os.path.exists(img5_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img5_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Bảng điều khiển Quản trị PMS theo dõi sơ đồ phòng và công suất buồng")

    add_heading_2(doc, "4.2. Kiểm thử tải đồng thời chống xung đột đặt phòng (Concurrency Test)")
    add_clean_paragraph(doc, "Để kiểm chứng tính hiệu quả của thuật toán Khóa bi quan (Pessimistic Locking), một kịch bản kiểm thử tải đồng thời (Concurrency Test) được thực hiện bằng cách gửi hàng loạt yêu cầu đặt cùng phòng P.101 vào cùng khung ngày nhận/trả phòng trong khoảng thời gian dưới 100ms.")

    # BẢNG 5
    add_table_caption(doc, prefix="Bảng", title="Kết quả kiểm thử tải đồng thời thuật toán Anti-Overbooking")
    b5_data = [
        ("10 yêu cầu đồng thời", "1 (Cấp mã phòng hợp lệ)", "9 (Từ chối - Báo phòng đã kín lịch)", "Toàn vẹn tuyệt đối; Không bán trùng"),
        ("20 yêu cầu đồng thời", "1 (Cấp mã phòng hợp lệ)", "19 (Từ chối - Báo phòng đã kín lịch)", "Toàn vẹn tuyệt đối; Không bán trùng"),
        ("50 yêu cầu đồng thời", "1 (Cấp mã phòng hợp lệ)", "49 (Từ chối - Báo phòng đã kín lịch)", "Toàn vẹn tuyệt đối; Không bán trùng")
    ]

    tbl_b5 = doc.add_table(rows=len(b5_data) + 1, cols=4)
    tbl_b5.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b5.autofit = False
    set_table_borders(tbl_b5)

    b5_widths = [Cm(3.8), Cm(3.6), Cm(4.6), Cm(4.5)]
    for r in tbl_b5.rows:
        for i, w in enumerate(b5_widths):
            r.cells[i].width = w

    headers_b5 = ["Kịch Bản Tải", "Thành Công (HTTP 201)", "Bị Từ Chối (HTTP 409)", "Trạng Thái Dữ Liệu"]
    for i, h in enumerate(headers_b5):
        cell = tbl_b5.cell(0, i)
        set_cell_background(cell, "0F2540")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (sc, sc_ok, sc_rej, st) in enumerate(b5_data, start=1):
        shd = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate([sc, sc_ok, sc_rej, st]):
            cell = tbl_b5.cell(row_idx, col_idx)
            set_cell_background(cell, shd)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.font.bold = True

    add_clean_paragraph(doc, "Kết quả chứng minh thuật toán Khóa bi quan hoạt động hoàn hảo, bảo vệ cơ sở dữ liệu khỏi 100% rủi ro Overbooking trong môi trường đồng thời.")

    add_heading_2(doc, "4.3. Kiểm thử thu thập Time-series Metrics và truy vấn LogQL")
    add_clean_paragraph(doc, "1. Kiểm tra trạng thái cào dữ liệu của Prometheus: Truy cập http://localhost:9090/targets, tất cả các endpoint hotel-backend:5000 và node-exporter:9100 đều hiển thị trạng thái UP (Healthy).")
    add_clean_paragraph(doc, "2. Bảng điều khiển Grafana giám sát hiệu năng: Cung cấp đầy đủ các chỉ số RED, biểu đồ lưu lượng và tỷ lệ lấp đầy phòng theo thời gian thực.")

    # Hình 6 & 7
    img6_path = "docs/images/hinh6_grafana_dashboard.png"
    if os.path.exists(img6_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img6_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Bảng điều khiển Grafana giám sát hiệu năng RED Metrics thời gian thực")

    img7_path = "docs/images/hinh7_prometheus_targets.png"
    if os.path.exists(img7_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img7_path, width=Cm(14.5))
        add_figure_caption(doc, prefix="Hình", title="Nhật ký và trạng thái các Endpoints giám sát qua Prometheus")

    add_heading_2(doc, "4.4. Quy trình khởi chạy, sao lưu dữ liệu và phục hồi sự cố (Disaster Recovery)")
    add_clean_paragraph(doc, "Nhằm đảm bảo tính sẵn sàng cao và khả năng phục hồi nhanh chóng khi xảy ra lỗi hệ thống, các quy trình vận hành tiêu chuẩn được văn bản hóa như sau:")
    add_clean_paragraph(doc, "1. Quy trình khởi chạy toàn bộ cụm dịch vụ:")

    add_code_block(doc,
"""# 1. Khởi tạo mạng liên thông ngoài
docker network create novera_network

# 2. Khởi động toàn bộ container nền tảng
docker compose up -d --build

# 3. Kiểm tra trạng thái sức khỏe các dịch vụ
docker compose ps""")

    add_clean_paragraph(doc, "2. Quy trình Sao lưu dữ liệu (Backup):")

    add_code_block(doc,
"""# Xuất toàn bộ dữ liệu CSDL ra tệp SQL sao lưu
docker exec -t hotel-postgres pg_dump -U postgres hotel_db > backup_hotel_db_$(date +%Y%m%d).sql""")

    add_clean_paragraph(doc, "3. Quy trình Phục hồi dữ liệu khi gặp sự cố (Disaster Recovery):")

    add_code_block(doc,
"""# Nạp lại dữ liệu từ tệp sao lưu vào container CSDL
docker exec -i hotel-postgres psql -U postgres -d hotel_db < backup_hotel_db_20261025.sql""")

    # -------------------------------------------------------------------------
    # KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------------------
    add_heading_1(doc, "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "1. Kết quả đạt được")
    add_clean_paragraph(doc, "Triển khai thành công 100% hệ thống Đặt phòng Khách sạn Chuẩn Doanh nghiệp trên nền tảng Docker với 7 container liên thông bền vững, bảo đảm độ cô lập và hiệu năng cao.", is_bullet=True)
    add_clean_paragraph(doc, "Xây dựng cơ sở dữ liệu quan hệ PostgreSQL chuẩn 3NF, tích hợp thành công thuật toán chống trùng lịch bằng khóa bi quan (SELECT ... FOR UPDATE), bảo đảm tính toàn vẹn ACID tuyệt đối.", is_bullet=True)
    add_clean_paragraph(doc, "Tối ưu hóa cấu hình mạng và Nginx reverse proxy giúp hệ thống vận hành mượt mà trên môi trường Localhost (localhost:3001) mà không gặp bất kỳ lỗi CORS hay định tuyến nào.", is_bullet=True)
    add_clean_paragraph(doc, "Thiết lập cụm quan sát hiện đại (Prometheus, Grafana, Loki), cho phép theo dõi thời gian thực các chỉ số RED và truy vấn nhật ký tập trung thông qua LogQL.", is_bullet=True)
    add_clean_paragraph(doc, "Mã nguồn được chuẩn hóa và quản lý trên GitHub theo đúng rubric học phần với định danh duy nhất của sinh viên: DIOVN (Phùng Thiên Trường - DTC245200274).", is_bullet=True)

    add_heading_2(doc, "2. Hạn chế tồn đọng")
    add_clean_paragraph(doc, "Môi trường Localhost hiện tại chạy trên giao thức HTTP thường, chưa tích hợp chứng chỉ bảo mật SSL/TLS tự ký (Self-signed certificate).", is_bullet=True)
    add_clean_paragraph(doc, "Cổng thanh toán SePay đang hoạt động ở chế độ Sandbox thử nghiệm, chưa kích hoạt tài khoản định danh doanh nghiệp thực tế.", is_bullet=True)

    add_heading_2(doc, "3. Hướng phát triển nâng cấp")
    add_clean_paragraph(doc, "Nâng cấp cụm dịch vụ lên môi trường điều phối container Kubernetes (K8s) với cơ chế tự động mở rộng theo tải (Horizontal Pod Autoscaler - HPA).", is_bullet=True)
    add_clean_paragraph(doc, "Bổ sung bộ đệm phân tán Redis Caching để tăng tốc độ truy vấn danh mục phòng trống lên gấp 10 lần.", is_bullet=True)
    add_clean_paragraph(doc, "Tích hợp cổng AI Chatbot tư vấn chọn phòng và hỗ trợ đặt dịch vụ tự động cho khách hàng.", is_bullet=True)

    # -------------------------------------------------------------------------
    # TÀI LIỆU THAM KHẢO
    # -------------------------------------------------------------------------
    add_heading_1(doc, "TÀI LIỆU THAM KHẢO")

    refs = [
        "[1] Docker Inc., \"Docker Compose File Reference v3 & Best Practices,\" Docker Documentation, 2024. [Online]. Available: https://docs.docker.com/compose/",
        "[2] PostgreSQL Global Development Group, \"PostgreSQL 16 Documentation: Concurrency Control and Explicit Locking,\" 2024. [Online]. Available: https://www.postgresql.org/docs/16/explicit-locking.html",
        "[3] Prometheus Authors, \"Prometheus Monitoring System and Time Series Database,\" The Linux Foundation, 2024. [Online]. Available: https://prometheus.io/docs/",
        "[4] Grafana Labs, \"Grafana Loki: Like Prometheus, but for logs,\" 2024. [Online]. Available: https://grafana.com/docs/loki/",
        "[5] Bộ Nội Vụ, \"Nghị định số 30/2020/NĐ-CP về Công tác văn thư và Thể thức trình bày văn bản hành chính,\" Chính phủ Nước CHXHCN Việt Nam, ban hành ngày 05/03/2020."
    ]

    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-1.0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.color.rgb = TEXT_COLOR

    # Lưu tài liệu Word
    out_dir = "docs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Bao_Cao_Trien_Khai_He_Thong.docx")
    doc.save(out_path)
    print(f"Xuất file thành công: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    build_report()
