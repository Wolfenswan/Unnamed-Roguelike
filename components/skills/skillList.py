from typing import List

from dataclasses import dataclass, field

from components.skills.baseSkill import BaseSkill


@dataclass
class SkillList:
    all : List[BaseSkill] = field(default_factory=list)

    def __len__(self):
        return len(self.all)

    def __iter__(self):
        yield from self.all

    def add_skill(self, skill: BaseSkill):
        self.all.append(skill)

    @property
    def available(self):
        """
        Available skills are skills which are currently not on cooldown.
        """
        available_skills = [skill for skill in self if skill.is_available]
        return available_skills

    def active(self, target, game):
        """
        Active skills are skills which are not on cooldown and all conditions (e.g. distance to target) are fulfilled.
        """
        possible_skills = [skill for skill in self.available if skill.is_active(target, game)]
        return possible_skills

    def cooldown(self, reset=False):
        for skill in self:
            skill.cooldown_skill(reset=reset)