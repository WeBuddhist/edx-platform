"""
Signal handlers for offline mode.
"""
from django.dispatch.dispatcher import receiver
from opaque_keys.edx.locator import LibraryLocator

from xmodule.modulestore.django import SignalHandler

from .tasks import generate_offline_content_for_course
from .toggles import is_offline_mode_enabled


@receiver(SignalHandler.course_cache_updated)
def generate_offline_content_on_course_cache_update(sender, course_key, **kwargs):  # pylint: disable=unused-argument
    """
    Catches the signal that a course has been updated in the module
    store and generates offline content for the course.
    Ignores cache update signals from content libraries.
    """
    if isinstance(course_key, LibraryLocator):
        return

    # Global flag on, course override off: this course gets no ZIP job.
    if not is_offline_mode_enabled(course_key):
        return

    generate_offline_content_for_course.apply_async([str(course_key)])
