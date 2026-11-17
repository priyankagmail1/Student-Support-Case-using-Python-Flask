from flask import Flask, session, request, jsonify, abort
import hmac
import hashlib

app = Flask(__name__)
# A strong secret key used for signing Flask session cookies and HMAC verification
app.secret_key = "super_secure_random_production_secret_key"
HMAC_SECRET = b"another_cryptographic_signing_key"

def generate_secure_hmac_token(data_string):
    """Generates an HMAC-SHA256 signature to guarantee message integrity and prevent spoofing."""
    return hmac.new(HMAC_SECRET, data_string.encode('utf-8'), hashlib.sha256).hexdigest()

def verify_hmac_token(data_string, provided_signature):
    """Verifies the HMAC signature safely using constant-time comparison to prevent timing attacks."""
    expected_signature = generate_secure_hmac_token(data_string)
    return hmac.compare_digest(expected_signature, provided_signature)

@app.route('/login', methods=['POST'])
def login():
    incoming_data = request.get_json()
    username = incoming_data.get('username')
    
    # Authenticate user credentials securely...
    if username == "admin_user":
        # Store verified identity inside Flask's cryptographically signed session
        session['authenticated_user'] = username
        session['role'] = 'administrator'
        
        # Generate an integrity token for sensitive client payloads
        integrity_token = generate_secure_hmac_token(username)
        
        return jsonify({
            "status": "success",
            "message": "Logged in securely.",
            "integrity_token": integrity_token
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/secure-action', methods=['POST'])
def secure_action():
    # 1. Check Flask's signed session (prevents session cookie tampering/spoofing)
    if 'authenticated_user' not in session:
        return jsonify({"error": "Unauthorized access. Session missing or invalid."}), 403
    
    request_payload = request.get_json()
    action_data = request_payload.get('data')
    client_signature = request_payload.get('signature')
    
    # 2. Verify payload integrity using HMAC validation (prevents data spoofing/forgery)
    if not client_signature or not verify_hmac_token(action_data, client_signature):
        abort(400, description="Data spoofing detected! Payload signature verification failed.")
        
    return jsonify({
        "status": "success",
        "user": session['authenticated_user'],
        "result": "Action executed safely with verified data integrity."
    }), 200

if __name__ == '__main__':
    app.run(debug=False)