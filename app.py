import io
import base64

import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# --- Demo investor credentials (replace with DB in production) ---
# Generate a fresh totp_secret per user with: pyotp.random_base32()
INVESTORS = {
    'john.smith@investor.com': {
        'password': 'demo1234',
        'name': 'John Smith',
        'totp_secret': 'JBSWY3DPEHPK3PXP',
    },
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'investor_email' not in session:
            flash('Please log in to access the investor portal.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/strategy')
def strategy():
    return render_template('strategy.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'investor_email' in session:
        return redirect(url_for('portal'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        code = request.form.get('otp', '').strip()
        user = INVESTORS.get(email)
        if user and user['password'] == password:
            totp = pyotp.TOTP(user['totp_secret'])
            # TODO: remove dev bypass before production
            if code == '123456' or totp.verify(code, valid_window=1):
                session['investor_email'] = email
                session['investor_name'] = user['name']
                return redirect(url_for('portal'))
        flash('Invalid credentials or authenticator code. Please try again.', 'error')
    return render_template('login.html')

@app.route('/login/setup')
def login_setup():
    email = request.args.get('email', '').strip().lower()
    user = INVESTORS.get(email)
    if not user:
        return redirect(url_for('login'))
    uri = pyotp.TOTP(user['totp_secret']).provisioning_uri(
        name=email, issuer_name='CoinOfVantage'
    )

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    return render_template('login_setup.html', qr_b64=qr_b64, secret=user['totp_secret'])

@app.route('/portal')
@login_required
def portal():
    name = session.get('investor_name', 'Investor')
    return render_template('portal.html', name=name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
