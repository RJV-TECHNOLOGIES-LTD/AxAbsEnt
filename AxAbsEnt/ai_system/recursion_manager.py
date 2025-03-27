def check_paradox(result):
    if isinstance(result, dict) and result.get('collapse') or result.get('collapse_triggered'):
        return True
    return False

def handle_collapse(result):
    result['handled'] = 'collapse resolved by AI protocol'
    return result
