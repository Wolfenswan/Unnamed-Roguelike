from dataclasses import dataclass, field

from components.skill import Skill


@dataclass
class Skills:
    listing : list = field(default_factory=list)

    def __len__(self):
        return len(self.listing)

    def __iter__(self):
        yield from self.listing

    def add_skill(self, skill: Skill):
        self.listing.append(skill)

    @property
    def available(self):
        """
        Available skills are skills which are currently not on cooldown.
        """
        available_skills = [skill for skill in self if skill.is_available]
        return available_skills

    def possible(self, target, game):
        """
        Possible skills are skills which are not on cooldown and all conditions (e.g. distance to target) are fulfilled.
        """
        possible_skills = [skill for skill in self.available if skill.is_possible(target, game)]
        return possible_skills

    def cooldown(self, reset=False):
        for skill in self:
            skill.cooldown_skill(reset=reset)