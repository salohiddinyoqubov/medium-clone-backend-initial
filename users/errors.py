# users/errors.py

from django.conf import settings

BIRTH_YEAR_ERROR_MSG = "Tug'ilgan yili {min_year} dan katta va {max_year} dan kichik bo'lishi kerak.".format(
    min_year=settings.BIRTH_YEAR_MIN, max_year=settings.BIRTH_YEAR_MAX
)
ACTIVE_USER_NOT_FOUND_ERROR_MSG = (
    "Ushbu elektron pochta manzili bilan faol foydalanuvchi topilmadi!"
)
