import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# TOKEN DEL BOT
TOKEN = "7942353821:AAEajVvhiu5nH83zKtpElyWnuzJP4OjkGoE"

# LINK DIRECTO A CSV DEL GOOGLE SHEETS
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1qIQXc4OfUfcYVkzOC5r9Wu-sqPiC2qZRWM9K20HBpFo/export?format=csv"

# CONTRASEÑA DE ACCESO
CLAVE_DE_ACCESO = "Y2122C"

# CONJUNTO PARA GUARDAR USUARIOS AUTORIZADOS
usuarios_autorizados = set()

def cargar_datos():
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL, dtype=str)
    df.fillna("", inplace=True)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in usuarios_autorizados:
        await update.message.reply_text("🔐 Ingresá la contraseña para acceder al bot.")
        return
    await update.message.reply_text(
        "🚓 Bot División Sustracción Activo.\n\n"
        "Escribí cualquier dato (expediente, nombre, vehículo, etc.) y te mostraré los resultados relacionados."
    )

async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text.strip().lower()

    if user_id not in usuarios_autorizados:
        if texto == CLAVE_DE_ACCESO.lower():
            usuarios_autorizados.add(user_id)
            await update.message.reply_text("✅ Acceso concedido. Ahora podés usar el bot.")
        else:
            await update.message.reply_text("❌ Contraseña incorrecta. Volvé a intentarlo.")
        return

    df = cargar_datos()
    resultados = []
    for _, fila in df.iterrows():
        if any(texto in str(valor).lower() for valor in fila):
            resultados.append(fila)

    if not resultados:
        await update.message.reply_text("❌ No se encontraron resultados.")
        return

    for fila in resultados:
        mensaje = (
            f"📄 *Cantidad de Expte:* {fila.get('cantidad_de_expte','')}\n"
            f"⚖️ *Carátula:* {fila.get('caratula','')}\n"
            f"👤 *Denunciante:* {fila.get('denunciante','')}\n"
            f"👥 *Inculpado/Protagonista:* {fila.get('inculpado/protagonista','')}\n"
            f"🚗 *Vehículo:* {fila.get('vehiculo','')}\n"
            f"✍️ *Secretario:* {fila.get('secretario','')}\n"
            f"📤 *Salida:* {fila.get('salida','')}\n"
            "-----------------------------"
        )
        await update.message.reply_text(mensaje, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    print("✅ Bot activo y esperando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()
