from django.core.exceptions import ValidationError


def inn_validator(value: str) -> None:
    """ Валидация ИНН по длине и контрольным цифрам """
    try:
        digits_list = n = list(map(int, value))
    except ValueError as e:
        raise ValidationError(f'Проверьте введенный ИНН: {value}. ИНН должен содержать только цифры. ({e})')

    if len(digits_list) == 10:  # Для 10-значного ИНН, присваиваемого юридическому лицу
        multipliers = m = (2, 4, 10, 3, 5, 9, 4, 6, 8)

        received_check_digits = n[-1]
        computed_check_digits = (sum((m*n for m, n in zip(m, n))) % 11) % 10

    elif len(digits_list) == 12:  # Для 12-значного ИНН, присваиваемого физическому лицу
        multipliers = m = ((7, 2, 4, 10, 3, 5, 9, 4, 6, 8),
                           (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8))

        received_check_digits = n[-2], n[-1]
        computed_check_digits = ((sum((m*n for m, n in zip(m[0], n))) % 11) % 10,
                                 (sum((m*n for m, n in zip(m[1], n))) % 11) % 10)

    else:
        raise ValidationError(f"Проверьте введенный ИНН: {value} ({len(value)} знаков) "
                              f"Длина ИНН должна быть: 10 знаков для юридического лица, "
                              f"или 12 знаков для физицеского лица.")

    if received_check_digits != computed_check_digits:
        raise ValidationError(f"Проверьте введенный ИНН: {value}. Контрольные цифры ИНН не совпадают.")