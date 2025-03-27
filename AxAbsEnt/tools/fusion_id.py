import uuid
def generate_fusion_id(prefix='omega'):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
