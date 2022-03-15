#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import *
from telebot import types
import random
import sqlite3
from config_game import *

number_base

##################################   S E T T I N G S ##############################
bot = telebot.TeleBot(token) 

def number(summ):
    if summ > 0:
        data = ''
        for num in str(summ):
            data = data + number_base[num]
    else:
        data = '➖1️⃣'

    return data

class Logging():
    def pool_error(logg):
        old_logg = open('pool_logg.txt', 'r', encoding="utf-8").read()
        new_logg = old_logg + '\n' + time.strftime("%m/%d/%Y, %H:%M:%S") + " | " + logg
        open("pool_logg.txt", 'wt', encoding="utf-8").write(new_logg)

class SQL():
################### NEW DB ############################
    def new_db():
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS USERS (ID TEXT,ИМЯ TEXT,MSG1 TEXT,MSG2 TEXT,REF1 TEXT,REF2 TEXT,DATA1 TEXT,DATA2 TEXT,DATA3 TEXT,DATA4 TEXT,DATA5 TEXT);""")
        conn.commit()

################### WINNERS ############################
    def winners():
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT DATA2 FROM USERS") # Ищем в базе
        base = cursor.fetchall()
        cursor.execute(f"SELECT ИМЯ FROM USERS") # Ищем в базе
        names = cursor.fetchall()
        text = 'Сатистика победителей:\n-----------------------------------'
        dict = {}
        summ = []

        for point in range(0,len(base)):
            dict[int(base[point][0])] = names[point][0]
        data = sorted(dict,reverse=True)
        count = len(data)

        if count > 10:
            count = 10

        for n in range(count):
            text = text +f'\n|{score_base[n]} | {data[n]}   {dict[data[n]]}\n-----------------------------------'

        return text

    def best_of_best(new_record):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT DATA2 FROM USERS") # Ищем в базе
        base = cursor.fetchall()
        best = True

        for point in base:
            if int(point[0]) > new_record:
                best = False
                break

        return best
        


################### Н О В Ы Й  Ю З Е Р ############################
    def add_new_user(id,name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT (ID) FROM USERS WHERE ID = {id}") # Ищем в базе
        msg_base = cursor.fetchone()

        if msg_base == None:
            cursor.execute(f"INSERT INTO USERS (ID,ИМЯ,MSG1,MSG2,REF1,REF2,DATA1,DATA2,DATA3,DATA4,DATA5) VALUES ({id},'{name}','|','|','0','0','100','100','','','')")
            conn.commit()
        conn.close()

################### Р А Б О Т А  С  О Д Н О Й  Я Ч Е Й К О Й ############################
    def read_one(table,id,column):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM {table} WHERE ID = {id}") # Ищем в базе
        data = cursor.fetchone()
        conn.close()

        if data ==  None:
            return None
        else:
            return data[0]
    
    def write_one(table,id,column,data):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table} SET ({column}) = '{data}'  WHERE ID = {id}")
        conn.commit()
        conn.close()

################### Р А Б О Т А  С  С О О Б Щ Е Н И Я М И ############################
    def msg_id_save(id,message_id):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor() 
            cursor.execute(f"SELECT (MSG2) FROM USERS WHERE ID = {id}") # Ищем в базе
            msg_base = cursor.fetchone()
            new_msg_base = msg_base[0] + f'{message_id}|'
            cursor.execute(f"UPDATE USERS SET (MSG2) = '{new_msg_base}'  WHERE ID = {str(id)}")
            conn.commit()
            conn.close()
        except:
            conn.close()
            pass

    def msg_id_clear(id): 
        try:  
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor() 
            cursor.execute(f"SELECT (MSG1) FROM USERS WHERE ID = {id}") # Ищем в базе
            msg_base = cursor.fetchone()

            if msg_base[0] != '|':
                data = msg_base[0].split('|')[1:][:-1]

                for message_id in data:
                    try:
                        bot.delete_message(chat_id=id, message_id=int(message_id))
                    except:
                        pass

            cursor.execute(f"SELECT (MSG2) FROM USERS WHERE ID = {id}") # Ищем в базе
            new_msg_base = cursor.fetchone()
            cursor.execute(f"UPDATE USERS SET (MSG1) = '{new_msg_base[0]}'  WHERE ID = {str(id)}")
            cursor.execute(f"UPDATE USERS SET (MSG2) = '|'  WHERE ID = {str(id)}")
            conn.commit()
            conn.close()
        except:
            conn.close()
            pass

class Game():
    def balance(data,btn):
        info = None
        count = 0

        for color in colour_base:

            if color in btn:
                count+=1

        if count == 6:
            info = 'Все цвета на кнопке разные.'

        if data > 0:
            for point in btn:
                if data > 0:
                    if point == colour_base[0]:
                        data = data + random.randint(0,4)
                    elif point == colour_base[1]:
                        data = data - random.randint(0,4)
                    elif point == colour_base[2]:
                        data = data + random.randint(0,12)
                    elif point == colour_base[3]:
                        data = data - random.randint(0,12)
                    elif point == colour_base[4]:
                        data = data + random.randint(0,30)
                    elif point == colour_base[5]:
                        data = data - random.randint(0,30)
                    elif point == colour_base[6]:
                        if data < 100:
                            data = data + random.randint(0,(100-data))
                        else:
                            data = data - random.randint(0,(data-100))
                else:
                    info = 'Баланс опустился ниже 0'
                    break

        if data % 17 == 0:
            info = 'Баланс кратен 17.'

        return data, info

    def buttons():
        btns = {}

        for number in range(8):
            one_btn = ''

            for n in range(6):
                one_btn = one_btn + colour_base[random.randint(0,6)]
            btns[one_btn] = f'BTN{one_btn}'

        return btns

class Bot():
#############################        B O T        ###############################
    def __init__(self):
        super().__init__()
        @bot.message_handler(content_types=['text'])
        def new_msg(message):
            def inline_keyboard(dict,row_width):
                kb = types.InlineKeyboardMarkup(row_width=row_width)
                kb_list = []

                for text, data in dict.items():
                    kb_list.append(types.InlineKeyboardButton(text=text, callback_data=data))
                kb.add(*kb_list)

                return kb

            if message.text == '/start' or message.text == '/Start':
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                name = message.from_user.first_name if message.from_user.first_name!=None else message.from_user.username

                if SQL.read_one('USERS',message.chat.id,'ИМЯ') == None:
                    SQL.add_new_user(message.chat.id,name)
                text =f'''
    Привет, {name}👋
    Это тестовый Бот-Игра ColorSquare.
    '''
                
                msg = bot.send_message(message.chat.id, text,reply_markup=inline_keyboard(start_btn,2))
                SQL.msg_id_save(message.chat.id,msg.message_id)
                SQL.msg_id_clear(message.chat.id)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            def inline_keyboard(dict,row_width):
                kb = types.InlineKeyboardMarkup(row_width=row_width)
                kb_list = []

                for text, data in dict.items():
                    kb_list.append(types.InlineKeyboardButton(text=text, callback_data=data))
                kb.add(*kb_list)

                return kb

            if call.data == 'START_NOW': 
                start_balance = 100
                SQL.write_one('USERS',call.message.chat.id,'DATA1',start_balance)
                text = f'🎲  🔲🔲🔲🔲🔲🔲\n\n🏦  {number(start_balance)}'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_keyboard(Game.buttons(),2))

            elif call.data == 'STTISTIC':
                text = SQL.winners()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_keyboard(winners_btn,2))
            elif call.data == 'INFORMATION': 
                text = f'ИНФОРМАЦИЯ'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_keyboard(info_btn,2))
            elif 'BTN' in call.data:
                start_balance = int(SQL.read_one('USERS',call.message.chat.id,'DATA1'))
                btn_colore = call.data.split('BTN')[1]
                data = Game.balance(start_balance,btn_colore)
                balance = data[0]
                info = data[1]
                new_record = ''
                max_balance = int(SQL.read_one('USERS',call.message.chat.id,'DATA2'))
                
                if info == None:
                    SQL.write_one('USERS',call.message.chat.id,'DATA1',balance)

                    if start_balance < balance:

                        if max_balance < balance:
                            SQL.write_one('USERS',call.message.chat.id,'DATA2',balance)
                            new_record = '\n🏆  New record  🏆\n'
                        text = f'''
🟢🔵⚪️  ➕ {number(balance - start_balance)}    ⚪️🔵🟢
{new_record}
🎲  {btn_colore}

🏦  {number(balance)}'''
                    else:
                        text = f'''
🔴🟠🟡   ➖{number(start_balance - balance)}   🟡🟠🔴

🎲  {btn_colore}

🏦  {number(balance)}
'''

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_keyboard(Game.buttons(),2))
                else:
                    if SQL.best_of_best(balance):
                        text = f'''
🟢🔵⚪️ ⭐️  YOU WIN  ⭐️ ⚪️🔵🟢

🎲  {btn_colore}

🏦  {number(balance)}

Description: {info}'''
                    else:    
                        text = f'''
🔴🟠🟡 G A M E   O W E R 🟡🟠🔴

🎲  {btn_colore}

🏦  {number(balance)}

Description: {info}'''
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=text, reply_markup=inline_keyboard(restart_btn,2))



        try:
            bot.skip_pending = True
            bot.infinity_polling(long_polling_timeout=100)
        except Exception as e:
            Logging.pool_error(str(e))
            pass

bbot = Bot()
