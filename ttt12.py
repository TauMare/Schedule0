import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from bs4 import BeautifulSoup
import time

vk_session = vk_api.VkApi(token='3e10411afa19524cd71d25430998b81c23509e03b1493c1000d60396e1cbce4e3f95b106d1d16bc541996')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)



def sender(id, text):
    vk_session.method('messages.send', {'user_id':id, 'message': text, 'random_id': 0})

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # f = open('groups\idGroup.txt', '+a')
        # print(f.readlines())
        if event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            print(msg)
            with open('groups\idGroup.txt') as File:
                Readlines = File.readlines()

            Readlines_Copy = Readlines

            print(Readlines_Copy)
            SomeBool = False
            for element in Readlines_Copy:
                if element.find(str(user_id)) != -1:
                    SomeBool = True
                elif element.find(str(user_id)) == -1:
                    SomeBool = False
            print(SomeBool)
            if msg == 'подписка 801а2':
                if SomeBool == True:
                    sender(user_id, 'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 801a2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801а2')
            elif msg == 'подписка 801а1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 801a1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801а1')
            elif msg == 'подписка 801б1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 80б1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801б1')
            elif msg == '801б2':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 801б2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801б2')
            elif msg == 'подписка 803а1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803a1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803а1')
            elif msg == 'подписка 803а2':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803a2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803а2')
            elif msg == 'подписка 803б2':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803б2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803б2')
            elif msg == 'подписка 803б1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803б1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803б1')
            elif msg == 'подписка 803в1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803в1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803в1')
            elif msg == 'подписка 803в2':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803в2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803в2')
            elif msg == 'подписка 803г1':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803г1\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803г1')
            elif msg == 'подписка 803г2':
                if SomeBool == True:
                    sender(user_id,
                           'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open('groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803г2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803г2')
            elif msg == 'отписка' and SomeBool == True:
                for element in Readlines_Copy:
                    if element.find(str(user_id)) != -1:
                        sender(user_id, 'Вы были успешно отписаны от ежедневной рассылки расписания')
                        Readlines_Copy.pop(Readlines_Copy.index(element))
                        with open('groups\idGroup.txt', 'w+') as File:
                            File.writelines(Readlines_Copy)
            elif msg == 'отписка' and SomeBool == False:
                sender(user_id, 'Мы не можем вас отписать так как вы не подписаны')
            else:
                sender(user_id, 'напиши что-нибудь нормальное')

  # for element in Search: asd asdasdasdxyCYXcYXC
  #                       if element.find(str(user_id)) != -1:
  #                           sender(user_id, 'пошел нахуй петушара')
  #                       else:

# if msg == 'подписка 801а2':
#     File = open('groups\idGroup.txt', '+a')
#     Search = File.readlines()
#     print(Search)
#     if len(Search) != 0:
#         for element in Search:
#             if element.find(str(user_id)) != -1:
#                 sender(user_id,
#                        'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы данных? Тогда напишите "Отписка"')
#             elif element.find(str(user_id)) == -1:
#                 File.write(str(user_id) + ', 801a2\n')
#                 sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801а2')
#     else:
#         File.write(str(user_id) + ', 801a2\n')
#         sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 801а1')
#     File.close()