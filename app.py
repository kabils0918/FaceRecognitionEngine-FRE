import csv
import os
import shutil
from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template, send_file, request, jsonify, send_from_directory
from flask import redirect, url_for 

# Set field size limit to max 32-bit int
csv.field_size_limit(2**31 - 1)

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

CSV_FILE = os.path.join(os.path.dirname(__file__), 'data', 'detection_log.csv')
# CHANGED: IMAGE_DIR now points to the subfolder 'Terrorist_Data'
IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'captured_faces', 'Terrorist_Data')

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print(f"[INFO] Created image directory at {IMAGE_DIR}")


@app.route('/')
def dashboard():
    detections = []
    daily_counts = defaultdict(int)

    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)
            # Skip header row if it exists, otherwise process the first row
            first_row = next(reader, None)
            if first_row:
                if first_row[0] == 'Timestamp': # Check if it's the header
                    pass # Skip it
                else:
                    # If it's not a header, it's data, so append it and count
                    if len(first_row) >= 5:
                        detections.append(first_row)
                        date_str = first_row[0].split(' ')[0]
                        daily_counts[date_str] += 1
            
            for row in reader:
                if len(row) >= 5:
                    detections.append(row)
                    date_str = row[0].split(' ')[0]
                    daily_counts[date_str] += 1
    except FileNotFoundError:
        print("[WARNING] detection_log.csv not found. No detections to display.")
    except Exception as e:
        print(f"[ERROR] Error reading CSV: {e}")

    chart_labels = sorted(daily_counts.keys())
    chart_values = [daily_counts[date] for date in chart_labels]


    latest = detections[-1] if detections else None
    is_terrorist = latest and latest[3].lower() == "terrorist"

    return render_template(
        'dashboard.html',
        detections=detections,
        latest=latest,
        chart_labels=chart_labels,
        chart_values=chart_values,
        is_terrorist=is_terrorist
    )

@app.route('/images/<path:filename>') # Changed to <path:filename> to handle subdirectories in URL
def serve_image(filename):
    # This expects `filename` to be something like 'captured_faces/Terrorist_Data/image.jpg'
    # as Flask's `url_for('static', filename=...)` will construct the path relative to `static/`.
    return send_from_directory(app.static_folder, filename)

@app.route('/download')
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, mimetype='text/csv', as_attachment=True, download_name='detection_log.csv')
    else:
        return "Error: detection_log.csv not found.", 404

@app.route('/clear_all', methods=['POST'])
def clear_all():
    print("[INFO] clear_all endpoint called")
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({"status": "error", "message": "CSV not found."}), 404

        backup_file = os.path.join(os.path.dirname(__file__), 'data', f'detection_log_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        shutil.copy2(CSV_FILE, backup_file)
        print(f"[INFO] Backup created: {backup_file}")

        if os.path.exists(IMAGE_DIR): # Check if directory exists
            for file in os.listdir(IMAGE_DIR):
                file_path = os.path.join(IMAGE_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"[INFO] Deleted image: {file_path}")
        else:
            print(f"[WARNING] Image directory not found at {IMAGE_DIR}. Nothing to clear.")

        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Person_ID_Numeric', 'Person_Name_or_ID', 'Category', 'Image_Filename'])
        print("[INFO] CSV log cleared and header re-written.")

        return redirect(url_for('dashboard'))

    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied. Ensure files are not open."}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/dashboard-data')
def dashboard_data():
    detections = []
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)
            # Skip header row if it exists
            first_row = next(reader, None)
            if first_row and first_row[0] == 'Timestamp':
                pass
            else:
                if first_row:
                    if len(first_row) >= 5:
                        detections.append(first_row) # Append if it's data and not a header
            
            for row in reader:
                if len(row) >= 5:
                    detections.append(row)
    except FileNotFoundError:
        print("[WARNING] CSV file not found.")

    latest = detections[-1] if detections else None
    return jsonify({
        'detections': detections,
        'latest': latest
    })

@app.route('/clear_latest', methods=['POST'])
def clear_latest():
    print("[INFO] clear_latest endpoint called")
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({"status": "error", "message": "CSV not found."}), 404

        with open(CSV_FILE, 'r') as file:
            lines = file.readlines()

        # Check if there's only a header or no lines at all
        if not lines or (len(lines) == 1 and lines[0].strip().startswith('Timestamp')):
            return jsonify({"status": "error", "message": "No data entries to clear (only header or empty)."}), 400

        # Get the last data line (excluding header if present)
        # If the first line is header, we want to clear the one before the end.
        # If there's no header, or only one data line, clear the last one.
        if len(lines) > 1 and lines[0].strip().startswith('Timestamp'):
            last_line_index = len(lines) - 1
        else:
            last_line_index = len(lines) - 1
        
        last_line_content = lines[last_line_index].strip().split(',')
        
        if len(last_line_content) < 5:
            return jsonify({"status": "error", "message": "Malformed last CSV entry."}), 400

        image_filename_in_csv = last_line_content[4]

        # Extract the actual filename from the full path stored in CSV
        # Example: 'static/captured_faces/Terrorist_Data/image.jpg' -> 'image.jpg'
        actual_image_filename = os.path.basename(image_filename_in_csv)
        image_path_on_disk = os.path.join(IMAGE_DIR, actual_image_filename) # Corrected variable name

        # Write all lines except the last data line
        lines_to_write = lines[:last_line_index]
        with open(CSV_FILE, 'w', newline='') as file:
            file.writelines(lines_to_write)
        print(f"[INFO] Cleared last entry from CSV.")

        if os.path.exists(image_path_on_disk):
            os.remove(image_path_on_disk)
            print(f"[INFO] Deleted image: {image_path_on_disk}")
        else:
            print(f"[WARNING] Image not found on disk for clearing: {image_path_on_disk}")

        return jsonify({"status": "success", "message": "Latest detection cleared."})

    except Exception as e:
        print(f"[ERROR] Error in clear_latest: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)