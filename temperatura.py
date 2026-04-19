def validar_contraseña(password):
    if len(password) < 8:
        return "Contraseña muy corta (mínimo 8 caracteres)"
    
    if not any(c.isupper() for c in password):
        return "Debe tener mayúsculas"
    
    if not any(c.isdigit() for c in password):
        return "Debe tener números"
    
    return "Contraseña válida"

# Probar
print(validar_contraseña("abc123"))        # Contraseña muy corta...
print(validar_contraseña("Abc123"))        # Contraseña válida
print(validar_contraseña("password123"))   # Debe tener mayúsculas