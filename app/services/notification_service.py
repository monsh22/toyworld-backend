from datetime import datetime

def send_order_confirmation(order_id: int, user_name: str, user_email: str, total: float, items: list):
    """Simula envío de email de confirmación al cliente."""
    print(f"""
╔══════════════════════════════════════════╗
📧 EMAIL ENVIADO A: {user_email}
══════════════════════════════════════════
Asunto: ✅ Pedido #{order_id} confirmado — ToyWorld

Hola {user_name},

¡Tu pedido ha sido recibido con éxito! 🧸

📦 Pedido: #{order_id}
💰 Total: ${total:.2f} MXN
📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Recibirás tu pedido en 3-5 días hábiles.
Puedes rastrear tu pedido en: toyworld.mx/orders

¡Gracias por comprar en ToyWorld! 🎉
╚══════════════════════════════════════════╝
    """)

def send_admin_alert(order_id: int, user_name: str, total: float, items_count: int):
    """Simula alerta al admin cuando hay un pedido nuevo."""
    print(f"""
╔══════════════════════════════════════════╗
🔔 ALERTA ADMIN — NUEVO PEDIDO
══════════════════════════════════════════
📦 Pedido #: {order_id}
👤 Cliente: {user_name}
🛒 Productos: {items_count}
💰 Total: ${total:.2f} MXN
📅 Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Accede al panel: localhost:5173/admin
╚══════════════════════════════════════════╝
    """)

def send_shipment_update(order_id: int, user_name: str, user_email: str, status: str, tracking: str = None):
    """Notifica al cliente sobre cambios en su envío."""
    status_msg = {
        "preparing": "🔧 Tu pedido está siendo preparado",
        "in_transit": "🚚 Tu pedido está en camino",
        "delivered": "✅ Tu pedido ha sido entregado",
    }.get(status, f"Estado actualizado: {status}")

    print(f"""
╔══════════════════════════════════════════╗
📧 ACTUALIZACIÓN DE ENVÍO → {user_email}
══════════════════════════════════════════
Hola {user_name},

{status_msg}

📦 Pedido: #{order_id}
{f"🔍 Tracking: {tracking}" if tracking else ""}
╚══════════════════════════════════════════╝
    """)
