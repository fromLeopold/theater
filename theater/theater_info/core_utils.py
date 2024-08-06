# utils/utils.py


def admin_check(user):
    return user.is_staff


def get_navigation_menu(user):
    """
    Возвращает меню навигации в зависимости от статуса пользователя.

    :param user: Объект пользователя Django
    :return: Словарь меню навигации
    """
    menu = {
        "navigation-menu": {
            "base-menu": {
                "Контакты": "theater_contacts",
                "Труппа": "troupe",
                "Репертуар": "repertoire",
                "Афиша": "afisha"
            }
        },
    }

    if user.is_authenticated:
        # Общие элементы для авторизованных пользователей
        menu["navigation-menu"]["client"] = {
            "Корзина": "basket",
            "Мои билеты": "order",
        }
        menu["auth-menu"] = {
            "Выход": "site_logout",
            f"{user.username}": "order",
        }
        if user.is_staff:
            # Дополнительный элемент для администраторов
            menu["navigation-menu"]["client"].update({"Административная панель": "admin_page"})

    else:
        # Элементы для неавторизованных пользователей
        menu.update({
            "auth-menu": {
                "Вход": "site_login",
                "Регистрация": "registration"
            }
        })

    return menu
