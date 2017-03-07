from telegram import InlineKeyboardButton


spb_adm=u'адмиралтейский'
spb_vas=u'василеостровский'
spb_vyb=u'выборгский'
spb_kln=u'калининский'
spb_kir=u'кировский'
spb_krg=u'красногвардейский'
spb_krs=u'красносельский'
spb_krd=u'кронштадтский'
spb_msk=u'московский'
spb_nev=u'невский'
spb_prd=u'петроградский'
spb_pdv=u'петродворцовый'
spb_prm=u'приморский'
spb_frz=u'фрунзенский'
spb_cnt=u'центральный'


districts_button_list = [[InlineKeyboardButton(spb_adm, callback_data='spb_adm')], # адмиралтейский
            [InlineKeyboardButton(spb_vas, callback_data='spb_vas')], # василеостровский
            [InlineKeyboardButton(spb_vyb, callback_data='spb_vyb')], # выборгский
            [InlineKeyboardButton(spb_kln, callback_data='spb_kln')], # калининский
            [InlineKeyboardButton(spb_kir, callback_data='spb_kir')], # кировский
            [InlineKeyboardButton(spb_krg, callback_data='spb_krg')], # красногвардейский
            [InlineKeyboardButton(spb_krs, callback_data='spb_krs')], # красносельский
            [InlineKeyboardButton(spb_krd, callback_data='spb_krd')], # кронштадтский
            [InlineKeyboardButton(spb_msk, callback_data='spb_msk')], # московский
            [InlineKeyboardButton(spb_nev, callback_data='spb_nev')], # невский
            [InlineKeyboardButton(spb_prd, callback_data='spb_prd')], # петроградский
            [InlineKeyboardButton(spb_pdv, callback_data='spb_pdv')], # петродворцовый
            [InlineKeyboardButton(spb_prm, callback_data='spb_prm')], # приморский
            [InlineKeyboardButton(spb_frz, callback_data='spb_frz')], # фрунзенский
            [InlineKeyboardButton(spb_cnt, callback_data='spb_cnt')]  # центральный
            ]

metro_button_list = [
    InlineKeyboardButton("ст.м. Автово",                           callback_data='spb_01'),
    InlineKeyboardButton("ст.м. Адмиралтейская",                   callback_data='spb_02'),
    InlineKeyboardButton("ст.м. Академическая",                    callback_data='spb_03'),
    InlineKeyboardButton("ст.м. Балтийская",                       callback_data='spb_04'),
    InlineKeyboardButton("ст.м. Бухарестская",                     callback_data='spb_05'),
    InlineKeyboardButton("ст.м. Василеостровская",                 callback_data='spb_06'),
    InlineKeyboardButton("ст.м. Владимирская",                     callback_data='spb_07'),
    InlineKeyboardButton("ст.м. Волковская",                       callback_data='spb_08'),
    InlineKeyboardButton("ст.м. Выборгская",                       callback_data='spb_09'),
    InlineKeyboardButton("ст.м. Горьковская",                      callback_data='spb_10'),
    InlineKeyboardButton("ст.м. Гостиный двор",                    callback_data='spb_11'),
    InlineKeyboardButton("ст.м. Гражданский проспект",             callback_data='spb_12'),
    InlineKeyboardButton("ст.м. Девяткино",                        callback_data='spb_13'),
    InlineKeyboardButton("ст.м. Достоевская",                      callback_data='spb_14'),
    InlineKeyboardButton("ст.м. Елизаровская",                     callback_data='spb_15'),
    InlineKeyboardButton("ст.м. Звёздная",                         callback_data='spb_16'),
    InlineKeyboardButton("ст.м. Звенигородская",                   callback_data='spb_17'),
    InlineKeyboardButton("ст.м. Кировский завод",                  callback_data='spb_18'),
    InlineKeyboardButton("ст.м. Комендантский проспект",           callback_data='spb_19'),
    InlineKeyboardButton("ст.м. Крестовский остров",               callback_data='spb_20'),
    InlineKeyboardButton("ст.м. Купчино",                          callback_data='spb_21'),
    InlineKeyboardButton("ст.м. Ладожская",                        callback_data='spb_22'),
    InlineKeyboardButton("ст.м. Ленинский проспект",               callback_data='spb_23'),
    InlineKeyboardButton("ст.м. Лесная",                           callback_data='spb_24'),
    InlineKeyboardButton("ст.м. Лиговский проспект",               callback_data='spb_25'),
    InlineKeyboardButton("ст.м. Ломоносовская",                    callback_data='spb_26'),
    InlineKeyboardButton("ст.м. Маяковская",                       callback_data='spb_27'),
    InlineKeyboardButton("ст.м. Международная",                    callback_data='spb_28'),
    InlineKeyboardButton("ст.м. Московская",                       callback_data='spb_29'),
    InlineKeyboardButton("ст.м. Московские ворота",                callback_data='spb_30'),
    InlineKeyboardButton("ст.м. Нарвская",                         callback_data='spb_31'),
    InlineKeyboardButton("ст.м. Невский проспект",                 callback_data='spb_32'),
    InlineKeyboardButton("ст.м. Новочеркасская",                   callback_data='spb_33'),
    InlineKeyboardButton("ст.м. Обводный канал",                   callback_data='spb_34'),
    InlineKeyboardButton("ст.м. Обухово",                          callback_data='spb_35'),
    InlineKeyboardButton("ст.м. Озерки",                           callback_data='spb_36'),
    InlineKeyboardButton("ст.м. Парк Победы",                      callback_data='spb_37'),
    InlineKeyboardButton("ст.м. Парнас",                           callback_data='spb_38'),
    InlineKeyboardButton("ст.м. Петроградская",                    callback_data='spb_39'),
    InlineKeyboardButton("ст.м. Пионерская",                       callback_data='spb_40'),
    InlineKeyboardButton("ст.м. Площадь Александра Невского 1",    callback_data='spb_41'),
    InlineKeyboardButton("ст.м. Площадь Александра Невского 2",    callback_data='spb_42'),
    InlineKeyboardButton("ст.м. Площадь Восстания",                callback_data='spb_43'),
    InlineKeyboardButton("ст.м. Площадь Ленина",                   callback_data='spb_44'),
    InlineKeyboardButton("ст.м. Площадь Мужества",                 callback_data='spb_45'),
    InlineKeyboardButton("ст.м. Политехническая",                  callback_data='spb_46'),
    InlineKeyboardButton("ст.м. Приморская",                       callback_data='spb_47'),
    InlineKeyboardButton("ст.м. Пролетарская",                     callback_data='spb_48'),
    InlineKeyboardButton("ст.м. Проспект Большевиков",             callback_data='spb_49'),
    InlineKeyboardButton("ст.м. Проспект Ветеранов",               callback_data='spb_50'),
    InlineKeyboardButton("ст.м. Проспект Просвещения",             callback_data='spb_51'),
    InlineKeyboardButton("ст.м. Пушкинская",                       callback_data='spb_52'),
    InlineKeyboardButton("ст.м. Рыбацкое",                         callback_data='spb_53'),
    InlineKeyboardButton("ст.м. Садовая",                          callback_data='spb_54'),
    InlineKeyboardButton("ст.м. Сенная площадь",                   callback_data='spb_55'),
    InlineKeyboardButton("ст.м. Спасская",                         callback_data='spb_56'),
    InlineKeyboardButton("ст.м. Спортивная",                       callback_data='spb_57'),
    InlineKeyboardButton("ст.м. Старая Деревня",                   callback_data='spb_58'),
    InlineKeyboardButton("ст.м. Технологический институт 1",       callback_data='spb_59'),
    InlineKeyboardButton("ст.м. Технологический институт 2",       callback_data='spb_60'),
    InlineKeyboardButton("ст.м. Удельная",                         callback_data='spb_61'),
    InlineKeyboardButton("ст.м. Улица Дыбенко",                    callback_data='spb_62'),
    InlineKeyboardButton("ст.м. Фрунзенская",                      callback_data='spb_63'),
    InlineKeyboardButton("ст.м. Чёрная речка",                     callback_data='spb_64'),
    InlineKeyboardButton("ст.м. Чернышевская",                     callback_data='spb_65'),
    InlineKeyboardButton("ст.м. Чкаловская",                       callback_data='spb_66'),
    InlineKeyboardButton("ст.м. Электросила",                      callback_data='spb_67')
]

types_button_list = [
            [InlineKeyboardButton('Пластиковый пакет',              callback_data='type_1')],
            [InlineKeyboardButton('Пластиковое ведерко',            callback_data='type_2')],
            [InlineKeyboardButton('CD/DVD диски',                   callback_data='type_3')],
            [InlineKeyboardButton('Бумага',                         callback_data='type_4')],
            [InlineKeyboardButton('Втулка',                         callback_data='type_5')],
            [InlineKeyboardButton('Упаковка от яиц',                callback_data='type_6')],
            [InlineKeyboardButton('Упаковка от масла, маргарина',   callback_data='type_7')],
            [InlineKeyboardButton('Пластиковый контейнер',          callback_data='type_8')]
            ]

