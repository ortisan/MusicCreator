import os

class Configs(object):

    @classmethod
    def get_project_home(cls):
      proj_home = os.getenv("MUSIC_PROJECT_HOME")
      assert proj_home, '"MUSIC_PROJECT_HOME" environment variable must be set'
      return proj_home