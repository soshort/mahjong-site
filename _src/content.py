"""Тексты страницы «Как играть» и раздела «Вопросы и ответы» (en, ru).
Только то, что в игре правда (правила — из подсказок Мажобэ TIP_* и
описания в Play); меняется игра — меняется и здесь."""

HOWTO = {
    "en": {
        "file": "how-to-play.html",
        "title": "How to play Mazhobe: Mahjong for Two — rules of the 4-tile shelf",
        "desc": "Rules of Mazhobe: Mahjong for Two: free tiles, the 4-slot shelf, pairs, ice, locks and mystery tiles, "
                "online duels, Duet and the daily level. Tips for winning.",
        "h1": "How to play",
        "intro": "Mazhobe is mahjong solitaire with a twist: tiles don't disappear from the board in pairs — they go "
                 "to a shelf with four slots. Here are the rules, the board mechanics and the two-player modes.",
        "sections": [
            ("The goal", ["Clear the board: take every tile and match them all in pairs on the shelf."]),
            ("Free tiles", ["You can only take a free tile: nothing lies on top of it and at least one side, left or "
                            "right, is open. Tiles you can't take yet look darker.",
                            "From level 15 some tiles lie face down: the first tap turns one over, the next one "
                            "takes it."]),
            ("The shelf", ["Tap a free tile and it flies to the shelf. When two identical tiles meet there, the pair "
                           "vanishes and earns acorns.",
                           "The shelf has only four slots. Fill all four with different tiles and the level is lost — "
                           "so before taking a tile, know where its twin is."]),
            ("Stars, hints and undo", ["Each level has one to five stars of difficulty. Every deal is checked: it has "
                                       "a solution, and the hint leads exactly to it.",
                                       "A hint shows the next good move, undo takes back the last one. When they run "
                                       "out, you can get one more by watching a short ad — only if you want to."]),
            ("Ice, locks and mysteries", ["Ice: a frozen tile can't be taken until its neighbours are cleared in "
                                          "pairs — then the ice cracks.",
                                          "Locks: a locked tile opens once you match the pair of keys of the same "
                                          "metal — bronze, silver or gold.",
                                          "Mystery: a tile with a question mark hides its picture. Put it on the "
                                          "shelf: if it meets its twin, it sweeps the whole board at once; if not, it "
                                          "just takes up a slot."]),
            ("Online duel", ["Two players, two phones, one board and one shelf. Both tap at the same time; the pair "
                             "goes to whoever closes it, and the one with more pairs wins.",
                             "If your tap would fill the shelf with a fourth different tile, it is cancelled: the tile "
                             "goes back and you lose a point.",
                             "In a timed duel you take turns, and a bar shows whose move it is.",
                             "Invite a friend from the leaderboard or tap “Find an opponent”. After the match, say GG."]),
            ("Duel with Mazhobe", ["The same duel against Mazhobe the toad — he sits behind the shelf and eyes your "
                                   "tiles. Three moods: Sleepy, Sly and Reckless; the more reckless he is, the more "
                                   "acorns a win brings. Works without a connection."]),
            ("Duet", ["Clear one board together with a shared shelf. You win — or fill the shelf — together."]),
            ("Daily level", ["One level for everyone each day. The ghost of the day's best player plays beside you; "
                             "overtake it for a bonus."]),
            ("Tips", ["Keep a slot free: three different tiles on the shelf leave no room for a mistake.",
                      "Take tiles whose twin you can already see.",
                      "Open a new layer only when the shelf has room — you don't know what's underneath."]),
        ],
        "image": ("mechanics", "Ice, locks and mysteries on the board"),
    },
    "ru": {
        "file": "how-to-play.html",
        "title": "Как играть в «Мажобэ: Маджонг на двоих» — правила полки на 4 тайла",
        "desc": "Правила игры «Мажобэ: Маджонг на двоих»: свободные тайлы, полка на 4 места, пары, лёд, замки и "
                "загадки, дуэль онлайн, «Дуэт» и уровень дня. Советы, как выигрывать.",
        "h1": "Как играть",
        "intro": "Мажобэ — маджонг-пасьянс с одним отличием: тайлы не снимаются с поля парами, а ложатся на полку на "
                 "четыре места. Ниже — правила, механики поля и режимы на двоих.",
        "sections": [
            ("Цель", ["Разобрать поле: взять все тайлы и собрать их парами на полке."]),
            ("Свободные тайлы", ["Брать можно только свободный тайл: сверху на нём пусто и хотя бы один бок, левый "
                                 "или правый, открыт. Тайлы, которые пока не взять, темнее.",
                                 "С 15-го уровня часть тайлов лежит рубашкой вверх: первый тап переворачивает тайл, "
                                 "второй — берёт."]),
            ("Полка", ["Тапни свободный тайл — он полетит на полку. Две одинаковые встретились на полке — пара "
                       "исчезает и приносит жёлуди.",
                       "Мест на полке всего четыре. Займёшь все четыре разными тайлами — уровень проигран, поэтому "
                       "прежде чем брать тайл, знай, где его близнец."]),
            ("Звёзды, подсказки и отмена", ["У каждого уровня от одной до пяти звёзд сложности. Каждая раздача "
                                            "проверена: у неё есть решение, а подсказка ведёт именно к нему.",
                                            "Подсказка показывает следующий удачный ход, отмена возвращает последний. "
                                            "Закончились — можно получить ещё, посмотрев короткую рекламу, если "
                                            "захочешь."]),
            ("Лёд, замки и загадки", ["Лёд: ледяной тайл не возьмёшь, пока его соседи не уйдут парами — тогда лёд "
                                      "треснет.",
                                      "Замки: тайл с замком откроется, когда соберёшь пару ключей того же металла — "
                                      "бронзу, серебро или золото.",
                                      "Загадка: у тайла с вопросом не видно картинки. Положи его на полку: встретит "
                                      "близнеца — сметёт всё поле разом, не встретит — просто займёт место."]),
            ("Дуэль онлайн", ["Двое игроков, два телефона, одно поле и одна полка. Тапать можно одновременно; пара "
                              "достаётся тому, кто её замкнул, побеждает тот, у кого пар больше.",
                              "Если твой тап забил бы полку четвёртым разным тайлом, он отменяется: тайл "
                              "возвращается на поле, а у тебя минус очко.",
                              "В «Дуэли на время» ходите по очереди, полоска показывает, чей ход.",
                              "Позови друга из таблицы лидеров или жми «Найти соперника». После партии — GG."]),
            ("Дуэль с Мажобэ", ["Та же дуэль против жабы Мажобэ — он сидит за полкой и косится на твои тайлы. Три "
                                "характера: Сонный, Хитрый и Азартный; чем азартнее, тем больше жёлудей за победу. "
                                "Работает без сети."]),
            ("Дуэт", ["Разбирайте одно поле вместе, полка общая. Победа — общая, и забитая полка — тоже."]),
            ("Уровень дня", ["Один уровень на всех в сутки. Рядом играет призрак лучшего игрока дня — обгони его и "
                             "получи бонус."]),
            ("Советы", ["Держи место на полке свободным: при трёх разных тайлах права на ошибку уже нет.",
                        "Бери тайлы, близнец которых уже виден.",
                        "Открывай новый слой, только когда на полке есть место — неизвестно, что под ним."]),
        ],
        "image": ("mechanics", "Лёд, замки и загадки на поле"),
    },
}

FAQ = {
    "en": ("Questions and answers", [
        ("How do I play mahjong with a friend?",
         "Open Two players → Duel and invite a friend from the leaderboard, or tap “Find an opponent”. You play on "
         "one board online, each on your own phone. In Duet you clear one board together."),
        ("Can I play offline?",
         "Yes: all levels and the duel with Mazhobe work without a connection. Online duels, leaderboards and the "
         "shop need one."),
        ("Is the game free?",
         "Yes. There are no purchases; when hints or undos run out, you can get another by watching a short ad if "
         "you want to."),
        ("How is it different from classic mahjong solitaire?",
         "Tiles don't vanish from the board in pairs — they go to a shelf with four slots, where pairs meet. Fill "
         "the shelf with four different tiles and you lose, so you have to think a move ahead."),
        ("Will my progress move to a new phone?",
         "Yes. Progress is stored anonymously, without registration, and comes back on a new phone through "
         "Google Play Games."),
        ("Is there an iPhone version?", "Not yet — the game is available on Android in Google Play."),
        ("Which languages does it support?", "22 languages, including English, Russian, Spanish, German, French, "
         "Portuguese, Turkish, Japanese, Korean and Chinese."),
    ]),
    "ru": ("Вопросы и ответы", [
        ("Как поиграть в маджонг с другом?",
         "Открой «Играть вдвоём» → «Дуэль» и позови друга из таблицы лидеров или жми «Найти соперника». Вы играете "
         "на одном поле по сети, каждый на своём телефоне. В «Дуэте» разбираете поле вместе."),
        ("Можно играть без интернета?",
         "Да: все уровни и дуэль с Мажобэ работают без сети. Дуэлям онлайн, таблице лидеров и лавке нужна связь."),
        ("Игра бесплатная?",
         "Да. Покупок нет; когда закончатся подсказки или отмены, можно получить ещё за короткую рекламу, если "
         "захочешь."),
        ("Чем это отличается от обычного маджонга?",
         "Тайлы не исчезают с поля парами, а ложатся на полку на четыре места — пары встречаются там. Забил полку "
         "четырьмя разными — проиграл, поэтому думать приходится на ход вперёд."),
        ("Прогресс перенесётся на новый телефон?",
         "Да. Прогресс хранится анонимно, без регистрации, и возвращается на новом телефоне через Google Play Игры."),
        ("Есть версия для iPhone?", "Пока нет — игра выходит для Android в Google Play."),
        ("На каких языках игра?", "22 языка, среди них русский, украинский, белорусский, казахский, английский, "
         "немецкий, испанский, турецкий, японский, корейский и китайский."),
    ]),
}

# Подписи сайта для новых частей.
UI = {
    "en": {"howto_link": "How to play", "home": "Home", "back_cta": "Ready to try?"},
    "ru": {"howto_link": "Как играть", "home": "Главная", "back_cta": "Попробуешь?"},
}
