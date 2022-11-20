# Выбор языка
LANGUAGE_RU = 'RU'
LANGUAGE_KO = 'KO'

########################################################################################################################
# Общее
CHOICE_LANGUAGE = 'Выберите язык/ (언어를 선택해주세요)'

START_RU = 'Выберите действие'
START_KO = '시작을 눌러주세요'

GET_PHONE_NUMBER_RU = 'Нажмите на кнопку и отправь номер телефона или \n' \
                      'напишите его в формате (+998*********)'
GET_PHONE_NUMBER_KO = '핸드폰 번호를 입력해주세요' '+998*********으로 써주세요'

INVALID_PHONE_NUMBER_RU = 'Неправильный формат номера, попробуйте еще раз'
INVALID_PHONE_NUMBER_KO = '번호를 맞게 다시 한번 적어주세요'

GET_FIRST_NAME_RU = 'Введите свое имя'
GET_FIRST_NAME_KO = '성함을 입력해주세요'

# Кнопки
RUSSIAN = 'Русский 🇷🇺'
KOREAN = '한국어 🇰🇷'

BOOKING_RU = 'Бронирование 🕐'
BOOKING_KO = '예약 🕐'

DELIVERY_RU = 'Доставка 🚚'
DELIVERY_KO = '배달 🚚'

CHANGE_LANG_RU = 'Поменять язык'
CHANGE_LANG_KO = '언어 바꾸기'

CHANGE_LANG_SUCCESS_RU = 'Язык успешно изменен.'
CHANGE_LANG_SUCCESS_KO = '언어가 성공적으로 바뀌었습니다'

BACK_TO_MAIN_PAGE_RU = 'Вернуться на главную страницу 📃'
BACK_TO_MAIN_PAGE_KO = '처음으로 돌아가기 📃'

BACK_TO_MENU_RU = 'Вернуться в меню ⏪'
BACK_TO_MENU_KO = 'Вернуться в меню ⏪'

SEND_CONTACT_RU = 'Отправить контакт 📱'
SEND_CONTACT_KO = '전화번호 보내기 📱'

BACK_RU = 'Назад 🔙'
BACK_KO = '뒤로 🔙'

ACCEPT_RU = 'Подтвердить ✅'
ACCEPT_KO = '확인 ✅'

ACCEPTING_RU = 'Подтверждено'
ACCEPTING_KO = '확인되었습니다'

CANCEL_RU = 'Отменить ❌'
CANCEL_KO = '취소 ❌'

ERROR_RU = 'Упс, что-то пошло не так, нажмите на кнопку и перезапустите бот'
ERROR_KO = '잘못되었습니다, 봇을 재시작해주세요'

########################################################################################################################
# Бронирование
BOOKING_REQUEST_CATEGORY_RU = 'Пожалуйста, выберите категорию посадочных мест'
BOOKING_REQUEST_CATEGORY_KO = '자리를 선택해주세요'

BOOKING_REQUEST_DATE_RU = 'Пожалуйста, ниже выберите дату на которую хотите забронировать столик.'
BOOKING_REQUEST_DATE_KO = '날짜를 선택해주세요'

BOOKING_FAILED_DATE_RU = 'Извините, я не могу забронировать место на предедущие дни, попробуйте еще раз'
BOOKING_FAILED_DATE_KO = '죄송합니다, 지난 날짜에는 예약하 실수 없습니다'

BOOKING_REQUEST_TIME_RU = 'Пожалуйста, введите время на которое хотите забронировать столик.\n' \
                          'Формат времени ЧЧ:ММ (Заказ столиков может осуществлятся только в 00 минут.\n' \
                          'Например: 18:00, 19:00 и т.д)'
BOOKING_REQUEST_TIME_KO = '예약 시간을 적어주세요 (18:00/ 19:00) (분 단위로 설정하실 수 없습니다)'

BOOKING_FAILED_TIME_RU = 'Не удалось определить время, пожалуйста введите еще раз.'
BOOKING_FAILED_TIME_KO = '시간을 다시 한번 입력해주세요'

BOOKING_FAILED_TIME_NOW_RU = 'Невозможно забронировать столик на это время, попробуйте выбрать другое время'
BOOKING_FAILED_TIME_NOW_KO = '이 시간에는 예약하실 수 없습니다, 다른 시간을 선택해주세요'

BOOKING_REQUEST_PEOPLE_RU = 'Пожалуйста, введите количество человек'
BOOKING_REQUEST_PEOPLE_KO = '몇 분인지 입력해주세요'

BOOKING_FAILED_REQUEST_PEOPLE_RU = 'Некорректный ввод, попробуйте заново'
BOOKING_FAILED_REQUEST_PEOPLE_KO = '번호를 다시 한번 적어주세요'

BOOKING_FAILED_PEOPLE_QUANTITY_RU = 'Извините, но число людей не может превышать допустимого количества\n' \
                           'В эту кабинку разрешается от {0} до {1} человек'
BOOKING_FAILED_PEOPLE_QUANTITY_KO = '죄송합니다, 인원 수를 초과하셨습니다. 여기는 0-4명까지 가능합니다'

BOOKING_GET_TABLEID_RU = 'Выберите номер столика\n' \
                         'P.S. Столики которые не отображаются в кнопках, либо заняты, \n' \
                         'либо ориентировочно будут заняты на это время'
BOOKING_GET_TABLEID_KO = '테이블을 선택해 주세요 번호가 안나와있는 테이블은 이미 예약이 되어 있는 자리입니다'

BOOKING_DETAIL_RU = 'Детали бронирования:\n\n' \
                    'Имя: {0}\n' \
                    'Телефон: {1}\n' \
                    'Дата и время: {2}\n' \
                    'Посадочное место: {3}\n' \
                    'Стол: {4}\n' \
                    'Количество человек: {5}'
BOOKING_DETAIL_KO = '예약 세부 정보:\n\n' \
                    '성함: {0}\n' \
                    '전화번호: {1}\n' \
                    '날짜 및 시간: {2}\n' \
                    '자리 선택: {3}\n' \
                    '테이블: {4}\n' \
                    '인원 수 : {5}'

BOOKING_CONFIRMED_RU = 'Бронирование прошло успешно'
BOOKING_CONFIRMED_KO = '성공적으로 예약 되었습니다'

BOOKING_CANCELED_RU = 'Бронирование отменено'
BOOKING_CANCELED_KO = '죄송합니다, 예약이 취소되었습니다, /start를 눌러서 다시 한번 시도해주세요'

BOOKING_ADMIN_CANCEL_RU = 'Сожалеем, но бронирование отменено, нажмите на /start чтобы попробовать снова'
BOOKING_ADMIN_CANCEL_KO = '죄송합니다, 예약이 취소되었습니다, /start를 눌러서 다시 한번 시도해주세요'

BOOKING_WAIT_CONFIRM_RU = 'Ожидайте подтверждение бронирования от оператора, это займет немного времени'
BOOKING_WAIT_CONFIRM_KO = '예약 확인을 위해 곧 매니저로부터 연락이 갈 것입니다, 조금만 기다려주세요'



# Кнопки
TABLES_RU = '1️⃣ Столы'
TABLES_KO = '1️⃣ 테이블'

CABINS_RU = '2️⃣ Кабинки'
CABINS_KO = '2️⃣  룸'

PEOPLE_RU = 'чел.'
PEOPLE_KO = '인원 수.'

########################################################################################################################
# Доставка
DELIVERY_REQUEST_CATEGORY_RU = 'Категории меню'
DELIVERY_REQUEST_CATEGORY_KO = '메뉴를 선택해 주세요'

DELIVERY_REQUEST_DISH_RU = 'Выберите блюдо'
DELIVERY_REQUEST_DISH_KO = '음식을 선택해 주세요'

DELIVERY_REQUEST_QUANTITY_RU = 'Пожалуйста, выберите или введите количество'
DELIVERY_REQUEST_QUANTITY_KO = '갯수를 선택 또는 적어주세요'

DELIVERY_BASKET_RU = 'Добавлено в корзину.\n' \
                     'Хотите что-то еще?'
DELIVERY_BASKET_KO = '장바구니에 추가되었습니다.\n' \
                     '다른걸 추가하시겠습니까?'

DELIVERY_INCORRECT_QUANTITY_RU = 'Количество порций должны состоять из цифр и не могут быть меньше нуля.\n' \
                                 'Попробуйте снова.'
DELIVERY_INCORRECT_QUANTITY_KO = '갯수는 숫자로 표기 되어야하며 1 이하로는 선택하실 수 없습니다.\n' \
                                 '다시 한번 시도해주세요'
DELIVERY_PAYMENT_METHOD_RU = "<b>Выберите способ оплаты:</b>"
DELIVERY_PAYMENT_METHOD_KO = "<b>결제방식을 선택해주세요:</b>"

DELIVERY_REQUEST_ADDRESS_RU = '<b>Введите свой адрес или нажмите на "Поделиться геолокацией"\n ' \
                              'и телеграм определит ваше местоположение автоматически.</b>'
DELIVERY_REQUEST_ADDRESS_KO = '<b>주소를 적어주시거나 ”위치 공유하기“ 를 눌러주시면 저희가 주소를 받을 수 있습니다.</b>'

DELIVERY_CASH_METHOD_RU = 'Наличными 💵'
DELIVERY_CASH_METHOD_KO = '현금 💵'

DELIVERY_PAYME_METHOD_RU = 'PayMe 💵'
DELIVERY_PAYME_METHOD_KO = 'PayMe 💵'

DELIVERY_CANCELED_RU = 'Сожалеем, но Ваш заказ отменен, нажмите на /start чтобы попробовать снова'
DELIVERY_CANCELED_KO = '죄송합니다, 주문이 취소되었습니다, /start를 누르고 다시 한번 시도해주세요 '

DELIVERY_CART_RU = '<b>Корзина:</b>\n\n\n'
DELIVERY_CART_KO = '<b>장바구니:</b>\n\n\n'

DELIVERY_CART_PRODUCT_RU = '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'
DELIVERY_CART_PRODUCT_KO = '<b>{0}</b>\n{1} x {2:,} = {3:,}\n\n'

DELIVERY_CART_TOTAL_RU = '\n<b>Итого: {0:,} сум</b>'
DELIVERY_CART_TOTAL_KO = '\n<b>총합: {0:,} сум</b>'

DELIVERY_CART_EMPTY_RU = '<b>\nКорзина пуста.\n</b>'
DELIVERY_CART_EMPTY_KO = '<b>\n장바구니가 비었습니다.\n</b>'

DELIVERY_ORDER_ACCEPT_CLIENT_RU = '<b>Заказ </b>\n' \
                                  'Тип заказа: <b> "Доставка 🚘"</b>\n' \
                                  'Адрес: <b>{0}</b>\n' \
                                  'Номер телефона: <b>{1}</b>\n' \
                                  'Метод оплаты: <b>{2}</b>\n\n\n'
DELIVERY_ORDER_ACCEPT_CLIENT_KO = '<b> 주문확인 </b>\n' \
                                  '배달 방식: <b> "배달 🚘"</b>\n' \
                                  '주소: <b>{0}</b>\n' \
                                  '전화번호: <b>{1}</b>\n' \
                                  '결제 방식: <b>{2}</b>\n\n\n'

DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_RU = '<b>Заказ</b>\n' \
                                           'Тип заказа: <b>На вынос 🏃🏻‍♂️</b>\n' \
                                           'Адрес ресторана: <b>Мирабад, 41</b>\n' \
                                           'Номер телефона: <b>{0}</b>\n' \
                                           'Метод оплаты: <b>{1}</b>\n\n\n'
DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_KO = '<b>주문확인 </b>\n' \
                                           '배달 방식: <b>픽업 🏃🏻‍♂️</b>\n' \
                                           '가게 주소: <b>Мирабад, 41</b>\n' \
                                           '전화번호: <b>{0}</b>\n' \
                                           '결제방식: <b>{1}</b>\n\n\n'

DELIVERY_ORDER_CLIENT_TOTAL_RU = '\n<b>Сумма заказа: {0:,} сум + стоимость доставки (определяется исходя от адреса доставки)</b>\n\n' \
                                 'Для связи с оператором @masil_uz'
DELIVERY_ORDER_CLIENT_TOTAL_KO = '\n<b>결제 금액: {0:,} сум + 배달비 (배달지에 따라 금액이 달라집니다)</b>\n\n' \
                                 '매니저와 연락을 원하시면 @masil_uz'

DELIVERY_ORDER_ACCEPT_ADMIN_RU = '<b>Заказ #{0}</b>\n' \
                                 'Тип заказа: <b> "Доставка 🚘"</b>\n' \
                                 'Адрес: <b>{1}</b>\n' \
                                 'Номер телефона: <b>{2}</b>\n' \
                                 'Метод оплаты: <b>{3}</b>\n\n\n'
DELIVERY_ORDER_ACCEPT_ADMIN_KO = '<b>주문확인 #{0}</b>\n' \
                                 '배달 방식: <b> "배달 🚘"</b>\n' \
                                 '주소: <b>{1}</b>\n' \
                                 '전화번호: <b>{2}</b>\n' \
                                 '결제방식: <b>{3}</b>\n\n\n'

DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_RU = '<b>Заказ #{0}</b>\n' \
                                          'Тип заказа: <b>На вынос 🏃🏻‍♂️</b>\n' \
                                          'Номер телефона: <b>{1}</b>\n' \
                                          'Метод оплаты: <b>{2}</b>\n\n\n'
DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_KO = '<b>주문확인 #{0}</b>\n' \
                                          '배달 방식: <b>픽업 🏃🏻‍♂️</b>\n' \
                                          '전화번호: <b>{1}</b>\n' \
                                          '결제방식: <b>{2}</b>\n\n\n'

DELIVERY_ORDER_ADMIN_TOTAL_RU = '\n<b>Сумма заказа: {0:,} сум</b>'
DELIVERY_ORDER_ADMIN_TOTAL_KO = '\n<b>결제 금액: {0:,} сум</b>'

DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_RU = 'Спасибо, ваш заказ <b>#{}</b> ' \
                                       'передан на обработку. Ждите подтверждения от оператора.' ####
DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_KO = '주문해주셔서 감사합니다 <b>#{}</b> ' \
                                       '곧 매니저로부터 연락이 갈 것입니다.'

DELIVERY_QUESTION_ACCEPT_RU = '<b>Подтвердить заказ?</b>'
DELIVERY_QUESTION_ACCEPT_KO = '<b>주문하시겠습니까?</b>'


DELIVERY_COST_RU = "<b>Введите сумму доставки</b>"
DELIVERY_COST_KO = "<b>배달비를 입력해주세요</b>"

DELIVERY_ORDER_RU = '<b>Ваш заказ #{0}</b>\n' \
                    'Тип заказа: <b> "Доставка 🚘"</b>\n' \
                    'Адрес: <b>{1}</b>\n' \
                    'Номер телефона: <b>{2}</b>\n' \
                    'Метод оплаты: <b>{3}</b>\n' \
                    'Время получения заказа: <b>В ближайшее время</b>\n\n\n'
DELIVERY_ORDER_KO = '<b>주문번호 #{0}</b>\n' \
                    '배달 방식: <b> "배달 🚘"</b>\n' \
                    '주소: <b>{1}</b>\n' \
                    '전화번호: <b>{2}</b>\n' \
                    '결제방식: <b>{3}</b>\n' \
                    '배달 받는 시간: <b>음식이 다 된 후 바로</b>\n\n\n'

DELIVERY_ORDER_TAKEAWAY_RU = '<b>Ваш заказ #{0}</b>\n' \
                             'Тип заказа: <b>На вынос 🏃🏻‍♂️</b>\n' \
                             'Адрес ресторана: <b>Мирабад, 41</b>\n' \
                             'Номер телефона: <b>{1}</b>\n' \
                             'Метод оплаты: <b>{2}</b>\n\n\n ' \
                             'Время получения заказа: <b>В ближайшее время</b>\n\n\n'
DELIVERY_ORDER_TAKEAWAY_KO = '<b>주문번호 #{0}</b>\n' \
                             '배달 방식: <b>픽업 🏃🏻‍♂️</b>\n' \
                             '가게 주소: <b>Мирабад, 41</b>\n' \
                             '전화번호: <b>{1}</b>\n' \
                             '결제 방식: <b>{2}</b>\n\n\n ' \
                             '배달 받는 시간: <b>음식이 된 후 바로</b>\n\n\n'

DELIVERY_ORDER_SUM_TOTAL_RU = '\n<b>Сумма заказа: {0:,} сум\n' \
                              'Сумма доставки: {1:,}\n' \
                              'Итого: {2:,}</b>\n\n'
DELIVERY_ORDER_SUM_TOTAL_KO = '\n<b>결제 금액: {0:,} сум\n' \
                              '배달비: {1:,}\n' \
                              '총합: {2:,}</b>\n\n'

DELIVERY_SOMETHING_ELSE_RU = 'Хотите что-то еще?'
DELIVERY_SOMETHING_ELSE_KO = '추가로 주문하시겠습니까?'

DELIVERY_WAITING_RU = 'Ожидайте подтверждение бронирование от оператора, это займет немного времени'
DELIVERY_WAITING_KO = '예약 확인을 위해 곧 매니저로부터 연락이 갈 것입니다, 조금만 기다려주세요'

DELIVERY_THANKS_RU = 'Благодарим за заказ, с вами свяжется оператор. Спасибо, что выбрали нас!' ###
DELIVERY_THANKS_KO = '주문해주셔서 감사합니다, 매니저로부터 곧 연락이 갈 것입니다. 저희 가게를 선택해주셔서 감사합니다!'

DELIVERY_TIME_INVALID_RU = 'Заказы принимаются с 11:00 до 21:00'
DELIVERY_TIME_INVALID_KO = '11:00부터 21:00까지 주문 가능합니다'

# Кнопки
BASKET_RU = 'Корзина 🛒'
BASKET_KO = '장바구니 🛒'

DELETE_RU = '❌ Удалить {}'
DELETE_KO = '❌ 지우기 {}'

CLEAR_BASKET_RU = 'Очистить корзину 🚫'
CLEAR_BASKET_KO = '장바구니 비우기 🚫'

ORDER_RU = 'Оформить заказ 🧾'
ORDER_KO = '주문하기 🧾'

SEND_LOCATION_RU = 'Поделиться локацией 🌐'
SEND_LOCATION_KO = '위치 공유하기 🌐'

TAKEAWAY_RU = 'На вынос 🏃🏻‍♂️'
TAKEAWAY_KO = '픽업 🏃🏻‍♂️'


########################################################################################################################
trans = {
    'general':
        {
            'LANGUAGE_RU': LANGUAGE_RU,
            'LANGUAGE_KO': LANGUAGE_KO,
            'RUSSIAN': RUSSIAN,
            'KOREAN': KOREAN,
            'CHOICE_LANGUAGE': CHOICE_LANGUAGE,
            'START_RU': START_RU,
            'START_KO': START_KO,
            'GET_PHONE_NUMBER_RU': GET_PHONE_NUMBER_RU,
            'GET_PHONE_NUMBER_KO': GET_PHONE_NUMBER_KO,
            'INVALID_PHONE_NUMBER_RU': INVALID_PHONE_NUMBER_RU,
            'INVALID_PHONE_NUMBER_KO': INVALID_PHONE_NUMBER_KO,
            'GET_FIRST_NAME_RU': GET_FIRST_NAME_RU,
            'GET_FIRST_NAME_KO': GET_FIRST_NAME_KO,
            'BOOKING_RU': BOOKING_RU,
            'BOOKING_KO': BOOKING_KO,
            'DELIVERY_RU': DELIVERY_RU,
            'DELIVERY_KO': DELIVERY_KO,
            'CHANGE_LANG_RU': CHANGE_LANG_RU,
            'CHANGE_LANG_KO': CHANGE_LANG_KO,
            'CHANGE_LANG_SUCCESS_RU': CHANGE_LANG_SUCCESS_RU,
            'CHANGE_LANG_SUCCESS_KO': CHANGE_LANG_SUCCESS_KO,
            'BACK_TO_MAIN_PAGE_RU': BACK_TO_MAIN_PAGE_RU,
            'BACK_TO_MAIN_PAGE_KO': BACK_TO_MAIN_PAGE_KO,
            'BACK_TO_MENU_RU': BACK_TO_MENU_RU,
            'BACK_TO_MENU_KO': BACK_TO_MENU_KO,
            'SEND_CONTACT_RU': SEND_CONTACT_RU,
            'SEND_CONTACT_KO': SEND_CONTACT_KO,
            'BACK_RU': BACK_RU,
            'BACK_KO': BACK_KO,
            'ACCEPT_RU': ACCEPT_RU,
            'ACCEPT_KO': ACCEPT_KO,
            'ACCEPTING_RU': ACCEPTING_RU,
            'ACCEPTING_KO': ACCEPTING_KO,
            'CANCEL_RU': CANCEL_RU,
            'CANCEL_KO': CANCEL_KO,
            'ERROR_RU': ERROR_RU,
            'ERROR_KO': ERROR_KO,
        },
    'booking':
        {
            'BOOKING_REQUEST_CATEGORY_RU': BOOKING_REQUEST_CATEGORY_RU,
            'BOOKING_REQUEST_CATEGORY_KO': BOOKING_REQUEST_CATEGORY_KO,
            'BOOKING_REQUEST_DATE_RU': BOOKING_REQUEST_DATE_RU,
            'BOOKING_REQUEST_DATE_KO': BOOKING_REQUEST_DATE_KO,
            'BOOKING_FAILED_DATE_RU': BOOKING_FAILED_DATE_RU,
            'BOOKING_FAILED_DATE_KO': BOOKING_FAILED_DATE_KO,
            'BOOKING_REQUEST_TIME_RU': BOOKING_REQUEST_TIME_RU,
            'BOOKING_REQUEST_TIME_KO': BOOKING_REQUEST_TIME_KO,
            'BOOKING_FAILED_TIME_RU': BOOKING_FAILED_TIME_RU,
            'BOOKING_FAILED_TIME_KO': BOOKING_FAILED_TIME_KO,
            'BOOKING_FAILED_TIME_NOW_RU': BOOKING_FAILED_TIME_NOW_RU,
            'BOOKING_FAILED_TIME_NOW_KO': BOOKING_FAILED_TIME_NOW_KO,
            'BOOKING_REQUEST_PEOPLE_RU': BOOKING_REQUEST_PEOPLE_RU,
            'BOOKING_REQUEST_PEOPLE_KO': BOOKING_REQUEST_PEOPLE_KO,
            'BOOKING_FAILED_REQUEST_PEOPLE_RU': BOOKING_FAILED_REQUEST_PEOPLE_RU,
            'BOOKING_FAILED_REQUEST_PEOPLE_KO': BOOKING_FAILED_REQUEST_PEOPLE_KO,
            'BOOKING_FAILED_PEOPLE_QUANTITY_RU': BOOKING_FAILED_PEOPLE_QUANTITY_RU,
            'BOOKING_FAILED_PEOPLE_QUANTITY_KO': BOOKING_FAILED_PEOPLE_QUANTITY_KO,
            'BOOKING_GET_TABLEID_RU': BOOKING_GET_TABLEID_RU,
            'BOOKING_GET_TABLEID_KO': BOOKING_GET_TABLEID_KO,
            'BOOKING_DETAIL_RU': BOOKING_DETAIL_RU,
            'BOOKING_DETAIL_KO': BOOKING_DETAIL_KO,
            'BOOKING_CONFIRMED_RU': BOOKING_CONFIRMED_RU,
            'BOOKING_CONFIRMED_KO': BOOKING_CONFIRMED_KO,
            'BOOKING_CANCELED_RU': BOOKING_CANCELED_RU,
            'BOOKING_CANCELED_KO': BOOKING_CANCELED_KO,
            'BOOKING_ADMIN_CANCEL_RU': BOOKING_ADMIN_CANCEL_RU,
            'BOOKING_ADMIN_CANCEL_KO': BOOKING_ADMIN_CANCEL_KO,
            'BOOKING_WAIT_CONFIRM_RU': BOOKING_WAIT_CONFIRM_RU,
            'BOOKING_WAIT_CONFIRM_KO': BOOKING_WAIT_CONFIRM_KO,
            'TABLES_RU': TABLES_RU,
            'TABLES_KO': TABLES_KO,
            'CABINS_RU': CABINS_RU,
            'CABINS_KO': CABINS_KO,
            'PEOPLE_RU': PEOPLE_RU,
            'PEOPLE_KO': PEOPLE_KO,
        },
    'delivery':
        {
            'DELIVERY_REQUEST_CATEGORY_RU': DELIVERY_REQUEST_CATEGORY_RU,
            'DELIVERY_REQUEST_CATEGORY_KO': DELIVERY_REQUEST_CATEGORY_KO,
            'DELIVERY_REQUEST_DISH_RU': DELIVERY_REQUEST_DISH_RU,
            'DELIVERY_REQUEST_DISH_KO': DELIVERY_REQUEST_DISH_KO,
            'DELIVERY_REQUEST_QUANTITY_RU': DELIVERY_REQUEST_QUANTITY_RU,
            'DELIVERY_REQUEST_QUANTITY_KO': DELIVERY_REQUEST_QUANTITY_KO,
            'DELIVERY_BASKET_RU': DELIVERY_BASKET_RU,
            'DELIVERY_BASKET_KO': DELIVERY_BASKET_KO,
            'DELIVERY_INCORRECT_QUANTITY_RU': DELIVERY_INCORRECT_QUANTITY_RU,
            'DELIVERY_INCORRECT_QUANTITY_KO': DELIVERY_INCORRECT_QUANTITY_KO,
            'DELIVERY_PAYMENT_METHOD_RU': DELIVERY_PAYMENT_METHOD_RU,
            'DELIVERY_PAYMENT_METHOD_KO': DELIVERY_PAYMENT_METHOD_KO,
            'DELIVERY_CASH_METHOD_RU': DELIVERY_CASH_METHOD_RU,
            'DELIVERY_CASH_METHOD_KO': DELIVERY_CASH_METHOD_KO,
            'DELIVERY_PAYME_METHOD_RU': DELIVERY_PAYME_METHOD_RU,
            'DELIVERY_PAYME_METHOD_KO': DELIVERY_PAYME_METHOD_KO,
            'DELIVERY_REQUEST_ADDRESS_RU': DELIVERY_REQUEST_ADDRESS_RU,
            'DELIVERY_REQUEST_ADDRESS_KO': DELIVERY_REQUEST_ADDRESS_KO,
            'DELIVERY_CANCELED_RU': DELIVERY_CANCELED_RU,
            'DELIVERY_CANCELED_KO': DELIVERY_CANCELED_KO,
            'DELIVERY_CART_RU': DELIVERY_CART_RU,
            'DELIVERY_CART_KO': DELIVERY_CART_KO,
            'DELIVERY_CART_PRODUCT_RU': DELIVERY_CART_PRODUCT_RU,
            'DELIVERY_CART_PRODUCT_KO': DELIVERY_CART_PRODUCT_KO,
            'DELIVERY_CART_TOTAL_RU': DELIVERY_CART_TOTAL_RU,
            'DELIVERY_CART_TOTAL_KO': DELIVERY_CART_TOTAL_KO,
            'DELIVERY_CART_EMPTY_RU': DELIVERY_CART_EMPTY_RU,
            'DELIVERY_CART_EMPTY_KO': DELIVERY_CART_EMPTY_KO,
            'DELIVERY_ORDER_ACCEPT_CLIENT_RU': DELIVERY_ORDER_ACCEPT_CLIENT_RU,
            'DELIVERY_ORDER_ACCEPT_CLIENT_KO': DELIVERY_ORDER_ACCEPT_CLIENT_KO,
            'DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_RU': DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_RU,
            'DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_KO': DELIVERY_ORDER_ACCEPT_CLIENT_TAKEAWAY_KO,
            'DELIVERY_ORDER_CLIENT_TOTAL_RU': DELIVERY_ORDER_CLIENT_TOTAL_RU,
            'DELIVERY_ORDER_CLIENT_TOTAL_KO': DELIVERY_ORDER_CLIENT_TOTAL_KO,
            'DELIVERY_ORDER_ACCEPT_ADMIN_RU': DELIVERY_ORDER_ACCEPT_ADMIN_RU,
            'DELIVERY_ORDER_ACCEPT_ADMIN_KO': DELIVERY_ORDER_ACCEPT_ADMIN_KO,
            'DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_RU': DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_RU,
            'DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_KO': DELIVERY_ORDER_ACCEPT_ADMIN_TAKEAWAY_KO,
            'DELIVERY_ORDER_ADMIN_TOTAL_RU': DELIVERY_ORDER_ADMIN_TOTAL_RU,
            'DELIVERY_ORDER_ADMIN_TOTAL_KO': DELIVERY_ORDER_ADMIN_TOTAL_KO,
            'DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_RU': DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_RU,
            'DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_KO': DELIVERY_ORDER_CLIENT_WAIT_ACCEPT_KO,
            'DELIVERY_QUESTION_ACCEPT_RU': DELIVERY_QUESTION_ACCEPT_RU,
            'DELIVERY_QUESTION_ACCEPT_KO': DELIVERY_QUESTION_ACCEPT_KO,
            'DELIVERY_COST_RU': DELIVERY_COST_RU,
            'DELIVERY_COST_KO': DELIVERY_COST_KO,
            'DELIVERY_ORDER_RU': DELIVERY_ORDER_RU,
            'DELIVERY_ORDER_KO': DELIVERY_ORDER_KO,
            'DELIVERY_ORDER_TAKEAWAY_RU': DELIVERY_ORDER_TAKEAWAY_RU,
            'DELIVERY_ORDER_TAKEAWAY_KO': DELIVERY_ORDER_TAKEAWAY_KO,
            'DELIVERY_ORDER_SUM_TOTAL_RU': DELIVERY_ORDER_SUM_TOTAL_RU,
            'DELIVERY_ORDER_SUM_TOTAL_KO': DELIVERY_ORDER_SUM_TOTAL_KO,
            'DELIVERY_SOMETHING_ELSE_RU': DELIVERY_SOMETHING_ELSE_RU,
            'DELIVERY_SOMETHING_ELSE_KO': DELIVERY_SOMETHING_ELSE_KO,
            'DELIVERY_TIME_INVALID_RU': DELIVERY_TIME_INVALID_RU,
            'DELIVERY_TIME_INVALID_KO': DELIVERY_TIME_INVALID_KO,
            'DELIVERY_WAITING_RU': DELIVERY_WAITING_RU,
            'DELIVERY_WAITING_KO': DELIVERY_WAITING_KO,
            'DELIVERY_THANKS_RU': DELIVERY_THANKS_RU,
            'DELIVERY_THANKS_KO': DELIVERY_THANKS_KO,
            'BASKET_RU': BASKET_RU,
            'BASKET_KO': BASKET_KO,
            'DELETE_RU': DELETE_RU,
            'DELETE_KO': DELETE_KO,
            'CLEAR_BASKET_RU': CLEAR_BASKET_RU,
            'CLEAR_BASKET_KO': CLEAR_BASKET_KO,
            'ORDER_RU': ORDER_RU,
            'ORDER_KO': ORDER_KO,
            'SEND_LOCATION_RU': SEND_LOCATION_RU,
            'SEND_LOCATION_KO': SEND_LOCATION_KO,
            'TAKEAWAY_RU': TAKEAWAY_RU,
            'TAKEAWAY_KO': TAKEAWAY_KO,

        }
}
