#!/usr/bin/env python3
"""
Environment Variable Validation Script
Ensures all required environment variables are set before deployment
"""

import os
import sys
import re
from typing import List, Tuple

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def print_error(message: str):
    print(f"{RED}✗ {message}{NC}")


def print_success(message: str):
    print(f"{GREEN}✓ {message}{NC}")


def print_warning(message: str):
    print(f"{YELLOW}⚠ {message}{NC}")


def print_info(message: str):
    print(f"ℹ {message}")


def load_env_file(filepath: str) -> dict:
    """Load environment variables from a file"""
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print_error(f"File not found: {filepath}")
        return {}
    return env_vars


def validate_required_vars(env_vars: dict, is_production: bool = False) -> List[str]:
    """Validate that required environment variables are set"""
    errors = []
    
    # Required for all environments
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for Whisper transcription',
        'ANTHROPIC_API_KEY': 'Anthropic API key for Claude SBAR generation',
    }
    
    # Additional required vars for production
    if is_production:
        required_vars.update({
            'SECRET_KEY': 'JWT secret key (generate with: openssl rand -hex 32)',
            'DATABASE_URL': 'PostgreSQL database connection string',
            'POSTGRES_PASSWORD': 'PostgreSQL password',
            'REDIS_PASSWORD': 'Redis password',
        })
    
    for var, description in required_vars.items():
        value = env_vars.get(var, '')
        
        # Check if variable is missing
        if not value:
            errors.append(f"{var} is not set ({description})")
            continue
        
        # Check if variable has placeholder value
        placeholders = [
            '[REQUIRED',
            'your-',
            'changeme',
            'change-me',
            'change_me',
            'xxx',
            'example',
            'test',
        ]
        
        if any(placeholder in value.lower() for placeholder in placeholders):
            errors.append(f"{var} has placeholder value: {value[:50]}...")
            continue
    
    return errors


def validate_secret_key(secret_key: str) -> Tuple[bool, str]:
    """Validate that SECRET_KEY is strong enough"""
    if not secret_key:
        return False, "SECRET_KEY is empty"
    
    if len(secret_key) < 32:
        return False, f"SECRET_KEY is too short ({len(secret_key)} chars, minimum 32)"
    
    # Check if it's a hex string (recommended format)
    if not re.match(r'^[0-9a-fA-F]+$', secret_key):
        return True, "SECRET_KEY is set but not in hex format (consider using: openssl rand -hex 32)"
    
    return True, "SECRET_KEY is valid"


def validate_api_keys(env_vars: dict) -> List[str]:
    """Validate API key formats"""
    warnings = []
    
    # OpenAI key format: sk-proj-... or sk-...
    openai_key = env_vars.get('OPENAI_API_KEY', '')
    if openai_key and not openai_key.startswith('sk-'):
        warnings.append("OPENAI_API_KEY doesn't look like a valid OpenAI key (should start with 'sk-')")
    
    # Anthropic key format: sk-ant-...
    anthropic_key = env_vars.get('ANTHROPIC_API_KEY', '')
    if anthropic_key and not anthropic_key.startswith('sk-ant-'):
        warnings.append("ANTHROPIC_API_KEY doesn't look like a valid Anthropic key (should start with 'sk-ant-')")
    
    return warnings


def validate_urls(env_vars: dict) -> List[str]:
    """Validate URL formats"""
    warnings = []
    
    # Check DATABASE_URL format
    db_url = env_vars.get('DATABASE_URL', '')
    if db_url and not db_url.startswith('postgresql://'):
        warnings.append("DATABASE_URL should start with 'postgresql://'")
    
    # Check CORS_ORIGINS format
    cors_origins = env_vars.get('CORS_ORIGINS', '')
    if cors_origins:
        if not (cors_origins.startswith('[') and cors_origins.endswith(']')):
            warnings.append("CORS_ORIGINS should be a JSON array (e.g., '[\"https://example.com\"]')")
        if 'localhost' in cors_origins:
            warnings.append("CORS_ORIGINS contains localhost - remove for production")
    
    return warnings


def validate_security_settings(env_vars: dict, is_production: bool) -> List[str]:
    """Validate security settings"""
    warnings = []
    
    if is_production:
        # Check DEBUG is false
        if env_vars.get('DEBUG', '').lower() != 'false':
            warnings.append("DEBUG should be 'false' in production")
        
        # Check ENVIRONMENT is production
        if env_vars.get('ENVIRONMENT', '').lower() != 'production':
            warnings.append("ENVIRONMENT should be 'production'")
    
    return warnings


def main():
    """Main validation function"""
    print("=" * 70)
    print("EclipseLink AI - Environment Variable Validation")
    print("=" * 70)
    print()
    
    # Check which environment file to validate
    env_file = '.env'
    is_production = False
    
    if len(sys.argv) > 1 and sys.argv[1] == 'production':
        env_file = '.env.production'
        is_production = True
    
    print_info(f"Validating: {env_file}")
    print_info(f"Environment: {'Production' if is_production else 'Development'}")
    print()
    
    # Load environment variables
    env_vars = load_env_file(env_file)
    if not env_vars:
        print_error(f"Failed to load {env_file}")
        print_info(f"Create it with: cp {env_file}.example {env_file}")
        sys.exit(1)
    
    print_success(f"Loaded {len(env_vars)} environment variables")
    print()
    
    # Run validations
    all_errors = []
    all_warnings = []
    
    # 1. Check required variables
    print("Checking required variables...")
    errors = validate_required_vars(env_vars, is_production)
    if errors:
        all_errors.extend(errors)
        for error in errors:
            print_error(error)
    else:
        print_success("All required variables are set")
    print()
    
    # 2. Validate SECRET_KEY
    if is_production:
        print("Validating SECRET_KEY...")
        secret_key = env_vars.get('SECRET_KEY', '')
        valid, message = validate_secret_key(secret_key)
        if valid:
            print_success(message)
        else:
            print_error(message)
            all_errors.append(message)
        print()
    
    # 3. Validate API keys
    print("Validating API keys...")
    warnings = validate_api_keys(env_vars)
    if warnings:
        all_warnings.extend(warnings)
        for warning in warnings:
            print_warning(warning)
    else:
        print_success("API keys look valid")
    print()
    
    # 4. Validate URLs
    print("Validating URLs...")
    warnings = validate_urls(env_vars)
    if warnings:
        all_warnings.extend(warnings)
        for warning in warnings:
            print_warning(warning)
    else:
        print_success("URLs look valid")
    print()
    
    # 5. Validate security settings
    if is_production:
        print("Validating security settings...")
        warnings = validate_security_settings(env_vars, is_production)
        if warnings:
            all_warnings.extend(warnings)
            for warning in warnings:
                print_warning(warning)
        else:
            print_success("Security settings are correct")
        print()
    
    # Summary
    print("=" * 70)
    print("Validation Summary")
    print("=" * 70)
    print()
    
    if all_errors:
        print_error(f"Found {len(all_errors)} errors:")
        for error in all_errors:
            print(f"  • {error}")
        print()
        
        if is_production:
            print_info("Fix these errors before deploying to production!")
            print_info("Generate SECRET_KEY with: openssl rand -hex 32")
        
        sys.exit(1)
    
    if all_warnings:
        print_warning(f"Found {len(all_warnings)} warnings:")
        for warning in all_warnings:
            print(f"  • {warning}")
        print()
    
    print_success("✅ Environment validation passed!")
    
    if is_production:
        print()
        print_info("Production deployment checklist:")
        print("  [ ] All errors fixed")
        print("  [ ] All warnings reviewed")
        print("  [ ] Secrets rotated from development")
        print("  [ ] Database backups configured")
        print("  [ ] Monitoring enabled")
        print("  [ ] SSL/TLS certificates valid")
        print("  [ ] HIPAA compliance review completed")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
