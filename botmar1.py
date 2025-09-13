import telebot
from telebot import types

TOKEN = '7648347976:AAEH-hh41WITe5A-ZnO_-1YAHxo94FfjHAE'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = -1002188920409

PRODUCTS = [
    {
        "id": 1,
        "name": "Навес за кв.м",
        "price": 45000,
        "photo": "https://avatars.mds.yandex.net/i?id=28e95770966f8fa59c4de3b0f8ed6875cd2e74dc-10811985-images-thumbs&n=13"
    },
    {
        "id": 1,
        "name": "Навес за кв.м",
        "price": 45000,
        "photo": "https://avatars.mds.yandex.net/i?id=39fa739c70c8de4bffb67bbe4d142c2109b51c9a-9094507-images-thumbs&n=13"
    },
    {
        "id": 2,
        "name": "Забор за п.м",
        "price": 45000,
        "photo": "https://avatars.mds.yandex.net/i?id=9289cf618c713aa68f21ba62f38437bddea2fc29-10113980-images-thumbs&n=13"
    },
    {
        "id": 3,
        "name": "Пергола за кв.м",
        "price": 65000,
        "photo": "https://avatars.mds.yandex.net/i?id=10e72737936cebb13f10dc09508d81b79795ef40-7753642-images-thumbs&n=13"
    },
    {
        "id": 4,
        "name": "Лавочка за шт",
        "price": 150000,
        "photo": "https://avatars.mds.yandex.net/i?id=56d3122ae1e54b1880ae49e0a9d0d7a11ba3caa3-7629177-images-thumbs&n=13"
    },
    {
        "id": 5,
        "name": "Урна за шт",
        "price": 35000,
        "photo": "https://avatars.mds.yandex.net/i?id=c13f54cfc0ed97ebb166cd76913d08af073473fc-4236663-images-thumbs&n=13"
    },
]

user_carts = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛍 Металлоцех", "🛒 Корзина")
    markup.add("📞 Связаться с нами")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в наш Металлоцех! 👋", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛍 Металлоцех")
def show_shop(message):
    for product in PRODUCTS:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Добавить в корзину 🛒", callback_data=f"add_{product['id']}"))
        bot.send_photo(
            message.chat.id,
            photo=product["photo"],
            caption=f"<b>{product['name']}</b>\nЦена: {product['price']}KZT",
            parse_mode='HTML',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart(call):
    user_id = call.from_user.id
    prod_id = int(call.data.split("_")[1])
    user_carts.setdefault(user_id, []).append(prod_id)
    bot.answer_callback_query(call.id, "Товар добавлен в корзину!")

@bot.message_handler(func=lambda m: m.text == "🛒 Корзина")
def show_cart(message):
    user_id = message.from_user.id
    cart = user_carts.get(user_id, [])
    if not cart:
        bot.send_message(message.chat.id, "🛒 Ваша корзина пуста.", reply_markup=main_menu())
        return

    total = 0
    text = "🛒 В корзине:\n"
    for pid in cart:
        prod = next((p for p in PRODUCTS if p["id"] == pid), None)
        if prod:
            text += f"• {prod['name']} - {prod['price']}KZT\n"
            total += prod['price']
    text += f"\n💰 Итого: <b>{total}KZT</b>"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔙 Назад", "✅ Оформить заказ")
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔙 Назад")
def go_back(message):
    bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "✅ Оформить заказ")
def checkout(message):
    user_id = message.from_user.id
    username = message.from_user.username or "без username"
    cart = user_carts.get(user_id, [])
    
    if not cart:
        bot.send_message(message.chat.id, "🛒 Ваша корзина пуста.", reply_markup=main_menu())
        return

    total = 0
    order_details = "🛍 Новый заказ:\n"
    for pid in cart:
        prod = next((p for p in PRODUCTS if p["id"] == pid), None)
        if prod:
            order_details += f"• {prod['name']} - {prod['price']}KZT\n"
            total += prod['price']
    order_details += f"\n💰 Итого: {total}KZT"
    order_details += f"\n👤 Пользователь: @{username} (ID: {user_id})"

    bot.send_message(message.chat.id, f"✅ Ваш заказ на сумму {total}KZT оформлен! Если менеджер не отвечает, нажмите связаться с нами 👇", reply_markup=main_menu())

    bot.send_message(ADMIN_ID, order_details)

    user_carts[user_id] = []

@bot.message_handler(func=lambda m: m.text == "📞 Связаться с нами")
def contact(message):
    bot.send_message(
        message.chat.id,
        "📲 Контакты:\n"
        "🟢 WhatsApp: https://wa.me/77064205588\n"
        "📞 Позвонить:👉🏽+77064205588👈🏽",
        reply_markup=main_menu()
    )

bot.polling()