from gi.repository import Gtk, Adw, Gio

import sys
#sys.path.append("./classes")
from .API import API

@Gtk.Template(resource_path='/de/davidbattefeld/envoye/window.ui')
class EnvoyeWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'EnvoyeWindow'

    main_box = Gtk.Template.Child()
    api_test_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        api_test_action = Gio.SimpleAction(name="api_test")
        api_test_action.connect("activate", self.test_action)
        self.add_action(api_test_action)

    def test_action(self, action, _):
      api = API()
      api.loadAndPrintLabels()
      #print(sys.path)
      #print("button pressed!")

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'envoye'
        self.props.version = "0.1.0"
        self.props.authors = ['dbt']
        self.props.copyright = '2023 dbt'
        self.props.logo_icon_name = 'de.davidbattefeld.envoye'
        self.props.modal = True
        self.set_transient_for(parent)
