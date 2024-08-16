from django.db import models

from problems.models.problem_tag import ProblemTag


class ProblemTagRelation(models.Model):
    parent = models.ForeignKey(
        ProblemTag,
        on_delete=models.CASCADE,
        related_name='parent'
    )
    child = models.ForeignKey(
        ProblemTag,
        on_delete=models.CASCADE,
        related_name='child'
    )

    class field_name:
        PARENT = 'parent'
        CHILD = 'child'

    def __str__(self) -> str:
        return f'{self.pk} : #{self.parent.key} <- #{self.child.key}'
