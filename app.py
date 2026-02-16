"""
Flask Web Application for TOPSIS
Allows users to upload CSV files and receive TOPSIS results via email
"""

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tempfile
import re

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def normalize_matrix(df):
    """Normalize the decision matrix"""
    numeric_data = df.iloc[:, 1:].values
    norm_matrix = numeric_data / np.sqrt((numeric_data ** 2).sum(axis=0))
    return norm_matrix


def calculate_topsis(df, weights, impacts):
    """Calculate TOPSIS scores and rankings"""
    
    # Normalize the decision matrix
    norm_matrix = normalize_matrix(df)
    
    # Calculate weighted normalized matrix
    weighted_matrix = norm_matrix * weights
    
    # Determine ideal best and ideal worst
    ideal_best = np.zeros(len(weights))
    ideal_worst = np.zeros(len(weights))
    
    for i in range(len(weights)):
        if impacts[i] == '+':
            ideal_best[i] = weighted_matrix[:, i].max()
            ideal_worst[i] = weighted_matrix[:, i].min()
        else:
            ideal_best[i] = weighted_matrix[:, i].min()
            ideal_worst[i] = weighted_matrix[:, i].max()
    
    # Calculate Euclidean distances
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    
    # Calculate TOPSIS score
    topsis_score = dist_worst / (dist_best + dist_worst)
    
    # Rank the alternatives
    rank = topsis_score.argsort()[::-1].argsort() + 1
    
    return topsis_score, rank


def send_email_with_attachment(recipient_email, result_file):
    """Send email with TOPSIS result file attached"""
    
    # Email configuration - Update these with your email credentials
    # For Gmail: Use App Password (not regular password)
    # Generate at: https://myaccount.google.com/apppasswords
    sender_email = os.environ.get('SENDER_EMAIL', 'vbansal_be23@thapar.edu')
    sender_password = os.environ.get('SENDER_PASSWORD', 'your_app_password_here')
    
    # Skip email if not configured
    if sender_password == 'your_app_password_here' or not sender_password:
        raise Exception("Email not configured. Set SENDER_EMAIL and SENDER_PASSWORD environment variables")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'TOPSIS Analysis Results'
    
    # Email body
    body = """
    Hello,
    
    Your TOPSIS analysis has been completed successfully.
    
    Please find the results attached to this email.
    
    Best regards,
    TOPSIS Web Service
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the result file
    try:
        with open(result_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename=topsis_result.csv')
            msg.attach(part)
    except Exception as e:
        raise Exception(f"Error attaching file: {str(e)}")
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/sample')
def sample():
    """Serve sample data file for download"""
    from flask import send_file
    import io
    
    # Sample data
    sample_data = """Fund Name,P1,P2,P3,P4,P5
M1,0.84,0.71,6.7,42.1,12.59
M2,0.91,0.83,7.0,31.7,10.11
M3,0.79,0.62,4.8,46.7,13.23
M4,0.78,0.61,6.4,42.4,12.55
M5,0.94,0.88,3.6,62.2,16.91
M6,0.88,0.77,6.5,51.5,14.91
M7,0.66,0.44,5.3,48.9,13.83
M8,0.93,0.87,5.5,53.3,15.07"""
    
    # Create file-like object
    sample_file = io.BytesIO(sample_data.encode('utf-8'))
    sample_file.seek(0)
    
    return send_file(
        sample_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='sample_data.csv'
    )


@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle TOPSIS calculation request"""
    
    try:
        # Get form data
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        weights_str = request.form.get('weights', '')
        impacts_str = request.form.get('impacts', '')
        email = request.form.get('email', '')
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'File must be a CSV file'})
        
        if not weights_str or not impacts_str:
            return jsonify({'success': False, 'error': 'Weights and impacts are required'})
        
        if not email or not validate_email(email):
            return jsonify({'success': False, 'error': 'Valid email address is required'})
        
        # Save uploaded file temporarily
        temp_input = tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False)
        file.save(temp_input.name)
        temp_input.close()
        
        # Read the CSV file
        try:
            df = pd.read_csv(temp_input.name)
        except Exception as e:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': f'Error reading CSV file: {str(e)}'})
        
        # Validate file structure
        if df.shape[1] < 3:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': 'Input file must contain at least three columns'})
        
        # Check numeric values
        numeric_cols = df.iloc[:, 1:]
        try:
            numeric_data = numeric_cols.apply(pd.to_numeric, errors='coerce')
            if numeric_data.isnull().any().any():
                os.unlink(temp_input.name)
                return jsonify({'success': False, 'error': 'From 2nd to last columns must contain numeric values only'})
        except Exception:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': 'From 2nd to last columns must contain numeric values only'})
        
        # Parse weights and impacts
        try:
            weights = [float(w.strip()) for w in weights_str.split(',')]
        except ValueError:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': 'Weights must be numeric values separated by commas'})
        
        impacts = [i.strip() for i in impacts_str.split(',')]
        
        # Validate counts
        num_criteria = df.shape[1] - 1
        
        if len(weights) != num_criteria:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': f'Number of weights must equal number of criteria ({num_criteria})'})
        
        if len(impacts) != num_criteria:
            os.unlink(temp_input.name)
            return jsonify({'success': False, 'error': f'Number of impacts must equal number of criteria ({num_criteria})'})
        
        # Validate impacts
        for impact in impacts:
            if impact not in ['+', '-', '+ve', '-ve']:
                os.unlink(temp_input.name)
                return jsonify({'success': False, 'error': f'Impacts must be either + or - (found: {impact})'})
        
        # Normalize impacts
        impacts = ['+' if i in ['+', '+ve'] else '-' for i in impacts]
        
        # Calculate TOPSIS
        topsis_score, rank = calculate_topsis(df, weights, impacts)
        
        # Create result dataframe
        result_df = df.copy()
        result_df['Topsis Score'] = topsis_score
        result_df['Rank'] = rank
        
        # Save result to temporary file
        temp_output = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        result_df.to_csv(temp_output.name, index=False)
        temp_output.close()
        
        # Send email
        try:
            send_email_with_attachment(email, temp_output.name)
            success_message = f'✅ TOPSIS calculation completed! Results sent to {email}'
        except Exception as e:
            # If email fails, still return success but with a note
            error_msg = str(e)
            if "not configured" in error_msg:
                success_message = f'✅ TOPSIS calculation completed! (Email not configured - see app.py for setup instructions)'
            else:
                success_message = f'✅ TOPSIS calculation completed! (Email failed: {error_msg}. Please check Gmail App Password setup)'
        
        # Clean up temporary files
        os.unlink(temp_input.name)
        os.unlink(temp_output.name)
        
        return jsonify({
            'success': True,
            'message': success_message,
            'results': result_df.to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
