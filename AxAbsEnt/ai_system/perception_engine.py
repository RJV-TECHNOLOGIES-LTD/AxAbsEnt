import os

def scan_domains(base_path):
    domains = []
    for domain in os.listdir(base_path):
        domain_path = os.path.join(base_path, domain)
        if os.path.isdir(domain_path) and 'registry.yaml' in os.listdir(domain_path):
            domains.append(domain)
    return domains
