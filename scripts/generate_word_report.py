import os, zipfile
from xml.sax.saxutils import escape

INPUT_MD = 'docs/final_year_project_report.md'
OUTPUT_DOCX = 'docs/IGNOU_MCA_Project_Report_BuyNow.docx'


def md_to_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read().splitlines()

    lines = []
    lines.append('IGNOU MCA (MCA_NEW) Project Report - BuyNow E-Commerce System')
    lines.append('Prepared as per MCSP-232 guideline structure.')
    lines.append('')
    for ln in raw:
        if ln.strip().startswith('```mermaid'):
            lines.append('[Diagram block: Mermaid source included in markdown version]')
            continue
        if ln.strip() == '```':
            continue
        if ln.startswith('# '):
            lines.append('')
            lines.append(ln[2:].strip().upper())
            lines.append('')
        elif ln.startswith('## '):
            lines.append('')
            lines.append(ln[3:].strip())
        elif ln.startswith('### '):
            lines.append(ln[4:].strip())
        else:
            lines.append(ln)

    lines.extend([
        '',
        'IGNOU COMPLIANCE CHECKLIST (Quick Reference)',
        '1. Includes software development lifecycle coverage: Yes.',
        '2. Includes objectives, SRS, analysis, design, coding, testing: Yes.',
        '3. Includes DFD/ERD/UML references and database table details: Yes.',
        '4. Includes Gantt and PERT planning guidance: Gantt included; PERT section to be added in final print if required by examiner format.',
        '5. Includes feasibility study and future scope: Yes.',
    ])
    return lines


def build_document_xml(lines):
    body_parts = []
    for line in lines:
        text = escape(line)
        if text == '':
            body_parts.append('<w:p/>')
        else:
            body_parts.append(
                '<w:p><w:r><w:t xml:space="preserve">' + text + '</w:t></w:r></w:p>'
            )

    body_xml = ''.join(body_parts)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
      <w:cols w:space="708"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>'''


def create_docx(lines, output_path):
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    document_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'''

    doc_xml = build_document_xml(lines)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/_rels/document.xml.rels', document_rels)


if __name__ == '__main__':
    lines = md_to_lines(INPUT_MD)
    create_docx(lines, OUTPUT_DOCX)
    print(f'Generated: {OUTPUT_DOCX}')
