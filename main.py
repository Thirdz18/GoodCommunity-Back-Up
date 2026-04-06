raw_verified = request.args.get('verified', '')
if raw_verified:
    try:
        decoded = _b64.b64decode(raw_verified + '==').decode('utf-8').strip().lower()
        is_verified_param = decoded  # 'true' o 'false'
    except Exception:
        is_verified_param = raw_verified.lower()
else:
    is_verified_param = request.args.get('isVerified', 'false').lower()
