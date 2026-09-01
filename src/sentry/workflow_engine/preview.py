from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from django.db.models import Q


class InvalidPreviewConfiguration(Exception):
    pass


@dataclass
class PreviewPlan:
    group_candidate_filters: list[Q] = field(default_factory=list)
    group_action_log_candidate_filters: list[Q] = field(default_factory=list)
    group_filters: list[Q] = field(default_factory=list)

    def add_group_candidates(self, condition: Q) -> None:
        self.group_candidate_filters.append(condition)

    def add_group_action_log_candidates(self, condition: Q) -> None:
        self.group_action_log_candidate_filters.append(condition)

    def add_group_filter(self, condition: Q) -> None:
        self.group_filters.append(condition)


class AlertPreviewBehavior:
    pass


class WorkflowTriggerPreviewBehavior(AlertPreviewBehavior, ABC):
    @abstractmethod
    def add_to_preview(self, plan: PreviewPlan, comparison: Any) -> None:
        raise NotImplementedError


class ActionFilterPreviewBehavior(AlertPreviewBehavior, ABC):
    @abstractmethod
    def filter_preview(self, plan: PreviewPlan, comparison: Any) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class UnsupportedPreviewBehavior(AlertPreviewBehavior):
    reason: str
