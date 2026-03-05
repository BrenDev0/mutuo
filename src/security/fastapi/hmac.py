import os
import logging
import hmac
import hashlib
import time
from fastapi import Request, HTTPException
logger = logging.getLogger(__name__)

def verify_hmac(request: Request) -> bool:
    """
    Verify HMAC signature for incoming requests
    Use with Depends() on specific routes that need HMAC verification
    """

    ## disactivate for development
    project_environment = os.getenv("ENVIRONMENT")
    if project_environment != "PRODUCTION":
        return True

    secret = os.getenv("HMAC_SECRET")
    if not secret:
        raise ValueError("Missing HMAC_SECRET environment variable")
     
    logger.error(f"Headers: {request.headers}")
    signature = request.headers.get('x-signature')
    payload = request.headers.get('x-payload')
    
    if not signature or not payload:
        logger.error(f"Missing signature or payload, ::: signature: {signature} ::: payload: {payload}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Validate timestamp
    try:
        timestamp = int(payload)
    except ValueError:
        logger.error(f"Invalid timestamp ::: timestamp: {payload}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    allowed_drift = 30_000  # 60 seconds
    
    if abs(current_time - timestamp) > allowed_drift:
        logger.error(f"Expired ::: timestamp: {timestamp}, ::: current_time: {current_time}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Generate expected signature
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures using constant-time comparison
    if not hmac.compare_digest(signature, expected):
        logger.error(f"Comparison failed ::: expected: {expected} ::: received: {signature}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return True