import telebot
from telebot import types
import time
import random as rn

from telegram._poll import Poll
import matplotlib.pyplot as plt
import sqlite3

bot = telebot.TeleBot("token")
n = 0
k = 0
# ограничения для тестов
num_no_machine = ""
num_no_tepl = ""
num_no_el = ""
num_no_kvants = ""
# для графика
people_short_otzv_1 = 0
people_short_otzv_2 = 0
people_short_otzv_3 = 0
people_short_otzv_4 = 0
podr_otz = []

####################################################################################
##      КОМАНДЫ АДМИНА:                                                           ##
##                                                                                ##
##      1) /statistik - построение гистограммы коротких отзывов                   ##
##      2) /read - чтение подробных отзывов                                       ##
##      3) /delete_data - удаление баз данных пользователей                       ##
##      4) /delete_all_no_num - удаление из базы всех данных пользователей тестов ##
##      5) /delete_admin_no_num                                                   ##
##      6) /delete_podr_otz - удаление ВСЕХ подробных отзывов из базы             ##
##      7) /delete_admin_short_otz - удаление короткого отзыва из базы            ##
####################################################################################

try:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        q = open("hello_sticker.webp", "rb")
        bot.send_sticker(message.chat.id, q)

        # создание кнопочек
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        item1 = types.KeyboardButton("⚙️Механические явления⚙️")
        item2 = types.KeyboardButton("🌡Тепловые явления🌡")
        item3 = types.KeyboardButton("⚡️Электромагнитные явления⚡️")
        item4 = types.KeyboardButton("☢️Квантовые явления☢️")
        item5 = types.KeyboardButton("📜Справочный материал📜")
        item6 = types.KeyboardButton("📝Тесты📝")
        item7 = types.KeyboardButton("🗂Оставить отзыв🗂")
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        bot.send_message(message.chat.id, "Выберете интересующий вас раздел физики =)", reply_markup=markup)


        # создание базы данных для тестов
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_users(
            id INTEGER,
            n INTEGER,
            k INTEGER
        )""")
        connect.commit()

        # создание базы данных для коротких ответов опроса
        cursor.execute("""CREATE TABLE IF NOT EXISTS short_otz(
                                id INTEGER,
                                people_short_otzv_1 INTEGER,
                                people_short_otzv_2 INTEGER,
                                people_short_otzv_3 INTEGER,
                                people_short_otzv_4 INTEGER
                            )""")
        connect.commit()

        # создание базы данных для тестов - улучшение
        cursor.execute("""CREATE TABLE IF NOT EXISTS tests_no_num(
                                            id INTEGER,
                                            num_no_machine TEXT,
                                            num_no_tepl TEXT,
                                            num_no_el TEXT,
                                            num_no_kvants TEXT
                                        )""")
        connect.commit()


        people_id = message.chat.id
        cursor.execute(f"SELECT id FROM telegram_users WHERE id = {people_id}")
        data1 = cursor.fetchone()
        global n, k
        global num_no_machine, num_no_tepl, num_no_el, num_no_kvants
        if data1 is None:
            # добавление данных
            users = [message.chat.id, n, k]
            cursor.execute("INSERT INTO telegram_users VALUES(?,?,?);", users)
            connect.commit()

        cursor.execute(f"SELECT id FROM short_otz WHERE id = {people_id}")
        data2 = cursor.fetchone()
        if data2 is None:
            data_short_otz = [message.chat.id, people_short_otzv_1, people_short_otzv_2, people_short_otzv_3, people_short_otzv_4]
            cursor.execute("INSERT INTO short_otz VALUES(?,?,?,?,?);", data_short_otz)
            connect.commit()

        cursor.execute(f"SELECT id FROM tests_no_num WHERE id = {people_id}")
        data3 = cursor.fetchone()
        if data3 is None:
            data_tests_no_num = [message.chat.id, num_no_machine, num_no_tepl, num_no_el, num_no_kvants]
            cursor.execute("INSERT INTO tests_no_num VALUES(?,?,?,?,?);", data_tests_no_num)
            connect.commit()


    # очистка баз данных: админ
    @bot.message_handler(commands=['delete_data'])
    def delete_data(message):
        if message.chat.id == 847195722:
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"DELETE FROM telegram_users WHERE id")
            connect.commit()
            bot.send_message(message.chat.id, "Данные пользователей из базы успешно удалены!")
        else:
            bot.send_message(message.chat.id, "Вы не админ!")

    @bot.message_handler(commands=['delete_all_no_num'])
    def delete_num_no_all(message):
        if message.chat.id == 847195722:
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"DELETE FROM tests_no_num WHERE id")
            connect.commit()
            bot.send_message(message.chat.id, "Данные пользователей из базы успешно удалены!")
        else:
            bot.send_message(message.chat.id, "Вы не админ!")

    @bot.message_handler(commands=['delete_admin_no_num'])
    def delete_admin_no_num(message):
        if message.chat.id == 847195722:
            admin = message.chat.id
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"DELETE FROM tests_no_num WHERE id = {admin}")
            connect.commit()
            bot.send_message(message.chat.id, "Данные админа из базы успешно удалены!")
        else:
            bot.send_message(message.chat.id, "Вы не админ!")

    @bot.message_handler(commands=['delete_podr_otz'])
    def delete_podr_otz(message):
        if message.chat.id == 847195722:
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"DELETE FROM podr_otz")
            connect.commit()
            bot.send_message(message.chat.id, "Данные из базы успешно удалены!")
        else:
            bot.send_message(message.chat.id, "Вы не админ!")

    @bot.message_handler(commands=['delete_admin_short_otz'])
    def delete_short_otz(message):
        if message.chat.id == 847195722:
            admin = message.chat.id
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"DELETE FROM short_otz WHERE id={admin}")
            connect.commit()
            bot.send_message(message.chat.id, "Данные админа из базы успешно удалены!")
        else:
            bot.send_message(message.chat.id, "Вы не админ!")

    def machine(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Кинематика")
        item2 = types.KeyboardButton("Динамика")
        item3 = types.KeyboardButton("Механическая энергия")
        item4 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4)
        bot.reply_to(message, "Кинематика или Динамика?", reply_markup=markup)


    def first_zakon_nutona(message):
        bot.send_message(message.chat.id,
                         "Существуют системы отсчёта, называемые инерциальными, относительно которых тело движется прямолинейно и равномерно, если на него не действуют другие дела. ")


    def second_zakon_nutona(message):
        bot.send_message(message.chat.id,
                         "Ускорение тела прямо пропорционально силе, действующей на него, и обратно пропорционально его массе: a = F/m")
        z2 = open("фото для проекта/img_1.png", "rb")
        bot.send_photo(message.chat.id, z2)


    def third_zakon_nutona(message):
        bot.reply_to(message,
                     "Силы с которыми тела действуют друг на друга, равны по модулю и направлены по одной прямой в противоположные стороны: F(1тела) = -F(2тела)")
        z3 = open("фото для проекта/img_2.png", "rb")
        bot.send_photo(message.chat.id, z3)


    def force_in_wild(message):
        bot.reply_to(message,
                     """
    📍Интересно: интенсивность сильного и слабого взаимодействий измеряется в единицах энергии (в электрон-вольтах), а не в единицах силы, и потому применение к ним термина 'сила' объясняется многовековой традицией все явления в окружающем мире объяснять действием характерных для каждого явления 'сил'."
    📍В механике обычно имеют дело с тремя видами сил - силами тяготения, силами упругости и силами трения.
                     """)
        v = open("фото для проекта/img_11.png", "rb")
        bot.send_photo(message.chat.id, v)


    def deformation_and_force_uprugosti(message):
        bot.reply_to(message, "Деформация - изменение формы или объёма тела.")
        v = open("фото для проекта/img_12.png", "rb")
        v1 = open("фото для проекта/img_13.png", "rb")
        bot.send_photo(message.chat.id, v)
        bot.send_photo(message.chat.id, v1)


    def zakon_Guka(message):
        v = open("фото для проекта/img_14.png", "rb")
        bot.send_photo(message.chat.id, v)


    def zakon_world_mg(message):
        bot.send_message(message.chat.id, "Закон всемирного тяготения был установлен Ньютоном, и он утверждает, что тела притягиваются друг к другу с силой, модуль которой\
        прямо пропорционален произведению их масс и обратно пропорционален квадрату расстояния между ними.")
        mg = open("фото для проекта/закон всемирного тяготения.jpg", "rb")
        bot.send_photo(message.chat.id, mg)


    def mv(message):
        bot.send_message(message.chat.id,
                         "Величину, равную произведению массы тела и его скорости, называют импульсом тела.")
        mvv = open("фото для проекта/импульс тела.jpg", "rb")
        bot.send_photo(message.chat.id, mvv)


    def zakon_save_mv(message):
        bot.send_message(message.chat.id,
                         "Геометрическая сумма импульсов тел, входящих в замкнутую систему, остаётся постоянной при любых взаимодействиях тел этой системы между собой.")
        zmv = open("фото для проекта/закон сохранения импульса тела.jpg", "rb")
        bot.send_photo(message.chat.id, zmv)


    def mechine_A_N(message):
        bot.send_message(message.chat.id,
                         """
1) Механическая работа - это физическая величина, равная произведению вектора силы, действующей на тело, и вектора его перемещения.
2) Если сила, действующая на тело, состоявляет некоторый угол (альфа) с перемещением, то работа постоянной силы равна произведению\
модулей векторов силы и перемещения и косинуса угла между этими векторами.
3) Мощностью называется физическая величина, равная отношению работы к промежутку времени, за который она совершена. Мощность характеризует быстроту совершения работы.
                         """)
        ma = open("фото для проекта/работа.jpeg", "rb")
        bot.send_photo(message.chat.id, ma)
        mn = open("фото для проекта/мощность.jpg", "rb")
        bot.send_photo(message.chat.id, mn)


    def KPD(message):
        bot.send_message(message.chat.id,
                         "КПД - это скалярная физическая величина, численно равная отношению полезной работы к затраченной в системе.")
        kpd = open("фото для проекта/кпд.jpeg", "rb")
        bot.send_photo(message.chat.id, kpd)


    def pressure(message):
        bot.send_message(message.chat.id,
                         "Давление - это физическая величина, равная отношению силы давления F к площади поверхности S.")
        prs = open("фото для проекта/давление.jpg", "rb")
        bot.send_photo(message.chat.id, prs)
        prs_water = open("фото для проекта/давление_жидкость.jpg", "rb")
        bot.send_photo(message.chat.id, prs_water)


    def pascal(message):
        bot.send_message(message.chat.id,
                         "Давление, производимое на жидкость или газ, передаётся по всем направлениям без изменения в каждую точку жидкости или газа.")
        pascal1 = open("фото для проекта/паскаль1.jpg", "rb")
        bot.send_photo(message.chat.id, pascal1)
        pascal2 = open("фото для проекта/паскаль 2.jpeg", "rb")
        bot.send_photo(message.chat.id, pascal2)


    def archimed(message):
        bot.send_message(message.chat.id, "Сила Архимеда - это сила, стремящееся вытянуть тело из воды.")
        ar = open("фото для проекта/закон архимеда.jpg", "rb")
        bot.send_photo(message.chat.id, ar)


    def kolebania_and_volns(message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        item0 = types.InlineKeyboardButton(text="Подроднее",
                                           url="https://fizi4ka.ru/egje-2018-po-fizike/mehanicheskie-kolebanija-i-volny-2.html")
        markup.add(item0)
        bot.reply_to(message, "Перейди по ссылке, если хочешь узнать больше.", reply_markup=markup)
        k_l = open("фото для проекта/колебаия и волны.gif", "rb")
        bot.send_photo(message.chat.id, k_l)


    def dinamika(message):
        bot.reply_to(message, "Раздел механики, изучающий причины изменения механического движения.")
        d = open("фото для проекта/img_5.png", 'rb')
        bot.send_photo(message.chat.id, d)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Первый закон Ньютона")
        item2 = types.KeyboardButton("Второй закон Ньютона")
        item3 = types.KeyboardButton("Третий закон Ньютона")
        item4 = types.KeyboardButton("Силы в природе")
        item5 = types.KeyboardButton("Деформация и сила упругости")
        item6 = types.KeyboardButton("Закон Гука")
        item7 = types.KeyboardButton("Закон всемирного тяготения")
        item8 = types.KeyboardButton("Импульс тела")
        item9 = types.KeyboardButton("Закон сохранения импульса")
        item10 = types.KeyboardButton("Механическая работа и мощность")
        item11 = types.KeyboardButton("КПД")
        item12 = types.KeyboardButton("Давление")
        item13 = types.KeyboardButton("Закон Паскаля")
        item14 = types.KeyboardButton("Закон Архимеда")
        item15 = types.KeyboardButton("Механические колебания и волны")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                   item14, item15, item0)
        bot.reply_to(message, "Темы:", reply_markup=markup)


    def energy(message):
        bot.reply_to(message,
                     "Энергия - это физическая величина, которая характерезует способность тела (или системы тел) соверать работу.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Потенциальная энергия")
        item2 = types.KeyboardButton("Кинетическая энергия")
        item3 = types.KeyboardButton("Теорема об изменении потенциальной энергии")
        item4 = types.KeyboardButton("Теорема об изменении кинетической энергии")
        item5 = types.KeyboardButton("Закон сохранения механической энергии")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item0)
        bot.reply_to(message, "Темы:", reply_markup=markup)


    def poten_energy(message):
        bot.reply_to(message,
                     "Потенциальная энергия - это энергия взаимодействия тел, обусловленная их взаимным расположением или взаимным расположением частей тела.")
        e = open("фото для проекта/slide-17.jpg", "rb")
        e1 = open("фото для проекта/упр-деф-потен-энрг.jpeg", "rb")
        bot.send_photo(message.chat.id, e)
        bot.send_photo(message.chat.id, e1)


    def kinet_energy(message):
        bot.reply_to(message, "Кинетическая энергия - это энергия, которой обладает движущееся тело.")
        e = open("фото для проекта/формула.jpg", "rb")
        bot.send_photo(message.chat.id, e)


    def teorema_poten_energy(message):
        e = open("фото для проекта/потен-энерги.jpg", "rb")
        bot.send_photo(message.chat.id, e)


    def teorema_kinet_energy(message):
        e = open("фото для проекта/теорема_кинет_энергии.png", "rb")
        bot.send_photo(message.chat.id, e)


    def zakon_save_energy(message):
        bot.send_message(message.chat.id, "В замкнутой системе с консервативными силами полная энергия сохраняется.")
        bot.send_message(message.chat.id,
                         "Консервативные силы - это силы, абота которых по замкнотому контуру равна нулю; например, сила тяжести, сила упругости.")
        e = open("фото для проекта/законсохранеияэнергии.jpeg", "rb")
        bot.send_photo(message.chat.id, e)


    def exit_to_menu(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("⚙️Механические явления⚙️")
        item2 = types.KeyboardButton("🌡Тепловые явления🌡")
        item3 = types.KeyboardButton("⚡️Электромагнитные явления⚡️")
        item4 = types.KeyboardButton("☢️Квантовые явления☢️")
        item5 = types.KeyboardButton("📜Справочный материал📜")
        item6 = types.KeyboardButton("📝Тесты📝")
        item7 = types.KeyboardButton("🗂Оставить отзыв🗂")
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        bot.reply_to(message, "Разделы:", reply_markup=markup)


    def kinematka(message):
        bot.reply_to(message,
                     "Раздел механики, изучающий способы описания движений и связь между величинами, характерезующими эти движения.")
        k = open("фото для проекта/img_3.png", 'rb')
        bot.send_photo(message.chat.id, k)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Равномерное движение")
        item2 = types.KeyboardButton("Равноускоренное/Равнозамедленное движение")
        item3 = types.KeyboardButton("Поступательное движение")
        item4 = types.KeyboardButton("Вращательное движение")
        item5 = types.KeyboardButton("Движение с постоянным ускорением свободного падения")
        item6 = types.KeyboardButton("Мгновенная и средняя скорости")
        item7 = types.KeyboardButton("Сложение скоростей")
        item8 = types.KeyboardButton("Ускорение")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item0)
        bot.reply_to(message, "Темы:", reply_markup=markup)


    def ravnomernoe_dvj(message):
        bot.reply_to(message,
                     "Движение точки называется равномерным, если она за любые равные промежутки времени проходит одинаковые пути.")
        p1 = open("фото для проекта/img_4.png", "rb")
        bot.send_photo(message.chat.id, p1)


    def ravn_uscor_and_zamedl_dvj(message):
        bot.reply_to(message,
                     "Движение вдоль прямой с постоянным ускорением, при котором модуль скорости увеличивается, называется прямолинейным равноускоренным движением, а прямолинейное  движение с постоянным ускорением, при котором модуль скорости уменьшается, называется равнозамедленным.")
        p2 = open("фото для проекта/img_4.png", "rb")
        bot.send_photo(message.chat.id, p2)


    def postupatelnoe_dvj(message):
        bot.reply_to(message,
                     "Поступательным называется такое движение абсолютно твёрдого тела, при котором любой отрезок, соединяющий любые две точки тела, остаётся параллейным самому себе.")
        a_scor = open("фото для проекта/img_6.png", "rb")
        bot.send_photo(message.chat.id, a_scor)


    def rotational_motion(message):
        bot.reply_to(message,
                     "Вращательным движением абсолютно твёрдого тела вокруг неподвижной оси называется такое его движение, при котором все точки тела описывают окружности, центры которых находятся на одной прямой, называемой осью вращения, при этом плоскости, которым принадлежат эти окружности, перпендикулярны оси вращения.")
        v = open("фото для проекта/img.png", "rb")
        bot.send_photo(message.chat.id, v)


    def svobodnoe_padenie(message):
        bot.reply_to(message,
                     "Закон независимости движений: всякое сложное движение можно представить как сумму движений по двум независимым координатам.")
        v = open("фото для проекта/img_7.png", "rb")
        bot.send_photo(message.chat.id, v)


    def slojenie_scorostey(message):
        bot.reply_to(message,
                     "Закон сложения скоростей: если тело движется относительно некоторой системы координат К1 со скоростью v и сама система К1 движется относительно другой системы координат К2 со скоростью v1, то скорость тела относительно второй системы равна геометрической сумме скоростей v1 и v.")
        v = open("фото для проекта/img_9.png", "rb")
        bot.send_photo(message.chat.id, v)


    def mgn_and_sr_scorosti(message):
        v = open("фото для проекта/img_8.png", "rb")
        bot.send_photo(message.chat.id, v)


    def a(message):
        bot.reply_to(message, "Физическая величина, характеризующая быстроту измения скорости.")
        v = open("фото для проекта/img_10.png", "rb")
        bot.send_photo(message.chat.id, v)


    # тепловые явления
    def teplo(message):
        bot.send_message(message.chat.id, "Тепловые явления - это физические процессы, протекающие в телах при их нагревании или охлаждении. К таким явлениям относятся, например, процессы нагревания и охлаждения тел, превращения вещества из твёрдого состояния\
в жидкое и газообразное.")
        t = open("фото для проекта/тепловые явления.jpg", "rb")
        bot.send_photo(message.chat.id, t)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("Строение вещества")
        item2 = types.KeyboardButton("Тепловое движение атомов и молекул")
        item3 = types.KeyboardButton("Внутренняя энергия")
        item4 = types.KeyboardButton("Виды теплопередачи")
        item5 = types.KeyboardButton("Количество теплоты")
        item6 = types.KeyboardButton("Тепловые двигатели")
        item7 = types.KeyboardButton("Испарение и конденсация")
        item8 = types.KeyboardButton("Плавление и кристаллизация")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item0)
        bot.reply_to(message, "Темы:", reply_markup=markup)


    def stroenie_substance(message):
        bot.send_message(message.chat.id,
                         """
📍Положение 1. 
Все вещетсва состоят из частиц, между которыми есть промежутки.
📍Положение 2.
Молекулы находятся в непрерывном беспорядочном (хаотическом) движении.
📍Положение 3.
Молекулы взаимодействуют между собой, между ними действуют силы и притяжния и отталкивания.

📍Атом - наименьшая частица вещества, не делящаяся при химических реакциях.
📍Молекула - наименьшая частица вещества, которая сохраняет его химические свойства.
                         """)
        s = open("фото для проекта/строение вещества.png", "rb")
        bot.send_photo(message.chat.id, s)


    def tepl_dv_atoms_and_mol(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="Броуновское движение", callback_data="броун")
        item2 = types.InlineKeyboardButton(text="Диффузия", callback_data="диффузия")
        item3 = types.InlineKeyboardButton(text="Тепловое равновесие", callback_data="тепловое_равновесие")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Тепловое движение - это непрерывное хаотического движение атомов и молекул.",
                         reply_markup=markup)
        bot.send_message(message.chat.id,
                         "Связь температуры со скоростью хаотического движения частиц заключается в том, что чем больше скорость частиц, тем выше температура, и наоборот.")


    def vn_energy(message):
        bot.send_message(message.chat.id,
                         """
1) Внутренней энерией тела называют сумму кинетической энергии движения его молекул и потенциальной энергии их взаимодействия.
2) Если тело само совершает работу, то его внутренняя энергия уменьшается, а если над ним совершают работу, то его внутренняя энергия увеличивается.
                         """)


    def teploperedachi(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="Теплопроводность", callback_data="теплопроводность")
        item2 = types.InlineKeyboardButton(text="Конвекция", callback_data="конвекция")
        item3 = types.InlineKeyboardButton(text="Излучение", callback_data="излучение")
        markup.add(item1, item2, item3)
        t0 = open("фото для проекта/теплопередача_виды.webp", "rb")
        bot.send_photo(message.chat.id, t0)
        bot.send_message(message.chat.id, "Виды теплопередачи:", reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: True)
    def check_callback_data(call):
        if call.data == "теплопроводность":
            bot.reply_to(call.message, text="Процесс передачи энергии от одного тела к другому или от одной части тела к другой благодаря\
тепловому движению частиц называется теплопроводностью.")
            t1 = open("фото для проекта/теплопроводность.jpg", "rb")
            bot.send_photo(call.message.chat.id, t1)

        elif call.data == "✅":
            try:
                connect = sqlite3.connect('data_telegram.db')
                cursor = connect.cursor()
                people_user_id = call.message.chat.id
                cursor.execute(f"""SELECT k FROM telegram_users WHERE id = {people_user_id}""")
                k_data = cursor.fetchone()
                k = int(k_data[0]) + 1
                cursor.execute(f"""Update telegram_users set k = {k} where id = {people_user_id}""")
                connect.commit()
                test_after_true_answer(call.message)
            except:
                pass


        elif call.data == "тесты":
            tests(call.message)

        elif call.data == "конвекция":
            bot.reply_to(call.message,
                         text="Конвекция - это вид теплопередачи, при котором энергия передаётся слоями жидкости или газа.")
            t2 = open("фото для проекта/конвекция.jpeg", "rb")
            bot.send_photo(call.message.chat.id, t2)

        elif call.data == "излучение":
            bot.reply_to(call.message, text="Излучение - это вид теплопередачи, при котором испускание и распространение энергии происходит\
            при помощи электромагнитных волн и элементарных частиц.")
            t3 = open("фото для проекта/излучение.jpg", "rb")
            bot.send_photo(call.message.chat.id, t3)

        elif call.data == "броун":
            b = open("фото для проекта/броун.jpg", "rb")
            bot.send_photo(call.message.chat.id, b)

        elif call.data == "диффузия":
            bot.reply_to(call.message,
                         text="Диффузией называется явление проникновения молекул одного вещества в промежутки между молекулами другого вещества.")
            d = open("фото для проекта/диффузия.jpeg", "rb")
            bot.send_photo(call.message.chat.id, d)

        elif call.data == "тепловое_равновесие":
            t = open("фото для проекта/тепловое равновесие.jpg", "rb")
            bot.send_photo(call.message.chat.id, t)

        elif call.data == "сила тока":
            bot.reply_to(call.message, text="Силой тока называют физическую величину, равную отношению заряда q, проходящего\
через поперечное сечение проводника за промежуток времени t, к этому промежутку времени.")
            i = open("фото для проекта/сила тока.jpeg", "rb")
            bot.send_photo(call.message.chat.id, i)

        elif call.data == "напряжение":
            bot.reply_to(call.message, text="Характеристикой источника тока служит величина, называемая напряжением.\
Напряжением U называют физическую величину, равную отношению работы (A) электрического поля по перемещению\
электрического заряда к заряду (q).")
            u = open("фото для проекта/напряжение.jpg", "rb")
            bot.send_photo(call.message.chat.id, u)

        elif call.data == "сопротивление":
            bot.reply_to(call.message, text="Сопротивлением проводника (R) называют физическую величину, равную отношению напряжения (U)\
на концах проводника к силе тока (I) в нём.")
            r1 = open("фото для проекта/сопротивление2.jpg", "rb")
            bot.send_photo(call.message.chat.id, r1)
            r2 = open("фото для проекта/сопротивление1.jpg", "rb")
            bot.send_photo(call.message.chat.id, r2)

        elif call.data == "буравчик":
            bot.reply_to(call.message, text="Правило буравчика: если направление поступательного движения буравчика совпадает с направлением тока в проводнике,\
то направление вращения ручки буравчика совпадает с ноправлением линий магнитной индукции.")
            b = open("фото для проекта/буравчик.jpg", "rb")
            bot.send_photo(call.message.chat.id, b)

        elif call.data == "правая рука":
            bot.send_message(call.message.chat.id, "Правило правой руки:")
            p = open("фото для проекта/правло правой руки.jpg", "rb")
            bot.send_photo(call.message.chat.id, p)

        elif call.data == "левая рука":
            bot.reply_to(call.message, text=
            """
Правило левой руки формулируется так: четыре пальца на левой руке располагаются в направлении, куда движутся положительные или 
отрицательные частицы электрического тока. Индукционные линии, как и в других случаях, должны перпендикулярно располагаться относительно ладони и 
входить в нее. Большой оттопыренный палец указывает на направление силы Ампера или Лоренца.
""")
            lr = open("фото для проекта/правило левой руки.jpg", "rb")
            bot.send_photo(call.message.chat.id, lr)

        elif call.data == "ампер":
            bot.reply_to(call.message, text=
            """
⚡️На проводник с током, помещённый в магнитное поле, действует сила, которую называют силой Ампера.
⚡️Формула силы Ампера позволяет раскрыть смысл понтия вектора магнитной индукции: 
Магнитной идукцией называется физическая величина, равная отношению силы, действующей на проводник с током в магнитном поле,\
к силе тока и длине проводника, находящейся в магнитном поле.
⚡️За единицу магнитной индукции принимают магнитную индукцию такого поля, в котором на проводник длиной 1 м действует сила 1 Н при силе тока в проводнике 1 А.
            """)
            amper = open("фото для проекта/ампер.jpg", "rb")
            bot.send_photo(call.message.chat.id, amper)

        elif call.data == "лоренц":
            bot.reply_to(call.message,
                         text="Сила, с которой электромагнитрое поле действует на точечную заряженную частицу.")
            l = open("фото для проекта/лоренц.jpg", "rb")
            bot.send_photo(call.message.chat.id, l)

        elif call.data == "магниты":
            bot.reply_to(call.message,
                         text="Тела, длительное время сохраняющие магнтные свойства, или намагниченность, называют постоянными магнитами.")


    def coll_teplots(message):
        bot.send_message(message.chat.id,
                         """
📍Изменение внутреней энергии тела при теплопередаче характерезуется величиной, называемой количеством теплоты.
📍Зависимость количества теплоты, необходимо для нагревания тела, от рода вещества характерезуется физической величиной, называемой удельной теплоёмкостью вещества.    
📍Физическая величина, равная количеству теплоты, которое необходимо сообщить 1 кг вещества для нагревания его на 1°С (или на 1 К), называется удельной теплоёмкостью вещества.
                         """)
        c = open("фото для проекта/нагрев.jpg", "rb")
        bot.send_photo(message.chat.id, c)


    def tepl_dvigatel(message):
        bot.send_message(message.chat.id,
                         "Устройства, совершающие механическую работу за счёт внутренней энергии топлива, называются тепловыми двигателями.")
        dv = open("фото для проекта/тепловые машины.jpg", "rb")
        bot.send_photo(message.chat.id, dv)


    def evaporation_condensation(message):
        bot.send_message(message.chat.id,
                         """
🎯Явление превращения вещества из жидкого состояния в газообразное называется парообразованием.
🎯Испарением называется процесс превращения вещества из жидкого состояния в газообразное, происходящий с поверхности жидкости при любой температуре.
🎯Процесс превращения вещества из газообразного состояния в жидкое называется конденсацией.
🎯Пар, образующийся над жидкостью, называется ненасыщенным.
🎯Если жидкость находится в закрытом сосуде, то в начале число молекул, вылетающих из жидкости, будет больше, чем число молекул,\
возвращающихся в неё, но с течением времени плотность пара над жидкостью возрастёт настолько, что число молекул, покидающих жидкость,\
станет равным числу молекул, возвращающихся в неё. В этом случае наступает динамическое равновесие жидкости с её паром.
🎯Пар, находящийся в состоянии динамического равновесия со своей жидкостью, называется насыщенным паром.
🎯Температуру, при которой водяной пар, содержащийся в воздухе, становится насященным, называют точкой росы.
🎯Для измерения влажности воздуха используют прибор, называемый пихрометром.
🎯Кипение - это процесс парообразования, происходящий во всём объёме жидкости при определённой температуре. Температуру, при которой жидкость кипит, называют температурой кипения.
🎯Для превращения разных веществ из жидкого состояния в газообразное требуется разная энергия, эта энергия характерезуется величиной,\
называемой удельной теплотой парообразования.
🎯 Удельной теплотой парообразования (L) называют величину, равную отношению количества теплоты, которое нужно сообщить веществу массой 1 кг,\
для превращения его из жидкого состояния в газообразное при температуре кипения.
                         """)
        e1 = open("фото для проекта/испарение и конденсация.jpeg", "rb")
        e2 = open("фото для проекта/испарение и конденсация 2.jpeg", "rb")
        bot.send_photo(message.chat.id, e1)
        bot.send_photo(message.chat.id, e2)


    def melting_crystallization(message):
        bot.send_message(message.chat.id,
                         """
🚀Плавлением называется процесс превращения вещества из твёрдого состояния в жидкое.
🚀Температуру, при которой происходит плавление вещества, называют темппературой плавления.
🚀Процесс перехода вещества из жидкого состояния в твёрдое состояние называют кристаллизацией.
🚀Температуру, при которой происходит кристаллизация вещества, называют температурой кристаллизации.
🚀Количество теплоты, которое необходимо сообщить 1 кг кристаллического вещества, чтобы превратить его в жидкость при температуре плавления,\
называют удельной телотой плавления.
                         """)
        m1 = open("фото для проекта/плавление и кристаллизация 1.jpeg", "rb")
        m2 = open("фото для проекта/плавление и кристаллизация 2.jpeg", "rb")
        bot.send_photo(message.chat.id, m1)
        bot.send_photo(message.chat.id, m2)


    # электромагнитные явления
    def electromagnitizm(message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Электризация тел")
        item2 = types.KeyboardButton("Электрическое поле")
        item3 = types.KeyboardButton("Постоянный электрический ток")
        item4 = types.KeyboardButton("Последовательное и параллельное соединение проводников")
        item5 = types.KeyboardButton("Работа и мощность электрического тока")
        item6 = types.KeyboardButton("Закон Джоуля-Ленца")
        item7 = types.KeyboardButton("Опыт Эрстеда. Магнитное поле тока")
        item8 = types.KeyboardButton("Электромагнитная индукция")
        item9 = types.KeyboardButton("💡Световые явления💡")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item0)
        bot.send_message(message.chat.id, "Темы:", reply_markup=markup)


    def el_tel(message):
        bot.send_message(message.chat.id,
                         """
⚡️Тела, которые в результате трения приобретают способность притягивать другие тела, называют наэлектризованными или заряженными,\
а явление приобретния телами электрического заряда называют электризацией.
⚡️Одноимённые заряды, т.е заряды одного знака, отталкиваются друг от друга, а разноимённые притягиваются друг к другу.
⚡️[q] = 1 Кл (заряд, а за единицу заряда принят 1 кулон)
                         """)
        el = open("фото для проекта/закон сохранения электрического заряда.jpeg", "rb")
        bot.send_photo(message.chat.id, el)


    def el_pole(message):
        bot.send_message(message.chat.id,
                         """
⚡️Согласно утверждению английских учёныых М. Фарадея и Д. Максвелла, в пространстве, в котором находится заряженно тело,\
существует электрическое поле. Посредством этого поля одно заряженное тело действует на другое.
⚡️Силу, с которой поле действует на внесённый в него электрический заряд, называют электрической силой. 
                         """)
        el = open("фото для проекта/провода.jpg", "rb")
        bot.send_photo(message.chat.id, el)


    def poston_tok(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="Сила тока", callback_data="сила тока")
        item2 = types.InlineKeyboardButton(text="Напряжение", callback_data="напряжение")
        item3 = types.InlineKeyboardButton(text="Электрическое сопротивление", callback_data="сопротивление")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Электрическим током называют упорядоченное движение заряженных частиц.",
                         reply_markup=markup)


    def zakon_oma(message):
        bot.send_message(message.chat.id, "Закон Ома: сила тока на участке цепи прямо пропорциональна напряжению на концах этого участка\
и обратно пропорциональна его сопротивлению.")
        z_o = open("фото для проекта/закон ома.jpeg", "rb")
        bot.send_photo(message.chat.id, z_o)


    def connection(message):
        c = open("фото для проекта/соединение.jpg", "rb")
        bot.send_photo(message.chat.id, c)


    def A_and_N_el_toka(message):
        bot.send_message(message.chat.id,
                         """
⚡️Работа электрического тока на участке цепи равна произведению напряжения на этом участке, силы тока и времени, в течение которого совершается работа.
⚡️Единицей работы является джоуль (1 Дж)
⚡️Мощность электрического тока равна произведению напряжения и силы тока в цепи
⚡️Единицей мощности является ватт (1 Вт)
                         """)
        q = open("фото для проекта/работа и мощность.png", "rb")
        bot.send_photo(message.chat.id, q)


    def zakon_Djol_lenz(message):
        bot.send_message(message.chat.id, "Количество теплоты, выделяющееся при прохождении тока по проводнику,\
равно произведению квадрата силы тока, сопротивления проводника и времени.")
        q = open("фото для проекта/джоуль-ленц.jpg", "rb")
        bot.send_photo(message.chat.id, q)


    def opt_ersteda(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="Правило буравчика", callback_data="буравчик")
        item2 = types.InlineKeyboardButton(text="Сила Ампера", callback_data="ампер")
        item3 = types.InlineKeyboardButton(text="Сила Лоренца", callback_data="лоренц")
        item4 = types.InlineKeyboardButton(text="Правило левой руки", callback_data="левая рука")
        item5 = types.InlineKeyboardButton(text="Правило правой руки", callback_data="правая рука")
        item6 = types.InlineKeyboardButton(text="Магниты", callback_data="магниты")
        markup.add(item1, item2, item3, item4, item5, item6)
        ersted = types.InlineKeyboardMarkup(row_width=1)
        item0 = types.InlineKeyboardButton(text="Видео опыта Эрстеда",
                                           url="https://yandex.ru/video/preview/3838845277258400825")
        ersted.add(item0)
        bot.send_message(message.chat.id,
                         """
1)Опыт Эрстеда показал существование взаимосвязи между электрическими и магнитными явлениями.
2)Силовой характеристикой магнитного поля является величина, называемая магнитной индукцией.                    
                         """, reply_markup=ersted)
        opt = open("фото для проекта/опыт эрстеда.jpg", "rb")
        bot.send_photo(message.chat.id, opt)
        bot.send_message(message.chat.id, "Подтемы:", reply_markup=markup)


    def el_induction(message):
        faradey = types.InlineKeyboardMarkup(row_width=1)
        item0 = types.InlineKeyboardButton(text="Видео опыта Фарадея",
                                           url="https://yandex.ru/video/preview/1109460983505475854")
        faradey.add(item0)
        bot.send_message(message.chat.id,
                         """
⚡️Явление возникновения тока в замкнутом проводнике при изменении магнитного поля, пронизывающего контур проводника, называется электромагнитной индукций.
⚡️Ток, возникающий в этом случае в цепи, называют индукционным током.
⚡️Если в самом проводнике изменяется сила тока, то вокруг проводника существуют переменное магнитное поле. Это поле порождает в проводнике индукционный ток,\
который называется током самоиндукции, а явление возникновения такого тока - явление самоиндукции.
⚡️Значение открытия явления магнитной индукции заключается в том, что в этом явлении наглядно наблюдается связь электрических и магнитных явлений,\
электрического и магнитного полей, что позволяет говорить о существовании единого электромагнитного поля.
                         """, reply_markup=faradey)
        f = open("фото для проекта/фарадей.jpg", "rb")
        bot.send_photo(message.chat.id, f)


    def svet_evl(message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Закон прямолинейного распространения света")
        item2 = types.KeyboardButton("Закон отражения света")
        item3 = types.KeyboardButton("Плоское зеркало")
        item4 = types.KeyboardButton("Преломление света")
        item5 = types.KeyboardButton("Дисперсия света")
        item6 = types.KeyboardButton("Линзы")
        item7 = types.KeyboardButton("Фокусное расстояние линзы")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item0)

        # световые явления
        svet = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton(text="Световые явления",
                                          url="https://www.evkova.org/svetovyie-yavleniya-v-fizike")
        svet.add(item)
        bot.send_message(message.chat.id,
                         "Замечательный сайт, который расскажет и покажет на рисунках всё о световых явлениях в физике и в природе!",
                         reply_markup=svet)
        bot.send_message(message.chat.id, "Темы:", reply_markup=markup)


    def zakon_raspr_sveta(message):
        bot.send_message(message.chat.id,
                         """
💡Закон прямолинейного распространения света: в однородной среде свет распространяется прямолинейно.
💡Тоечный источник - это такой источник, размеры которого малы по сравнению с расстоянием от него до наблюдателя.
                         """)
        svet = open("фото для проекта/закон прямолинейного распространения света.jpg", "rb")
        bot.send_photo(message.chat.id, svet)


    def zakon_otr_sveta(message):
        bot.send_message(message.chat.id,
                         """
1) Угол отражения света равен углу падения.
2) Луи падающий и отражённый, а также перпендикуляр, восставленный к границе раздела двух сред, лежат в одной плоскости.
                         """)
        s = open("фото для проекта/закон отражения.jpg", "rb")
        bot.send_photo(message.chat.id, s)


    def ploskoe_zerkalo(message):
        bot.send_message(message.chat.id,
                         """
🪞Плоское зеркало даёт прямое изображение предмета.
🪞Изображение имеет те же размеры, что и предмет.
🪞Расстояние от предмета до зеркала равно расстоянию от зеркала до изображения.
🪞Изображение предмета в плоском зеркале является мнимым.
🪞Мнимое изображение - это такое изображение, которое формируется глазом.
                         """)
        pl = open("фото для проекта/плоское зеркало.jpg", "rb")
        bot.send_photo(message.chat.id, pl)


    def dispersia(message):
        bot.send_message(message.chat.id,
                         """
🌈Разложение света в спект объясняется тем, что световые пучки по-разному преломляются призмой: лучи красного цвета преломляются слабее,\
а лучи фиолетового цвета - сильнее. Зависимость угла преломления света в среде от цвета света (от длины световой волны) называется дисперсией света.
🌈Радуга - это спектр солнечного света. Он образуется ри разложении белого света в каплях дождя, которые можно рассмотривать как призмы.
                         """)
        d = open("фото для проекта/дисперсия.png", "rb")
        bot.send_photo(message.chat.id, d)


    def prelomlenie_sveta(message):
        bot.send_message(message.chat.id,
                         """
💡Изменение направления распространения света при переходе в другую среду называют преломлением света.
💡Лучи падающий и преломлённый, а также перпендикуляр, восставленный к границе раздела двух сред, лежат в одной плоскости.
                         """)
        p = open("фото для проекта/преломление света.jpg", "rb")
        bot.send_photo(message.chat.id, p)


    def linzs(message):
        bot.send_message(message.chat.id,
                         """
📌Линзой называют прозрачное тело, ограниченное двумя сферическими поверхностями.
📌Линию, проходящую через центры сферических поверхностей, ограничивающих линзу, называют главной оптической осью.
                         """)
        l = open("фото для проекта/линзы.jpg", "rb")
        bot.send_photo(message.chat.id, l)


    def focus(message):
        bot.send_message(message.chat.id,
                         """
👀Главный фокус линзы F - это точка, в которой после прелмления собираются лучи, параллельные главной оптической оси.
👀Расстояние от оптического центра линзы до её фокуса называется фокусным расстоянием.
👀Величину, обратную фокусному расстоянию (F), называют оптической силой линзы (D). Единица измерения: 1 дптр (диоптрия).
                         """)
        f = open("фото для проекта/фокус.jpg", "rb")
        bot.send_photo(message.chat.id, f)


    # квантовые явления
    def quantum(message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Радиоактивность")
        item2 = types.KeyboardButton("Виды излучений")
        item3 = types.KeyboardButton("Опыты Резерфорда")
        item4 = types.KeyboardButton("Планетарная модель атома")
        item5 = types.KeyboardButton("Состав атомного ядра")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item0)
        bot.send_message(message.chat.id, "Темы:", reply_markup=markup)


    def radioactivnost(message):
        bot.send_message(message.chat.id,
                         """
☢️Радиоактивностью называют явление самопроизвольного излучения некоторых химических элементов, а\
вид этого излучения называют радиоактивным излучением.
☢️Радиоактивность, которой обладают вещества, существующие в природе, называют естественной радиоактивностью.
                         """)
        r = open("фото для проекта/анри беккерель.jpg", "rb")
        bot.send_photo(message.chat.id, r)


    def kind_of_izl(message):
        vids = open("фото для проекта/виды излучений.jpg", "rb")
        bot.send_photo(message.chat.id, vids)

        alpha = open("фото для проекта/альфа.jpg", "rb")
        bot.send_photo(message.chat.id, alpha)

        beta = open("фото для проекта/бета.jpg", "rb")
        bot.send_photo(message.chat.id, beta)

        gamma = open("фото для проекта/гамма.jpg", "rb")
        bot.send_photo(message.chat.id, gamma)


    def opt_rezerford(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item0 = types.InlineKeyboardButton(text="Видео опыта Резерфорда",
                                           url="https://dzen.ru/video/watch/6301df6922706a1bfc2986c0?f=video")
        markup.add(item0)
        bot.send_message(message.chat.id,
                         """
В результате экспериментов Резерфорд предложил новую модель строения атома, названную планетарной моделью. Он сделал следующие выводы:

☢️В атоме существует положительно заряженная частица, названная ядром атома, которая отталкивает альфа-частицы.
☢️Размеры ядра малы по сравнению с размерами атома, поскольку отталкивается очень небольшое число альфа-частиц, а большинство альфа-частиц,\
свободно проходит через фольгу.
☢️Масса ядра сравнима с массой бета-частицы, поскольку масса электронов в 8000 раз меньше масса альфа-частицы и электроны не смогли бы\
изменить направление её движения.
                         """, reply_markup=markup)
        rez = open("фото для проекта/опыт резерфорда.jpg", "rb")
        bot.send_photo(message.chat.id, rez)


    def model_of_atoms(message):
        atom = open("фото для проекта/планетарная модель атома.jpg", "rb")
        bot.send_photo(message.chat.id, atom)


    def sostaf_of_atoms(message):
        bot.send_message(message.chat.id,
                         """
☢️Радиоактивное превращение ядер одних элементов в ядра других элементов называют радиоактивным ядром.
☢️Периодом полураспада T называют промежуток времени, в течение которого распадается половина первоначальноо числа атомов радиоактивного вещества.
☢️Превращение иссходного атомного ядра при взаимодействии с какой-либо частицей в другое ядро, отличное от исходного, называют ядерной реакцией.
☢️Все реально происходящие ядерные реакции подчиняются закону сохранения массового числа и закону сохранения зарядового числа.
                         """)
        s1 = open("фото для проекта/состав атомного ядра.jpg", "rb")
        bot.send_photo(message.chat.id, s1)
        s2 = open("фото для проекта/обозначение ядер хим элем.jpg", "rb")
        bot.send_photo(message.chat.id, s2)


    # справочные материалы
    def spravka(message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Константы")
        item2 = types.KeyboardButton("Десятичные приставки")
        item3 = types.KeyboardButton("Плотность")
        item4 = types.KeyboardButton("Удельные величины")
        item5 = types.KeyboardButton("Удельное электрическое сопротивление")
        item6 = types.KeyboardButton("Температуры плавления и кипения")
        item0 = types.KeyboardButton("⬅️Выход в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item0)
        bot.send_message(message.chat.id, "Справочный материал:", reply_markup=markup)


    def const(message):
        c = open("фото для проекта/константы.png", "rb")
        bot.send_photo(message.chat.id, c)


    def des_prist(message):
        p = open("фото для проекта/десятичные приставки.png", "rb")
        bot.send_photo(message.chat.id, p)


    def ro(message):
        r = open("фото для проекта/ро.jpg", "rb")
        bot.send_photo(message.chat.id, r)


    def ydel_vel(message):
        y = open("фото для проекта/удельная.png", "rb")
        bot.send_photo(message.chat.id, y)


    def yd_el_soprot(message):
        el_sop = open("фото для проекта/удельное эл спорот.png", "rb")
        bot.send_photo(message.chat.id, el_sop)


    def temp_plav_kip(message):
        t = open("фото для проекта/кипение и плавление веществ.jpeg", "rb")
        bot.send_photo(message.chat.id, t)


    # тесты
    def tests(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = "Тесты по механическим явлениям"
        item2 = "Тесты по тепловым явлениям"
        item3 = "Тесты по электромагнитным явлениям"
        item4 = "Тесты по квантовым явлениям"
        item0 = "⬅️Выход в главное меню"
        markup.add(item1, item2, item3, item4, item0)
        bot.send_message(message.chat.id, "Если вы правильно решили тест, то нажмите на значок ✅ после теста!")
        bot.send_message(message.chat.id, text="Доступные тесты на данный момент:", reply_markup=markup)

        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        people_id = message.chat.id
        cursor.execute(f"SELECT id FROM telegram_users WHERE id = {people_id}")
        data = cursor.fetchone()
        global n, k
        if data is None:
            # добавление данных
            users = [message.chat.id, n, k]
            cursor.execute("INSERT INTO telegram_users VALUES(?,?,?);", users)
            connect.commit()


    def test_after_true_answer(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = "Тесты по механическим явлениям"
        item2 = "Тесты по тепловым явлениям"
        item3 = "Тесты по электромагнитным явлениям"
        item4 = "Тесты по квантовым явлениям"
        item0 = "⬅️Выход в главное меню"
        markup.add(item1, item2, item3, item4, item0)
        bot.send_message(message.chat.id, "Ответ записан!", reply_markup=markup)


    @bot.message_handler(commands=['statistik'])
    def statistik(message):
        if message.chat.id == 847195722:
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute(f"""SELECT people_short_otzv_1 FROM short_otz""")
            data_people_short_otzv_1 = cursor.fetchall()
            cursor.execute(f"""SELECT people_short_otzv_2 FROM short_otz""")
            data_people_short_otzv_2 = cursor.fetchall()
            cursor.execute(f"""SELECT people_short_otzv_3 FROM short_otz""")
            data_people_short_otzv_3 = cursor.fetchall()
            cursor.execute(f"""SELECT people_short_otzv_4 FROM short_otz""")
            data_people_short_otzv_4 = cursor.fetchall()
            try:
                y1 = data_people_short_otzv_1[0]
                y2 = data_people_short_otzv_2[0]
                y3 = data_people_short_otzv_3[0]
                y4 = data_people_short_otzv_4[0]
                plt.bar(1, y1)
                plt.bar(2, y2)
                plt.bar(3, y3)
                plt.bar(4, y4)
                plt.show()
            except:
                pass
        else:
            bot.send_message(message.chat.id, "Ты не админ!")


    def test_of_mechine(message):
        c_id = message.chat.id
        num_question = 0
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        cursor.execute(f"""SELECT num_no_machine FROM tests_no_num WHERE id = {c_id}""")
        data_tuple_machine = cursor.fetchone()
        try:
            data_machine = str(data_tuple_machine[0])

            if ("1" in data_machine) and ("2" in data_machine) and ("3" in data_machine) and ("4" in data_machine) and (
                    "5" in data_machine) and ("6" in data_machine) and ("7" in data_machine) and ("8" in data_machine) and ("9" in data_machine):
                bot.send_message(message.chat.id, "Вы решили все тесты по данной теме!")
            else:
                while num_question == 0:
                    num = rn.randint(1, 9)
                    if num < 10 and (str(num) not in data_machine):
                        connect = sqlite3.connect('data_telegram.db')
                        cursor = connect.cursor()
                        num_question = num
                        data_machine += str(num_question)
                        cursor.execute(f"""UPDATE tests_no_num set num_no_machine={data_machine} WHERE id = {c_id}""")
                        connect.commit()
        except:
            send_welcome(message)

        if num_question == 1:
            q1 = "Что изучает кинематика?"
            answers1 = ["Изучает способы описания движений",
                        "Изучает причины движений",
                        "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q1, options=answers1, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


        elif num_question == 2:
            q2 = "Что изучает динамика?"
            answers2 = ["Изучает способы описания движений", "Изучает причины движений",
                        "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q2, options=answers2, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 3:
            q3 = "Формула потенциальной энергии?"
            answers3 = ["E=FS", "E=mgh", "E=mv^2/2", "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q3, options=answers3, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 4:
            q4 = "Формула кинетической энергии?"
            answers4 = ["E=mv^2/2", "E=mgh", "E=mv", "E=FS"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q4, options=answers4, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 5:
            q5 = "Что такое ускорение?"
            answers5 = ["Физическая величина, характерезующая быстроту изменения энергии",
                        "Физическая величина, характерезующая быстроту изменения времени",
                        "Физическая величина, характеризующая быстроту измения скорости",
                        "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q5, options=answers5, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 6:
            q6 = "Формула третьего закона Ньютона:"
            answers6 = ["F1= - F2", "F1=F2", "F1≠F2", "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q6, options=answers6, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 7:
            q7 = "Формула второго закона Ньютона:"
            answers7 = ["F=mv", "F=gt", "F=mg", "F=ma"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q7, options=answers7, type=Poll.QUIZ, correct_option_id=3,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 8:
            q8 = "Что такое импульс?"
            answers8 = ["Величина, равная произведению силы, действующей на тело и его скорости",
                        "Величина, равная произведению массы тела и его скорости",
                        "Величина, равная произведению массы тела и его силы, действующей на тело",
                        "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q8, options=answers8, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 9:
            q9 = "Какое движение называют равномерным?"
            answers9 = ["Движение, при котором тело движется без остановок",
                        "Движение, при котором за равные промежутки времени тело проходит равные пути",
                        "Движение, при котором тело движется исключительно по прямой трактории"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q9, options=answers9, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        # новые тесты
        elif num_question == 10:
            q10 = "Как называется явление изменения формы или объёма тела?"
            answers10 = ["Изменение состава вещества",
                         "Деформация",
                         "Изменение агрегатного состояния вещества"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q10, options=answers10, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 11:
            q11 = "Что такое КПД?"
            answers11 = [
                "Это векторная физическая величина, численно равная отношению полезной работы к затраченной в системе",
                "Это скалярная физическая величина, численно равная отношению затраченной работы к полезной в системе",
                "Это скалярная физическая величина, численно равная отношению полезной работы к затраченной в системе"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q11, options=answers11, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 12:
            q12 = "Что такое давление?"
            answers12 = ["Это физическая величина, равная отношению силы давления F к площади поверхности S",
                         "Это физичесая величина, равная отношению площади поверхности S к силе давления F",
                         "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q12, options=answers12, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 13:
            q13 = "Что такое сила Архимеда?"
            answers13 = ["Это сила, стремящееся втянуть тело в воду",
                         "Это сила, стремящееся вытянуть тело из воды",
                         "Это сила, стремящееся растянуть тело по поверхности воды",
                         "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q13, options=answers13, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 14:
            q14 = "В каких направлениях передаётся давление покоящейся жидкости?"
            answers14 = ["Во всех",
                         "По направению к центру",
                         "По касательной относительно молекулы",
                         "В каком-то хаотическом одном",
                         "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q14, options=answers14, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


    def test_of_tepl(message):
        c_id = message.chat.id
        num_question = 0
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        cursor.execute(f"""SELECT num_no_tepl FROM tests_no_num WHERE id = {c_id}""")
        data_tuple_tepl = cursor.fetchone()
        try:
            data_tepl = str(data_tuple_tepl[0])

            if ("1" in data_tepl) and ("2" in data_tepl) and ("3" in data_tepl) and ("4" in data_tepl) and ("5" in data_tepl) and (
                    "6" in data_tepl) and ("7" in data_tepl) and ("8" in data_tepl) and ("9" in data_tepl):
                bot.send_message(message.chat.id, "Вы решили все тесты по данной теме!")
            else:
                while num_question == 0:
                    num = rn.randint(1, 9)
                    if num < 10 and (str(num) not in data_tepl):
                        connect = sqlite3.connect('data_telegram.db')
                        cursor = connect.cursor()
                        num_question = num
                        data_tepl += str(num_question)
                        cursor.execute(f"""UPDATE tests_no_num set num_no_tepl={data_tepl} WHERE id = {c_id}""")
                        connect.commit()
        except:
            send_welcome(message)

        if num_question == 1:
            q1 = "Как называется процесс передачи энергии от одного тела к другому или от одной части тела к другой благодаря тепловому движению частиц?"
            answers1 = ["Теплоотдача",
                        "Теплопроводность",
                        "Теплообмен"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q1, options=answers1, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


        elif num_question == 2:
            q2 = "Как называется вид теплопередачи, при котором энергия передаётся слоями жидкости или газа?"
            answers2 = ["Теплообмен",
                        "Излучение",
                        "Конвекция"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q2, options=answers2, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 3:
            q3 = "Как называется вид теплопередачи, при котором испускание и распространение энергии происходит при помощи электромагнитных волн и элементарных частиц?"
            answers3 = ["Излучение",
                        "Конвекция",
                        "Теплообмен"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q3, options=answers3, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 4:
            q = "Притяжение между частицами твёрдого тела?"
            answers = ["Сильное",
                       "Умеренное",
                       "Слабое"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 5:
            q = "Притяжение между частицами жидкости?"
            answers = ["Сильное",
                       "Умеренное",
                       "Слабое"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 6:
            q = "Притяжение между частицами газа?"
            answers = ["Сильное",
                       "Умеренное",
                       "Слабое"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 7:
            q = "Что такое дифузия?"
            answers = ["Явление проникновения молекул одного вещества в промежутки между молекулами другого вещества",
                       "Явление непроникновения молекул одного вещества в промежутки между молекулами другого вещества",
                       "Свойство молекул одного вещества проникать в молекулы другого вещества"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 8:
            q = "Формула количества теплоты:"
            answers = ["Q = Lm",
                       "Q = qm",
                       "Q = cm(t2-t1)",
                       "Q = qm(t2-t1)",
                       "Q = cm",
                       "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 9:
            q = "Что такое тепловые двигатели?"
            answers = ["Устройства, увеличивающие внутреннюю энергию за счёт совершения механической работы",
                       "Устройства, КПД которых равен 80%",
                       "Устройства, совершающие механическую работу за счёт внутренней энергии топлива"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        # новые тесты
        elif num_question == 10:
            q = "Формула для испарения и конденсации:"
            answers = ["Q = Lm",
                       "Q = qm",
                       "Q = cm(t2-t1)",
                       "Q = qm(t2-t1)",
                       "Q = cm",
                       "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 11:
            q = "Формула количества теплоты, выделяемое при сгорании топлива:"
            answers = ["Q = Lm",
                       "Q = qm",
                       "Q = cm(t2-t1)",
                       "Q = qm(t2-t1)",
                       "Q = cm",
                       "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


    def test_of_elctr(message):
        c_id = message.chat.id
        num_question = 0
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        cursor.execute(f"""SELECT num_no_el FROM tests_no_num WHERE id = {c_id}""")
        data_tuple_el = cursor.fetchone()
        try:
            data_el = str(data_tuple_el[0])

            if ("1" in data_el) and ("2" in data_el) and ("3" in data_el) and ("4" in data_el) and ("5" in data_el) and ("6" in data_el) and (
                    "7" in data_el) and ("8" in data_el) and ("9" in data_el):
                bot.send_message(message.chat.id, "Вы решили все тесты по данной теме!")
            else:
                while num_question == 0:
                    num = rn.randint(1, 9)
                    if num < 10 and (str(num) not in data_el):
                        connect = sqlite3.connect('data_telegram.db')
                        cursor = connect.cursor()
                        num_question = num
                        data_el += str(num_question)
                        cursor.execute(f"""UPDATE tests_no_num set num_no_el = {data_el} WHERE id = {c_id}""")
                        connect.commit()
        except:
            send_welcome(message)


        if num_question == 1:
            q = "Проводники:"
            answers = ["Состоят из нетральных в целом атомов или молекул",
                       "Все металлы",
                       "Не имеют заряженных частиц"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 2:
            q = "Диэлектрики:"
            answers = ["Все металлы",
                       "Не имеют заряженных частиц",
                       "Состоят из нетральных в целом атомов или молекул"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 3:
            q = "Что называют постоянным электрическим током?"
            answers = ["Хаотичное движение заряженных частиц",
                       "Упорядоченное движение незаряженных частиц",
                       "Упорядоченное движение заряженных частиц",
                       "Нет правильного варианта ответа"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 4:
            q = "Какая из картинок(формул) соответствует формуле силы тока?"
            a1 = open("фото для теста/1.jpeg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/2.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/3.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна из ниже представленных"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 5:
            q = "Какая из картинок(формул) соответствует формуле напряжения?"
            a1 = open("фото для теста/1.jpeg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/2.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/3.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна из ниже представленных"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 6:
            q = "Какая из картинок(формул) соответствует формуле сопротивления?"
            a1 = open("фото для теста/1.jpeg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/2.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/3.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна из ниже представленных"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 7:
            q = "Какое соединение изображено на фотографии?"
            a = open("фото для теста/паралл.jpg", "rb")
            bot.send_photo(message.chat.id, a)
            answers = ["Параллельное",
                       "Последовательное",
                       "Прямоугольное"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 8:
            q = "Какое соединение изображено на фотографии?"
            a = open("фото для теста/послед.jpg", "rb")
            bot.send_photo(message.chat.id, a)
            answers = ["Параллельное",
                       "Последовательное",
                       "Прямоугольное"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 9:
            q = "Какая фотография соответствует формуле работы тока?"
            a1 = open("фото для теста/джоуль-ленц.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/работа тока.jpeg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/мощность.jpeg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        # новые тесты
        elif num_question == 10:
            q = "Какая фотография соответствует формуле мощности электрического тока?"
            a1 = open("фото для теста/джоуль-ленц.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/работа тока.jpeg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/мощность.jpeg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 11:
            q = "Какая фотография соответствует формуле закона Джоуля-Ленца?"
            a1 = open("фото для теста/джоуль-ленц.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/работа тока.jpeg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/мощность.jpeg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни одна"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


    def tests_of_kvant(message):
        c_id = message.chat.id
        num_question = 0
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()
        cursor.execute(f"""SELECT num_no_kvants FROM tests_no_num WHERE id = {c_id}""")
        data_tuple_kvants = cursor.fetchone()
        try:
            data_kvants = str(data_tuple_kvants[0])

            if ("1" in data_kvants) and ("2" in data_kvants) and ("3" in data_kvants) and ("4" in data_kvants):
                bot.send_message(message.chat.id, "Вы решили все тесты по данной теме!")
            else:
                while num_question == 0:
                    num = rn.randint(1, 4)
                    if num < 5 and (str(num) not in data_kvants):
                        connect = sqlite3.connect('data_telegram.db')
                        cursor = connect.cursor()
                        num_question = num
                        data_kvants += str(num_question)
                        cursor.execute(f"""UPDATE tests_no_num set num_no_kvants={data_kvants} WHERE id = {c_id}""")
                        connect.commit()
            #print(data_kvants)
        except:
            send_welcome(message)

        if num_question == 1:
            q = "Какой учёный обнаружил явление радиоактивности?"
            answers = ["Исаак Ньютон",
                       "Майкл Фарадей",
                       "Анри Беккерель",
                       "Эрнест Резерфорд"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 2:
            q = "На какой из фотографий изображено альфа-излучение?"
            a1 = open("фото для теста/альфа.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/бета.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/гамма.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни на одной"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 3:
            q = "На какой из фотографий изображено бета-излучение?"
            a1 = open("фото для теста/альфа.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/бета.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/гамма.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни на одной"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=1,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()

        elif num_question == 4:
            q = "На какой из фотографий изображено гамма-излучение?"
            a1 = open("фото для теста/альфа.jpg", "rb")
            bot.send_photo(message.chat.id, a1)
            a2 = open("фото для теста/бета.jpg", "rb")
            bot.send_photo(message.chat.id, a2)
            a3 = open("фото для теста/гамма.jpg", "rb")
            bot.send_photo(message.chat.id, a3)
            answers = ["1",
                       "2",
                       "3",
                       "Ни на одной"]
            markup = types.InlineKeyboardMarkup(row_width=1)
            true_item = types.InlineKeyboardButton("✅", callback_data="✅", one_time_keyboard=True)
            markup.add(true_item)
            bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=2,
                          reply_markup=markup)
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_user_id = message.chat.id
            cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
            n_data = cursor.fetchone()
            n = int(n_data[0]) + 1
            cursor.execute(f"""Update telegram_users set n = {n} where id = {people_user_id}""")
            connect.commit()


    def otzv(message):
        bot.send_message(message.chat.id, """
Для короткого отзыва нажмите одну из кнопок ниже⬇️:
Чтобы написать подробный отзыв воспользуйтесь командой: /write

Важно❗️ 
Чтобы отзыв был оформлен правильно, то после команды /write нажмите Ctrl+Enter, если вы на ПК, и enter, для мобильных устройств (return - на iphone)

📍Пример: /write 
                      hello world!                                  
                                          """)
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Больше тестов")
        item2 = types.KeyboardButton("Расширенный список тем")
        item3 = types.KeyboardButton("Более подробный материал в темах")
        item4 = types.KeyboardButton("Другое..")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Что бы вы хотели видеть нового в боте?", reply_markup=markup)


    # чтение n и k + вычисление процентра пройденных тестов к числу правильно выполненных
    @bot.message_handler(commands=['results'])
    def users_statictik(message):
        global k
        global n
        connect = sqlite3.connect('data_telegram.db')
        cursor = connect.cursor()

        people_user_id = message.chat.id

        cursor.execute(f"""SELECT n FROM telegram_users WHERE id = {people_user_id}""")
        n_data = cursor.fetchone()
        cursor.execute(f"""SELECT k FROM telegram_users WHERE id = {people_user_id}""")
        k_data = cursor.fetchone()
        try:
            if int(n_data[0]) != 0:
                results = round((int(k_data[0])) / (int(n_data[0])) * 100)
                bot.send_message(message.chat.id, f"""Процент успешного выполнения тестов: {results}%\
                                                    Всего пройдено тестов: {int(n_data[0])}   
Дано правильных ответов: {int(k_data[0])}    """)
                if results > 101 or int(k_data[0]) > int(n_data[0]):
                    bot.send_message(message.chat.id, "Вы обманываете! Ваш результат обнуляется!")
                    people_id = message.chat.id
                    cursor.execute(f"DELETE FROM telegram_users WHERE id={people_id}")
                    connect.commit()
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton("Решать тесты!", callback_data="тесты")
                markup.add(item)
                bot.send_message(message.chat.id, "Вы ещё не решили ни одного теста!", reply_markup=markup)
        except:
            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton("Решать тесты!", callback_data="тесты")
            markup.add(item)
            bot.send_message(message.chat.id, "Вы ещё не решили ни одного теста!", reply_markup=markup)


    @bot.message_handler(commands=['write'])
    def writer(message):
        try:
            global podr_otz
            people = list(map(str, message.text.split("\n")))
            print(people[1:])
            for i in people[1:]:
                if len(i) > 2 and i in people[1:] is not None:
                    bot.send_message(message.chat.id, "Спасибо! Ваш отзыв отправлен на рассмотрение!")
                    podr_otz.append(people[1:])

                    # создание таблицы для отзывов
                    connect = sqlite3.connect('data_telegram.db')
                    cursor = connect.cursor()
                    cursor.execute("""CREATE TABLE IF NOT EXISTS podr_otz(
                                        otz TEXT
                                    )""")
                    connect.commit()
                    people_otz = people[1:]
                    cursor.execute("INSERT INTO podr_otz VALUES(?);", people_otz)
                    connect.commit()

                    print(podr_otz)
                else:
                    bot.send_message(message.chat.id, "Пустой отзыв! Проверьте право написания отзыва.")
        except:
            pass

    # админ , для чтения подробных отзывов
    @bot.message_handler(commands=['read'])
    def reader(message):
        if message.chat.id == 847195722:
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            cursor.execute("""SELECT otz FROM podr_otz""")
            data_otz= cursor.fetchall()
            for line_data in data_otz:
                bot.send_message(message.chat.id, line_data)
        else:
            bot.send_message(message.cgat.id, "Вы не админ!")

    # ответ на нажатие кнопок
    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        global people_short_otzv_1, people_short_otzv_2, people_short_otzv_3, people_short_otzv_4, kol_opr
        # динамика
        if message.text.upper() == "ВТОРОЙ ЗАКОН НЬЮТОНА":
            second_zakon_nutona(message)

        elif message.text.upper() == "ПЕРВЫЙ ЗАКОН НЬЮТОНА":
            first_zakon_nutona(message)

        elif message.text.upper() == "ТРЕТИЙ ЗАКОН НЬЮТОНА":
            third_zakon_nutona(message)

        elif message.text.lower() == "силы в природе":
            force_in_wild(message)

        elif message.text.lower() == "деформация и сила упругости":
            deformation_and_force_uprugosti(message)

        elif message.text.lower() == "закон гука":
            zakon_Guka(message)

        elif message.text.upper() == "ДИНАМИКА":
            dinamika(message)

        elif message.text.lower() == "закон всемирного тяготения":
            zakon_world_mg(message)

        elif message.text.lower() == "импульс тела":
            mv(message)

        elif message.text.lower() == "закон сохранения импульса":
            zakon_save_mv(message)

        elif message.text.lower() == "механическая работа и мощность":
            mechine_A_N(message)

        elif message.text.lower() == "кпд":
            KPD(message)

        elif message.text.lower() == "давление":
            pressure(message)

        elif message.text.lower() == "закон паскаля":
            pascal(message)

        elif message.text.lower() == "закон архимеда":
            archimed(message)

        elif message.text.lower() == "механические колебания и волны":
            kolebania_and_volns(message)

        # выход в главное меню
        elif message.text.lower() == "⬅️выход в главное меню":
            exit_to_menu(message)

        # кинематика
        elif message.text.upper() == "КИНЕМАТИКА":
            kinematka(message)

        elif message.text.upper() == "РАВНОМЕРНОЕ ДВИЖЕНИЕ":
            ravnomernoe_dvj(message)

        elif message.text.upper() == "РАВНОУСКОРЕННОЕ/РАВНОЗАМЕДЛЕННОЕ ДВИЖЕНИЕ":
            ravn_uscor_and_zamedl_dvj(message)

        elif message.text.upper() == "ПОСТУПАТЕЛЬНОЕ ДВИЖЕНИЕ":
            postupatelnoe_dvj(message)

        elif message.text.upper() == "ВРАЩАТЕЛЬНОЕ ДВИЖЕНИЕ":
            rotational_motion(message)

        elif message.text.lower() == "движение с постоянным ускорением свободного падения":
            svobodnoe_padenie(message)

        elif message.text.lower() == "мгновенная и средняя скорости":
            mgn_and_sr_scorosti(message)

        elif message.text.lower() == "сложение скоростей":
            slojenie_scorostey(message)

        elif message.text.lower() == "ускорение":
            a(message)

        # энергия
        elif message.text.lower() == "механическая энергия":
            energy(message)

        elif message.text.lower() == "потенциальная энергия":
            poten_energy(message)

        elif message.text.lower() == "кинетическая энергия":
            kinet_energy(message)

        elif message.text.lower() == "теорема об изменении потенциальной энергии":
            teorema_poten_energy(message)

        elif message.text.lower() == "теорема об изменении кинетической энергии":
            teorema_kinet_energy(message)

        elif message.text.lower() == "закон сохранения механической энергии":
            zakon_save_energy(message)

        # механика
        elif message.text.lower() == "⚙️механические явления⚙️":
            machine(message)

        # тепловые явления
        elif message.text.lower() == "🌡тепловые явления🌡":
            teplo(message)

        elif message.text.lower() == "строение вещества":
            stroenie_substance(message)

        elif message.text.lower() == "виды теплопередачи":
            teploperedachi(message)

        elif message.text.lower() == "тепловое движение атомов и молекул":
            tepl_dv_atoms_and_mol(message)

        elif message.text.lower() == "внутренняя энергия":
            vn_energy(message)

        elif message.text.lower() == "количество теплоты":
            coll_teplots(message)

        elif message.text.lower() == "тепловые двигатели":
            tepl_dvigatel(message)

        elif message.text.lower() == "испарение и конденсация":
            evaporation_condensation(message)

        elif message.text.lower() == "плавление и кристаллизация":
            melting_crystallization(message)

        # электромагнитные явления
        elif message.text.lower() == "⚡️электромагнитные явления⚡️":
            electromagnitizm(message)

        elif message.text.lower() == "электризация тел":
            el_tel(message)

        elif message.text.lower() == "электрическое поле":
            el_pole(message)

        elif message.text.lower() == "постоянный электрический ток":
            poston_tok(message)

        elif message.text.lower() == "закон ома":
            zakon_oma(message)

        elif message.text.lower() == "последовательное и параллельное соединение проводников":
            connection(message)

        elif message.text.lower() == "работа и мощность электрического тока":
            A_and_N_el_toka(message)

        elif message.text.lower() == "закон джоуля-ленца":
            zakon_Djol_lenz(message)

        elif message.text.lower() == "опыт эрстеда. магнитное поле тока":
            opt_ersteda(message)

        elif message.text.lower() == "электромагнитная индукция":
            el_induction(message)

        # световые явления
        elif message.text.lower() == "💡световые явления💡":
            svet_evl(message)

        elif message.text.lower() == "закон прямолинейного распространения света":
            zakon_raspr_sveta(message)

        elif message.text.lower() == "закон отражения света":
            zakon_otr_sveta(message)

        elif message.text.lower() == "плоское зеркало":
            ploskoe_zerkalo(message)

        elif message.text.lower() == "преломление света":
            prelomlenie_sveta(message)

        elif message.text.lower() == "дисперсия света":
            dispersia(message)

        elif message.text.lower() == "линзы":
            linzs(message)

        elif message.text.lower() == "фокусное расстояние линзы":
            focus(message)

        # квантовые явления
        elif message.text.lower() == "☢️квантовые явления☢️":
            quantum(message)

        elif message.text.lower() == "радиоактивность":
            radioactivnost(message)

        elif message.text.lower() == "виды излучений":
            kind_of_izl(message)

        elif message.text.lower() == "опыты резерфорда":
            opt_rezerford(message)

        elif message.text.lower() == "планетарная модель атома":
            model_of_atoms(message)

        elif message.text.lower() == "состав атомного ядра":
            sostaf_of_atoms(message)

        # справочный материал
        elif message.text.lower() == "📜справочный материал📜":
            spravka(message)

        elif message.text.lower() == "константы":
            const(message)

        elif message.text.lower() == "десятичные приставки":
            des_prist(message)

        elif message.text.lower() == "плотность":
            ro(message)

        elif message.text.lower() == "удельные величины":
            ydel_vel(message)

        elif message.text.lower() == "удельное электрическое сопротивление":
            yd_el_soprot(message)

        elif message.text.lower() == "температуры плавления и кипения":
            temp_plav_kip(message)

        # отзывы
        elif message.text.lower() == "🗂оставить отзыв🗂":
            otzv(message)

        elif message.text.lower() == "больше тестов":
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_id = message.chat.id
            try:
                cursor.execute(f"""SELECT people_short_otzv_1 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_1 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_2 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_2 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_3 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_3 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_4 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_4 = cursor.fetchone()
                if int(data_people_short_otzv_1[0]) == 1 or int(data_people_short_otzv_2[0]) == 1 or int(data_people_short_otzv_3[0]) == 1 or int(data_people_short_otzv_4[0]) == 1:
                    bot.send_message(message.chat.id, "Вы уже оставляли отзыв!")
                    exit_to_menu(message)
                else:
                    people_short_otzv_1 += 1
                    bot.send_message(message.chat.id, "Спасибо за отзыв!")
                    cursor.execute(f"""Update short_otz set people_short_otzv_1 = {people_short_otzv_1} where id = {people_id}""")
                    connect.commit()
                    exit_to_menu(message)
            except:
                send_welcome(message)

        elif message.text.lower() == "расширенный список тем":
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_id = message.chat.id
            try:
                cursor.execute(f"""SELECT people_short_otzv_1 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_1 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_2 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_2 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_3 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_3 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_4 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_4 = cursor.fetchone()
                if int(data_people_short_otzv_1[0]) == 1 or int(data_people_short_otzv_2[0]) == 1 or int(data_people_short_otzv_3[0]) == 1 or int(data_people_short_otzv_4[0]) == 1:
                    bot.send_message(message.chat.id, "Вы уже оставляли отзыв!")
                    exit_to_menu(message)
                else:
                    people_short_otzv_2 += 1
                    bot.send_message(message.chat.id, "Спасибо за отзыв!")
                    cursor.execute(f"""Update short_otz set people_short_otzv_2 = {people_short_otzv_2} where id = {people_id}""")
                    connect.commit()
                    exit_to_menu(message)
            except:
                send_welcome(message)

        elif message.text.lower() == "более подробный материал в темах":
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_id = message.chat.id
            try:
                cursor.execute(f"""SELECT people_short_otzv_1 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_1 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_2 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_2 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_3 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_3 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_4 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_4 = cursor.fetchone()
                if int(data_people_short_otzv_1[0]) == 1 or int(data_people_short_otzv_2[0]) == 1 or int(data_people_short_otzv_3[0]) == 1 or int(data_people_short_otzv_4[0]) == 1:
                    bot.send_message(message.chat.id, "Вы уже оставляли отзыв!")
                    exit_to_menu(message)
                else:
                    people_short_otzv_3 += 1
                    bot.send_message(message.chat.id, "Спасибо за отзыв!")
                    cursor.execute(f"""Update short_otz set people_short_otzv_3 = {people_short_otzv_3} where id = {people_id}""")
                    connect.commit()
                    exit_to_menu(message)
            except:
                send_welcome(message)

        elif message.text.lower() == "другое..":
            connect = sqlite3.connect('data_telegram.db')
            cursor = connect.cursor()
            people_id = message.chat.id
            try:
                cursor.execute(f"""SELECT people_short_otzv_1 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_1 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_2 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_2 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_3 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_3 = cursor.fetchone()
                cursor.execute(f"""SELECT people_short_otzv_4 FROM short_otz WHERE id = {people_id}""")
                data_people_short_otzv_4 = cursor.fetchone()
                if int(data_people_short_otzv_1[0]) == 1 or int(data_people_short_otzv_2[0]) == 1 or int(data_people_short_otzv_3[0]) == 1 or int(data_people_short_otzv_4[0]) == 1:
                    bot.send_message(message.chat.id, "Вы уже оставляли отзыв!")
                    exit_to_menu(message)
                else:
                    bot.send_message(message.chat.id, "Спасибо за отзыв!")
                    people_short_otzv_4 += 1
                    cursor.execute(f"""Update short_otz set people_short_otzv_4 = {people_short_otzv_4} where id = {people_id}""")
                    connect.commit()
                    exit_to_menu(message)
            except:
                send_welcome(message)

        # тесты
        elif message.text.lower() == "📝тесты📝":
            tests(message)

        elif message.text.lower() == "тесты по механическим явлениям":
            test_of_mechine(message)

        elif message.text.lower() == "тесты по тепловым явлениям":
            test_of_tepl(message)

        elif message.text.lower() == "тесты по электромагнитным явлениям":
            test_of_elctr(message)

        elif message.text.lower() == "тесты по квантовым явлениям":
            tests_of_kvant(message)

        else:
            bot.reply_to(message, "Я не понимаю ваш ввод =(")
except:
    time.sleep(1)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
