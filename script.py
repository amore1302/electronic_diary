import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from datacenter.models import Schoolkid
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Mark
from datacenter.models import Chastisement


def get_praise():
    praises = ["Молодец!"
        ,"Отлично!"
        , "Хорошо!"
        , "Гораздо лучше, чем я ожидал!"
        , "Ты меня приятно удивил!"
        , "Великолепно!"
        , "Прекрасно!"
        , "Ты меня очень обрадовал!"
        , "Именно этого я давно ждал от тебя!"
        , "Сказано здорово – просто и ясно!"
        , "Ты, как всегда, точен!"
        , "Очень хороший ответ!"
        , "Талантливо!"
        , "Ты сегодня прыгнул выше головы!"
        , "Я поражен!"
        , "Уже существенно лучше!"
        , "Потрясающе!"
        , "Замечательно!"
        , "Прекрасное начало!"
        , "Так держать!"
        , "Ты на верном пути!"
        , "Здорово!"
        , "Это как раз то, что нужно!"
        , "Я тобой горжусь!"
        , "С каждым разом у тебя получается всё лучше!"
        , "Мы с тобой не зря поработали!"
        , "Я вижу, как ты стараешься!"
        , "Ты растешь над собой!"
        , "Ты многое сделал, я это вижу!"
        , "Теперь у тебя точно все получится!"
    ]
    random.seed()
    return random.choice(praises)

def create_commendation(name_schoolkid, name_subject):
    try:
        current_schoolkid=Schoolkid.objects.get(full_name__icontains=name_schoolkid)
    except ObjectDoesNotExist:
        print("Не нашли ученика = "+ name_schoolkid)
        return
    except MultipleObjectsReturned:
        print("Много учеников с именем = "+ name_schoolkid)
        return

    try:
        current_subject = Subject.objects.get(title__icontains=name_subject
        ,year_of_study=current_schoolkid.year_of_study)
    except ObjectDoesNotExist:
        print("Не нашли Предмета = " + name_subject)
        return
    except MultipleObjectsReturned:
        print("Много предметов с именем = " + name_subject)
        return

    last_lesson = Lesson.objects.filter(year_of_study=current_schoolkid.year_of_study
                , group_letter=current_schoolkid.group_letter
                , subject= current_subject).order_by('-date').last()
    if not last_lesson:
        print("не обнаружили уроков для ученика = " + name_schoolkid + " и предмету = " +  name_subject)
        return

    praise = get_praise()
    teacher = last_lesson.teacher

    Commendation.objects.create(text=praise, created=last_lesson.date,schoolkid=current_schoolkid
                                , subject=current_subject,teacher=teacher)

def fix_marks(schoolkid):
    bad_marks=Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    for current_mark in bad_marks:
    current_mark.points = current_mark.points + 2
    current_mark.save()

def remove_chastisements(schoolkid):
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisements.delete()