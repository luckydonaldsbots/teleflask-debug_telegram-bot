# -*- coding: utf-8 -*-
__author__ = "luckydonald"

try:    from gitinfo_values import __all__
except: __all__ = ["GIT_COMMIT", "GIT_COMMIT_SHORT", "GIT_DIRTY_PROJECT", "GIT_DIRTY_GLOBAL", "GIT_MESSAGE", "GIT_AUTHOR", "GIT_DATE", "GIT_HEAD", "GIT_BRANCHES", "GIT_TAGS", "VERSION_STR", "GIT_MODIFIED_FILES", "GIT_MODIFIED_FILES_STR"]

try:    from gitinfo_values import GIT_COMMIT
except: GIT_COMMIT = None

try:    from gitinfo_values import GIT_DIRTY_PROJECT
except: GIT_DIRTY_PROJECT = None

try:    from gitinfo_values import GIT_DIRTY_GLOBAL
except: GIT_DIRTY_GLOBAL = None

try:    from gitinfo_values import GIT_COMMIT_SHORT
except: GIT_COMMIT_SHORT = None

try:    from gitinfo_values import GIT_MESSAGE
except: GIT_MESSAGE = None

try:    from gitinfo_values import GIT_AUTHOR
except: GIT_AUTHOR = None

try:    from gitinfo_values import GIT_AUTHOR
except: GIT_AUTHOR = None

try:    from gitinfo_values import GIT_DATE
except: GIT_DATE = None

try:    from gitinfo_values import GIT_HEAD
except: GIT_HEAD = None

try:    from gitinfo_values import GIT_BRANCHES
except: GIT_BRANCHES = []

try:    from gitinfo_values import GIT_TAGS
except: GIT_TAGS = []

try:    from gitinfo_values import VERSION_STR
except: VERSION_STR = []

try:    from gitinfo_values import GIT_MODIFIED_FILES
except: GIT_MODIFIED_FILES = {"added": [], "copied": [], "deleted": [], "modified": [], "renamed": [], "type_changed":[], "unmerged": [], "unknown": [], "broken": [], "by_file":{}}

try:    from gitinfo_values import GIT_MODIFIED_FILES_STR
except: GIT_MODIFIED_FILES_STR = ""
