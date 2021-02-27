import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='3e10411afa19524cd71d25430998b81c23509e03b1493c1000d60396e1cbce4e3f95b106d1d16bc541996')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

global SomeBool


# def subscribe(id):
#     try:
#         with open(r'groups\idGroup.txt', 'r+') as f:
#             string_from_file_list = f.readlines()
#             if len(string_from_file_list) != 0:
#                 for line in string_from_file_list:
#                     if line.find(str(id)) != -1:
#                         ifPersonSubscribed = True
#                         print(1)
#                     elif line.find(str(id)) == -1:
#                         ifPersonSubscribed = False
#                         print(2)
#                     return ifPersonSubscribed
#             else:
#                 print(3)
#                 ifPersonSubscribed = False
#                 return ifPersonSubscribed
#     except Exception as someException:
#         print('error' + str(someException))

# def subscribe(id):
#     try:
#         with open("groups/idGroup.txt") as subscribeListFile:
#             SubscribedList = subscribeListFile.readlines()
#             if len(SubscribedList) != 0:
#                 print(SubscribedList)
#                 for SubscribeElement in SubscribedList:
#                     if SubscribeElement.find(str(id)) != -1:
#                         print("Найден повтор ")
#                         return True
#                     elif SubscribeElement.find(str(id)) == -1:
#                         print("Повтор не найден")
#                         return False
#     except Exception as someException:
#         print('Возникла ошибка: ' + str(someException))
global SubscribedBoolean
def subscribe(id):
    try:
        with open("groups/idGroup.txt") as subscribeListFile:
            SubscribedList = subscribeListFile.readlines()
            if len(SubscribedList) != 0:
                print(SubscribedList)
                SubscribeElementCounter = 0
                for SubscribeElementCounter in range(0, len(SubscribedList)):
                    SubscribeElement = SubscribedList[SubscribeElementCounter]
                    print(SubscribeElement)
                    if SubscribeElement.find(str(id)) != -1:
                        print("Найден повтор ")
                        SubscribedBoolean = True
                        break
                    elif SubscribeElement.find(str(id)) == -1:
                        print("Повтор не найден")
                        SubscribedBoolean = False
                    print(SubscribeElement)
                    SubscribeElementCounter += 1
                return SubscribedBoolean
    except Exception as someException:
        print('Возникла ошибка: ' + str(someException))


# def unSubscribe (id):


def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # f = open('groups\idGroup.txt', '+a')
        # print(f.readlines())
        if event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            print(str(msg) + " от " + str(user_id))

            # with open(r'groups\idGroup.txt') as File:
            #     Readlines = File.readlines()
            #
            # Readlines_Copy = Readlines
            #
            # print(Readlines_Copy)
            # SomeBool = True
            # for element in Readlines_Copy:
            #     if element.find(str(user_id)) != -1:
            #         SomeBool = True
            #     elif element.find(str(user_id)) == -1:
            #         SomeBool = False
            # print(SomeBool)

            if msg == 'подписка 803г2':
                SomeBool = subscribe(user_id)
                if SomeBool:
                    sender(user_id, 'Вы уже есть в нашей базе данных для подписок, желаете удалить себя из базы '
                                    'данных? Тогда напишите "Отписка"')
                elif SomeBool == False:
                    with open(r'groups\idGroup.txt', 'a+') as File:
                        File.write(str(user_id) + ', 803г2\n')
                    sender(user_id, 'Вы были успешно подписаны на ежедневное получение расписания группы 803г2')

            elif msg == 'отписка':
                subscribe(user_id)
                if SomeBool:
                    sender(user_id, 'Вы были успешно отписаны от ежедневной рассылки расписания')
                else:
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
