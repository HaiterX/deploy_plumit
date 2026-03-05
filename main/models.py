from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class Case(models.Model):
    title = models.CharField("Название", max_length=200)
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True)
    description = models.TextField("Описание (под заголовком)", blank=True)

    show_on_home = models.BooleanField("Показывать на главной странице", default=False)

    COVER_SCALE_40 = 40
    COVER_SCALE_60 = 60
    COVER_SCALE_100 = 100
    COVER_SCALE_CHOICES = (
        (COVER_SCALE_40, "40%"),
        (COVER_SCALE_60, "60%"),
        (COVER_SCALE_100, "100%"),)

    cover_scale = models.PositiveSmallIntegerField(
        "Масштаб обложки (для списка)",
        choices=COVER_SCALE_CHOICES,
        default=COVER_SCALE_100,)


    HOME_POS_EMPTY = 0
    HOME_POS_1 = 1
    HOME_POS_2 = 2
    HOME_POS_3 = 3
    HOME_POS_CHOICES = (
        (HOME_POS_EMPTY, "Пустая позиция"),
        (HOME_POS_1, "1"),
        (HOME_POS_2, "2"),
        (HOME_POS_3, "3"),
    )

    home_position = models.PositiveSmallIntegerField(
        "Позиция на главной",
        choices=HOME_POS_CHOICES,
        blank=True,
        null=True,
    )
    cover_alt = models.CharField("Alt обложки", max_length=255, blank=True)

        # Показ и порядок на странице our-works
    show_on_works = models.BooleanField("Показывать на странице 'Наши проекты'", default=True)

    works_block = models.PositiveIntegerField(
        "Блок на странице 'Наши проекты' (ряд)",
        blank=True,
        null=True,
    )

    WORKS_POS_EMPTY = 0
    WORKS_POS_1 = 1
    WORKS_POS_2 = 2
    WORKS_POS_3 = 3
    WORKS_POS_CHOICES = (
        (WORKS_POS_EMPTY, "Пустая позиция"),
        (WORKS_POS_1, "1"),
        (WORKS_POS_2, "2"),
        (WORKS_POS_3, "3"),
    )

    works_position = models.PositiveSmallIntegerField(
        "Позиция в блоке (1-3)",
        choices=WORKS_POS_CHOICES,
        blank=True,
        null=True,
    )

    sphera_bg_image = models.ImageField(

        "Фон блока (sphera)",
        upload_to="cases/sphera/",
        blank=True,
        null=True)

    contact_bg_image = models.ImageField(


        "Фон блока формы",
        upload_to="cases/contact/",
        blank=True,
        null=True)

    desktop_title_gradient = models.CharField(
        "Desktop заголовок (градиентная часть)",
        max_length=80,
        blank=True,
        null=True)

    desktop_title_text = models.CharField(
        "Desktop заголовок (обычная часть)",
        max_length=200,
        blank=True,
        null=True)






    # NEW: картинки как в techimpuls.html
    cover_image = models.ImageField("Обложка для списка (avatar)", upload_to="cases/cover/", blank=True, null=True)
    hero_image = models.ImageField("Главная картинка (фон сверху)", upload_to="cases/hero/", blank=True, null=True)
    mockup_image = models.ImageField("Mockup (большая картинка под кнопкой)", upload_to="cases/mockup/", blank=True, null=True)

    # NEW: тексты блоков “Задача / Исполнение / Результат”
    task_text = models.TextField("Задача", blank=True)
    execution_text = models.TextField("Исполнение", blank=True)
    result_text = models.TextField("Достигнутый результат", blank=True)

    # NEW: блоки Desktop/Mobile как в techimpuls.html
    desktop_text = models.TextField("Текст блока Desktop", blank=True)
    desktop_image = models.ImageField("Картинка Desktop (macbook)", upload_to="cases/desktop/", blank=True, null=True)


    is_published = models.BooleanField("Опубликовано", default=True)
    sort = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    slug = models.SlugField("Ссылка (slug)", max_length=200, unique=True)

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"
        ordering = ["created_at"]  # чтобы новые шли вниз

        constraints = [
            models.UniqueConstraint(
                fields=["home_position"],
                condition=Q(show_on_home=True) & Q(home_position__in=[1, 2, 3]),
                name="uniq_home_position_1_3_when_show_on_home",),
            models.CheckConstraint(
                condition=Q(home_position__in=[0, 1, 2, 3]) | Q(home_position__isnull=True),
                name="check_home_position_0_3_or_null",),
                
            models.UniqueConstraint(
                fields=["works_block", "works_position"],
                condition=Q(show_on_works=True) & Q(works_position__in=[1, 2, 3]),
                name="uniq_works_block_pos_1_3_when_show_on_works",),
            models.CheckConstraint(
                condition=Q(works_position__in=[0, 1, 2, 3]) | Q(works_position__isnull=True),
                name="check_works_position_0_3_or_null",),]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.show_on_home:
            if self.home_position not in (0, 1, 2, 3):
                raise ValidationError({"home_position": "Выбери позицию 1, 2, 3 или Пустая позиция."})

            qs = Case.objects.filter(show_on_home=True).exclude(pk=self.pk)
            if qs.count() >= 3:
                raise ValidationError({"show_on_home": "На главной можно показать максимум 3 кейса."})
        else:
            self.home_position = None

        # --- our-works ---
        if self.show_on_works:
            if not self.works_block or self.works_block < 1:
                raise ValidationError({"works_block": "Укажи номер блока (ряд), начиная с 1."})

            if self.works_position not in (0, 1, 2, 3):
                raise ValidationError({"works_position": "Выбери позицию 1, 2, 3 или Пустая позиция."})
        else:
            self.works_block = None
            self.works_position = None  


class CaseMobileBlock(models.Model):
    LAYOUT_CHOICES = (
        ("image_left", "Картинка слева, текст справа"),
        ("image_right", "Картинка справа, текст слева"),
         ("image_only", "Оставить фото без текста"),
    )

    case = models.ForeignKey(
        "Case",
        on_delete=models.CASCADE,
        related_name="mobile_blocks",
        verbose_name="Кейс"
    )

    # можно оставить пустыми — тогда будет просто картинка
    title_gradient = models.CharField("Заголовок (градиент)", max_length=80, blank=True, null=True)
    title_text = models.CharField("Заголовок (текст)", max_length=200, blank=True, null=True)
    text = models.TextField("Текст", blank=True, null=True)

    # можно оставить пустым, но обычно item без картинки не нужен
    image = models.ImageField(upload_to="cases/mobile/items/", blank=True, null=True)

    layout = models.CharField("Расположение", max_length=20, choices=LAYOUT_CHOICES, default="image_right")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Моб. элемент"
        verbose_name_plural = "Моб. элементы"

    class CaseMobileBlock(models.Model):

        LAYOUT_CHOICES = (

            ("image_left", "Картинка слева, текст справа"),
            ("image_right", "Картинка справа, текст слева"),
            ("image_only", "Оставить фото без текста"),)

    case = models.ForeignKey(
        "Case",
        on_delete=models.CASCADE,
        related_name="mobile_blocks",
        verbose_name="Кейс",
    )

    title_gradient = models.CharField("Заголовок (градиент)", max_length=80, blank=True, null=True)
    title_text = models.CharField("Заголовок (текст)", max_length=200, blank=True, null=True)
    text = models.TextField("Текст", blank=True, null=True)

    image = models.ImageField(upload_to="cases/mobile/items/", blank=True, null=True)

    layout = models.CharField("Расположение", max_length=20, choices=LAYOUT_CHOICES, default="image_right")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Моб. элемент"
        verbose_name_plural = "Моб. элементы"

    def clean(self):
        super().clean()

        if self.layout == "image_only":
            if self.title_gradient or self.title_text or self.text:
                raise ValidationError({
                    "title_gradient": "В режиме 'Фото без текста' заголовки/текст должны быть пустыми.",
                    "title_text": "В режиме 'Фото без текста' заголовки/текст должны быть пустыми.",
                    "text": "В режиме 'Фото без текста' заголовки/текст должны быть пустыми.",
                })

            if self.image:
                raise ValidationError({
                    "image": "В режиме 'Фото без текста' не используй поле 'Картинка'. Добавляй фото ниже (до 4)."
                })

            if self.pk and self.images.count() > 4:
                raise ValidationError("В одном блоке можно максимум 4 фотографии.")
        else:
            if self.pk and self.images.exists():
                raise ValidationError("Доп. фотографии можно добавлять только в режиме 'Фото без текста'.")



class CaseMobileBlockImage(models.Model):
    block = models.ForeignKey(
        "CaseMobileBlock",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="cases/mobile/items/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Block #{self.block_id} image #{self.id}"




class CaseImage(models.Model):
    SCALE_40 = 40
    SCALE_60 = 60
    SCALE_100 = 100
    SCALE_CHOICES = (
        (SCALE_40, "40%"),
        (SCALE_60, "60%"),
        (SCALE_100, "100%"),
    )

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="images", verbose_name="Кейс")
    image = models.ImageField("Фото", upload_to="cases/gallery/")
    scale = models.PositiveSmallIntegerField("Масштаб", choices=SCALE_CHOICES, default=SCALE_100)
    title = models.CharField("Заголовок под фото", max_length=200, blank=True)
    subtitle = models.TextField("Текст под фото", blank=True)
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Фото кейса"
        verbose_name_plural = "Фото кейса"
        ordering = ["sort", "id"]

    def __str__(self):
        return f"{self.case.title} — {self.get_scale_display()}"