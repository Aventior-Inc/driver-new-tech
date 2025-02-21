import base64
import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageTemplate, Frame, Image
from reportlab.lib.styles import getSampleStyleSheet
import textwrap
from reportlab.lib.fonts import tt2ps
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def decode_base64_image(image_data):
  """Decodes a base64 image and returns a BytesIO object."""
  try:
    header, encoded = image_data.split(",") if "," in image_data else (None, image_data)
    return BytesIO(base64.b64decode(encoded))
  except Exception:
    return None


def wrap_text(text, width=15):
    """Wrap text to prevent overflowing in table cells."""
    return "\n".join(textwrap.wrap(str(text), width))


def extract_data(item, headers, max_columns=5):
    """Splits headers and values into multiple tables if needed, maintaining background effects."""
    values = [wrap_text(item.get(key, "")) for key in headers]
    table_data = []
    for i in range(0, len(headers), max_columns):
        table_data.append(
            [Paragraph(f'<b>{h}</b>', getSampleStyleSheet()["Normal"]) for h in headers[i:i + max_columns]])
        table_data.append([Paragraph(v, getSampleStyleSheet()["Normal"]) for v in values[i:i + max_columns]])
    return table_data


def footer(canvas, doc):
    """Adds footer for pagination."""
    canvas.saveState()
    footer_text = f"Page {doc.page}"
    canvas.drawString(A4[0] / 2, 20, footer_text)
    canvas.restoreState()

def split_table_data(headers, values, max_columns_per_row):
  """Splits headers and values into multiple rows if they exceed max_columns_per_row."""
  split_headers, split_values = [], []
  for i in range(0, len(headers), max_columns_per_row):
    split_headers.append(headers[i:i + max_columns_per_row])
    split_values.append(values[i:i + max_columns_per_row])
  return split_headers, split_values

def generate_pdf(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=15)

    elements = []

    styles = getSampleStyleSheet()

    letter_head_style = styles["Heading1"]
    letter_head_style.alignment = TA_CENTER
    letter_head_style.textColor = colors.navy
    letter_head_style.alignment = 0  # Left alignment
    letter_head_style.spaceBefore = 0
    letter_head_style.spaceAfter = 0

    letter_para_style = styles["Heading4"]
    letter_para_style.textColor = colors.navy
    letter_para_style.alignment = 0
    letter_para_style.spaceBefore = 0
    letter_para_style.spaceAfter = 0

    title = Paragraph("<b>MINISTRY OF POLICE, PRISONS & CORRECTIONS</b>", letter_head_style)

    left_text = """<b>Samoa Police Headquarters</b><br/>
    PO Box 53 Apia,<br/> SAMOA<br/>
    <b>Tel:</b> (685) 22 222  <b>Fax:</b> (685) 20 848"""
    left_paragraph = Paragraph(left_text, letter_para_style)

    right_text = """<b>Samoa Prisons and Corrections</b><br/>
    PO Box 6102 Tanumalala,<br/> SAMOA<br/>
    <b>Tel:</b> (685) 23516 Fax: (685) 23517"""
    right_paragraph = Paragraph(right_text, letter_para_style)

    # Create Table for Header
    header_data = [
        ["", title, ""],
        ["", left_paragraph, right_paragraph]
    ]
    header_table = Table(header_data, colWidths=[130,300, 300])

    header_table.setStyle(TableStyle([
        ("SPAN", (1, 0), (2, 0)),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(header_table)
    line = Table([[""]], colWidths=[510])
    line.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 2, colors.blue),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(line)
    elements.append(Spacer(1, 5))

    elements.append(Paragraph(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    elements.append(Spacer(1, 10))


    incident_headers = ["Identity", "Email of Encoder", "Location", "Weather", "Light", "Main Cause",
                         "Severity", "Road Defect", "Collision Type", "Reporting Agency", "Location Approximate"]

    incident_values = [data['identity'], data['data']['driverIncidentDetails']['Email of Encoder'], data.get('location_text', 'N/A'),
                       data.get('weather', 'N/A'), data.get('light', 'N/A'),
                       data['data']['driverIncidentDetails']['Main Cause'],
                       data['data']['driverIncidentDetails']['Severity'],
                       data['data']['driverIncidentDetails']['Road Defect'],
                       data['data']['driverIncidentDetails']['Collision Type'],
                       data['data']['driverIncidentDetails']['Reporting Agency'],
                       data['data']['driverIncidentDetails']['Location Approximate']]

    split_incident_headers, split_incident_values = split_table_data(incident_headers, incident_values, 6)

    incident_data = []
    for i in range(len(split_incident_headers)):
      incident_data.append([Paragraph(f'<b>{h}</b>', styles['Normal']) for h in split_incident_headers[i]])
      incident_data.append([Paragraph(str(v), styles['Normal']) for v in split_incident_values[i]])

    incident_table = Table(incident_data)
    incident_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
      ]))

    elements.append(Paragraph("Incident Details", styles["Title"]))
    elements.append(incident_table)
    elements.append(Spacer(1, 12))

    person_headers = ["First Name", "Middle Name", "Last Name", "Age", "Gender", "License Number", "License Status",
                      "Helmet", "Address", "Hospital", "Seat Belt", "Involvement", "Driver error", "License Type",
                      "Type of Injury", "Passenger factor", "Employment Status", "Island of License",
                      "Passenger Leaving", "Type of Employment", "Medical condition impacting the ability to drive"]

    try:
        for idx, driver in enumerate(data["data"]["driverPerson"], start=1):
            elements.append(Paragraph(f"Person {idx}", styles["Title"]))
            elements.append(Spacer(1, 12))
            driver_table = Table(extract_data(driver, person_headers))
            driver_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(driver_table)
            elements.append(Spacer(1, 12))
    except KeyError:
        pass


    vehicle_headers = ["Make & Model", "Plate Number", "License Number", "Vehicle Status", "Defect", "Damage",
                       "Loading", "Surface", "Maneuver", "Direction", "Drive Type", "License Type", "Vehicle type",
                       "Engine number", "Chassis number", "Classification", "Insurance details", "Island of License",
                       "Manufacturing Year", "Vehicle License Status"]

    try:
        for idx, vehicle in enumerate(data["data"]["driverVehicle"], start=1):
            elements.append(Paragraph(f"Vehicle {idx}", styles["Title"]))
            elements.append(Spacer(1, 12))
            vehicle_table = Table(extract_data(vehicle, vehicle_headers))
            vehicle_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(vehicle_table)
            elements.append(Spacer(1, 12))
    except KeyError:
        pass

    try:
        notes_header = "Notes"
        notes_value = data['data']['driverNotes']['Notes']
        notes_data = [[Paragraph(f'<b>{notes_header}</b>', styles['Normal'])],
                      [Paragraph(str(notes_value), styles['Normal'])]]

        notes_table = Table(notes_data)
        notes_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
          ]))
        elements.append(Paragraph("Notes", styles['Title']))
        elements.append(notes_table)
        elements.append(Spacer(1, 12))
    except KeyError:
        pass

    try:
        crash_diagram_headers = ["Crash Type", "Movement Code"]

        crash_diagram_values = [data['data']['driverCrashDiagram']['Crash Type'],
                           data['data']['driverCrashDiagram']['Movement Code']]

        crash_diagram_data = [[Paragraph(f'<b>{h}</b>', styles['Normal']) for h in crash_diagram_headers],
                              [Paragraph(str(v), styles['Normal']) for v in crash_diagram_values]]

        crash_diagram_table = Table(crash_diagram_data)
        crash_diagram_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
          ]))
        elements.append(Paragraph("Crash Diagram", styles['Title']))
        elements.append(crash_diagram_table)
        elements.append(Spacer(1, 12))
    except KeyError:
        pass

    try:
        image_data = base64.b64decode(data['data']['driverCrashDiagram']['Image'].split(',')[1])
        crash_image_path = "temp_logo_image.png"
        with open(crash_image_path, "wb") as image_file:
            image_file.write(image_data)
        crash_image = Image(crash_image_path, height=200, width=200)

        elements.append(crash_image)  # Add image as a separate element
        elements.append(Spacer(1, 12))

        driver_photos_list = []
        if len(data['data']['driverPhoto']) > 0:
            elements.append(Paragraph("Photos", styles['Title']))
            image_id = 1
            for photos_details in data['data']['driverPhoto']:
                image_data = base64.b64decode(photos_details['Picture'].split(',')[1])
                photo_image_path = f"driverPhoto-{image_id}.png"
                image_id += 1
                with open(photo_image_path, "wb") as image_file:
                    image_file.write(image_data)
                photo_image = Image(photo_image_path, height=200, width=200)
                elements.append(photo_image)
                driver_photos_list.append(photo_image_path)
                elements.append(Spacer(1, 5))
                elements.append(Paragraph(photos_details['Description']))
                elements.append(Spacer(1, 5))
    except KeyError:
        pass


    doc.build(elements, onLaterPages=footer, onFirstPage=footer)
    for obj_to_unlink in driver_photos_list:
        os.unlink(obj_to_unlink)
    os.unlink(crash_image_path)
    return filename
