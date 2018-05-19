from django.db import models, IntegrityError

from swot.models import Swot

from authenticationjwt.models import User


class Manager(models.Manager):
    def create(self, added_by_id=None, member_id=None, swot_id=None):

        member_ids = set([
            m.member_id for m in SwotMember.objects.filter(swot_id=swot_id)
        ])

        if len(member_ids) > 0 and added_by_id not in member_ids:
            raise IntegrityError('Only swot member can add member')

        try:
            self.get(swot_id=swot_id, member_id=member_id)
            raise IntegrityError('(`swot_id` and `member_id`) must be unique')
        except SwotMember.DoesNotExist:
            pass

        ret = SwotMember(
            member_id=member_id,
            swot_id=swot_id,
            added_by_id=added_by_id
        )
        ret.save()

        return ret


class SwotMember(models.Model):
    objects = Manager()

    created = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 blank=False,
                                 null=False,
                                 related_name='+',
                                 related_query_name='+')
    member = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='+',
                               related_query_name='+')
    swot = models.ForeignKey(Swot,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False,
                             related_name='+',
                             related_query_name='+')

    def __str__(self):
        return '[SwotMember id={}, added_by={}, member={}, swot={}]'.format(
            self.id,
            self.added_by_id,
            self.member_id,
            self.swot_id
        )

    def __repr__(self):
        return self.__str__()