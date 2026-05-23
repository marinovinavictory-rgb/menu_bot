import logging
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8760201795:AAFA9GbnUzo-yITqAVLbSTMPO3NLN5yB97A"

logging.basicConfig(level=logging.INFO)

MENU = {
    1:  {"name": "Суббота, день 1",     "b": "Овсянка на воде (150г) с яблоком и корицей + зелёный чай", "l": "Куриная грудка запечённая (150г) + гречка (100г) + огурец-помидор", "d": "Омлет из 2 яиц с овощами (перец, шпинат) + кефир 1% (200мл)"},
    2:  {"name": "Воскресенье, день 2", "b": "Творог 5% (150г) + горсть ягод + чай", "l": "Суп-пюре из брокколи (200мл) + ржаной хлеб + куриная котлета паровая (100г)", "d": "Рыба запечённая (треска/минтай, 150г) + тушёные кабачки с луком"},
    3:  {"name": "Понедельник, день 3", "b": "Яйцо варёное 2 шт + цельнозерновой тост + помидор + чай", "l": "Борщ на говядине (250мл) + гречка (80г) + салат из свежей капусты", "d": "Индейка тушёная (130г) + стручковая фасоль отварная (150г)"},
    4:  {"name": "Вторник, день 4",     "b": "Гречневая каша на воде (150г) + 1 ч.л. сливочного масла + чай", "l": "Тыквенный суп-пюре (250мл) + куриная грудка отварная (140г) + зелёный салат", "d": "Творожная запеканка без сахара (150г) + кефир (200мл)"},
    5:  {"name": "Среда, день 5",       "b": "Смузи: кефир (200мл) + банан (½) + шпинат + льняное семя 1 ч.л.", "l": "Говядина тушёная (130г) + бурый рис (80г) + тушёные овощи", "d": "Салат Нисуаз: тунец (100г) + яйцо + огурец + листовой салат + оливковое масло"},
    6:  {"name": "Четверг, день 6",     "b": "Блинчики из овсяных отрубей (2 шт) + натуральный йогурт + ягоды", "l": "Запечённый лосось (120г) + картофель варёный (100г) + огуречный салат", "d": "Куриный бульон (200мл) + паровые овощи (брокколи, цветная капуста, морковь)"},
    7:  {"name": "Пятница, день 7",     "b": "Овсянка (150г) с грушей и 1 ч.л. мёда + кофе без сахара с молоком", "l": "Куриные тефтели в томатном соусе (150г) + перловка (80г) + квашеная капуста", "d": "Рыбные котлеты паровые (130г) + стручковая фасоль + кефир (200мл)"},
    8:  {"name": "Суббота, день 8",     "b": "Омлет из 2 яиц с помидорами и зеленью + ржаной хлеб + чай", "l": "Чечевичный суп (250мл) + куриная грудка гриль (130г) + свежий огурец", "d": "Творог 2% (150г) с зеленью и огурцом + кефир (200мл)"},
    9:  {"name": "Воскресенье, день 9", "b": "Творог 5% (120г) + льняное масло 1 ч.л. + зелёное яблоко + чай", "l": "Минестроне (250мл) + хлебец ржаной + рыба запечённая (130г)", "d": "Говядина тушёная (120г) + тушёная капуста с морковью (150г)"},
    10: {"name": "Понедельник, день 10","b": "Каша пшённая с тыквой (150г) + чай с лимоном", "l": "Греческий салат + фета (30г) + куриная грудка отварная (130г) + хлебец", "d": "Запечённые кабачки с сыром (100г+20г) + паровая рыба (120г)"},
    11: {"name": "Вторник, день 11",    "b": "Яичница из 2 яиц со шпинатом + томатный сок (200мл)", "l": "Суп с фрикадельками из индейки (250мл) + гречка (80г) + салат из свёклы", "d": "Куриная грудка с лимоном и розмарином (150г) + брокколи на пару (150г)"},
    12: {"name": "Среда, день 12",      "b": "Натуральный йогурт 3% (200г) + орехи (10г) + ягоды + чай", "l": "Щи из свежей капусты (250мл) + картофель (1 шт) + телятина тушёная (120г)", "d": "Тунец в собственном соку (100г) + салат (листья, огурец, авокадо ¼)"},
    13: {"name": "Четверг, день 13",    "b": "Сырники без сахара (2 шт) + сметана 10% (1 ст.л.) + ягоды", "l": "Запечённая сёмга (120г) + бурый рис (80г) + тушёные овощи", "d": "Овощной суп-пюре (200мл) + отварное яйцо 1 шт + кефир"},
    14: {"name": "Пятница, день 14",    "b": "Гречневые блинчики (2 шт) + натуральный йогурт + фрукты", "l": "Куриный суп с вермишелью (250мл) + котлета паровая (130г) + огурец", "d": "Омлет белковый (3 белка + 1 желток) с грибами и луком + кефир (200мл)"},
    15: {"name": "Суббота, день 15",    "b": "Овсянка на воде (150г) с черникой и семенами чиа 1 ч.л. + чай", "l": "Куриное бедро без кожи (140г) + тушёные баклажаны с перцем + хлебец", "d": "Творог 2% (150г) + кефир (200мл) + огурец свежий"},
    16: {"name": "Воскресенье, день 16","b": "Яйцо пашот + цельнозерновой тост + авокадо (30г) + кофе", "l": "Рыбный суп (250мл) без картофеля + гречка (80г) + зелёный салат", "d": "Индейка запечённая с лимоном (140г) + стручковая фасоль на пару (150г)"},
    17: {"name": "Понедельник, день 17","b": "Смузи-боул: кефир (150мл) + банан (½) + клубника + овсяные хлопья (30г)", "l": "Говяжьи котлеты паровые (130г) + тушёная морковь + перловка (70г)", "d": "Минтай в томате запечённый (150г) + брокколи (150г) + кефир (200мл)"},
    18: {"name": "Вторник, день 18",    "b": "Творожная запеканка без сахара (150г) + груша + чай", "l": "Суп-пюре из чечевицы с куркумой (250мл) + куриная грудка (130г) + огурец", "d": "Салат: тунец (100г) + яйцо + огурец + листовой салат + оливковое масло 1 ч.л."},
    19: {"name": "Среда, день 19",      "b": "Омлет из 2 яиц с болгарским перцем и зеленью + ржаной хлеб + кофе", "l": "Куриный суп с овощами (250мл) без картошки + гречка (80г) + квашеная капуста", "d": "Кабачки фаршированные мясом индейки запечённые (150г) + зелёный чай"},
    20: {"name": "Четверг, день 20",    "b": "Ленивая овсянка: хлопья (50г) + кефир + ягоды + орехи (10г)", "l": "Запечённый лосось (120г) + шпинат тушёный с чесноком + бурый рис (70г)", "d": "Белковый омлет (3 белка) с грибами + кефир (200мл) + огурец"},
    21: {"name": "Пятница, день 21 - финал!","b": "Овсянка с яблоком и корицей (150г) + 2 ореха грецких + зелёный чай", "l": "Запечённая курица (150г) + гречка (80г) + свежие овощи на тарелке", "d": "Творог 5% (150г) + горсть ягод + кефир (200мл) — ты справилась!"},
}

TIPS = [
    "Пей 1.5-2 л воды в день. Начинай утро со стакана теплой воды.",
    "Последний прием пищи — не позже 19:00-19:30.",
    "Убрать: сахар, белый хлеб, алкоголь, сладкие напитки.",
    "Соль — до 4-5 г/день. Меньше соли = меньше отеков.",
    "Прогулки 30-40 мин в день значительно усилят результат.",
    "Кефир вечером снижает кортизол и улучшает сон.",
    "Взвешивайся раз в неделю, утром, натощак — не каждый день!",
]

def main_keyboard(day_num=None):
    buttons = []
    if day_num:
        buttons.append([InlineKeyboardButton(f"Сегодня (день {day_num})", callback_data=f"day_{day_num}")])
    buttons.append([InlineKeyboardButton("Выбрать день", callback_data="choose_week")])
    buttons.append([InlineKeyboardButton("Советы по питанию", callback_data="tips")])
    return InlineKeyboardMarkup(buttons)

def week_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Неделя 1 (дни 1-7)", callback_data="week_1"),
         InlineKeyboardButton("Неделя 2 (дни 8-14)", callback_data="week_2")],
        [InlineKeyboardButton("Неделя 3 (дни 15-21)", callback_data="week_3")],
        [InlineKeyboardButton("Назад", callback_data="back_main")],
    ])

def days_keyboard(week: int):
    start = (week - 1) * 7 + 1
    rows = []
    row = []
    for d in range(start, start + 7):
        row.append(InlineKeyboardButton(f"День {d}", callback_data=f"day_{d}"))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("Назад", callback_data="choose_week")])
    return InlineKeyboardMarkup(rows)

def meal_keyboard(day_num: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Завтрак", callback_data=f"meal_{day_num}_b"),
         InlineKeyboardButton("Обед", callback_data=f"meal_{day_num}_l"),
         InlineKeyboardButton("Ужин", callback_data=f"meal_{day_num}_d")],
        [InlineKeyboardButton("Все приемы сразу", callback_data=f"meal_{day_num}_all")],
        [InlineKeyboardButton("К неделям", callback_data="choose_week")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data["start_date"] = date.today()
    day_num = 1
    text = (
        "Привет! Я твой персональный бот питания на 21 день.\n\n"
        "Меню составлено специально для тебя:\n"
        "~1450 ккал в день\n"
        "Белок на завтрак и ужин\n"
        "Углеводы только на обед\n"
        "Без сахара и белого хлеба\n\n"
        "Выбери, что хочешь посмотреть:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard(day_num))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text("Выбери, что хочешь посмотреть:", reply_markup=main_keyboard(1))

    elif data == "choose_week":
        await query.edit_message_text("Выбери неделю:", reply_markup=week_keyboard())

    elif data.startswith("week_"):
        week = int(data.split("_")[1])
        await query.edit_message_text(f"Неделя {week} — выбери день:", reply_markup=days_keyboard(week))

    elif data.startswith("day_"):
        day_num = int(data.split("_")[1])
        day = MENU[day_num]
        text = f"День {day_num} — {day['name']}\n\nВыбери прием пищи:"
        await query.edit_message_text(text, reply_markup=meal_keyboard(day_num))

    elif data.startswith("meal_"):
        parts = data.split("_")
        day_num = int(parts[1])
        meal_type = parts[2]
        day = MENU[day_num]
        if meal_type == "b":
            text = f"Завтрак — {day['name']}\n\n{day['b']}"
        elif meal_type == "l":
            text = f"Обед — {day['name']}\n\n{day['l']}"
        elif meal_type == "d":
            text = f"Ужин — {day['name']}\n\n{day['d']}"
        else:
            text = (
                f"{day['name']}\n\n"
                f"ЗАВТРАК\n{day['b']}\n\n"
                f"ОБЕД\n{day['l']}\n\n"
                f"УЖИН\n{day['d']}"
            )
        back_week = (day_num - 1) // 7 + 1
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад к дню", callback_data=f"day_{day_num}")],
            [InlineKeyboardButton("Выбрать другой день", callback_data=f"week_{back_week}")],
        ])
        await query.edit_message_text(text, reply_markup=kb)

    elif data == "tips":
        text = "Правила питания на 21 день:\n\n" + "\n\n".join(TIPS)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="back_main")]])
        await query.edit_message_text(text, reply_markup=kb)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
