# RPA de Automatización Web

Este proyecto implementa un RPA (Automatización Robótica de Procesos) para automatizar el proceso de login en aplicaciones web y soporte para autenticación de dos factores.

## Autor

Desarrollado por [Nicolás Martínez](https://www.linkedin.com/in/martineznae/)

## Características

- Interfaz gráfica para gestión de credenciales
- Encriptación segura de credenciales
- Simulación de comportamiento humano para evitar detección
- Soporte para autenticación de dos factores
- Modo headless (sin interfaz de navegador)
- Compilación a ejecutable standalone (.exe)

## Requisitosi

```bash
pip install -r requirements.txt
```

## Uso

### Interfaz Gráfica

```bash
python gui.py
```

### Línea de Comandos

```bash
python main.py
```

## Compilación a Ejecutable

1. Instalar PyInstaller:
```bash
pip install pyinstaller
```

2. Compilar el proyecto:
```bash
pyinstaller rpa.spec
```

El ejecutable se generará en la carpeta `dist`.

## Configuración

Las credenciales se almacenan de forma segura en `config.json` y se encriptan usando una clave almacenada en `encryption.key`.

## Características Anti-detección

- Delays aleatorios entre acciones
- Simulación de escritura humana
- Eliminación de firmas de automatización
- Headers y user-agents personalizados

## Manejo de Errores

- Timeout en elementos web
- Credenciales incorrectas
- Fallos de red
- Cambios en el DOM
- Soporte para CAPTCHA (manual)

## Seguridad

- Las credenciales se almacenan encriptadas
- La clave de encriptación se genera automáticamente
- No se almacenan credenciales en texto plano
