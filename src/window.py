from gi.repository import Gtk, Adw, Gio

import sys
from .API import API
from .label import Label

@Gtk.Template(resource_path='/de/davidbattefeld/envoye/window.ui')
class EnvoyeWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'EnvoyeWindow'

    main_box = Gtk.Template.Child()
    api_test_button = Gtk.Template.Child()
    sidebar_list_box = Gtk.Template.Child()
    mail_body_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = API()
        self.labels = []

        api_test_action = Gio.SimpleAction(name="api_test")
        api_test_action.connect("activate", self.test_action)
        self.add_action(api_test_action)
        self.load_labels()

        # load_labels_action = Gio.SimpleAction(name="load_labels")
        # load_labels_action.connect("activate", self.load_labels)
        # self.add_action(load_labels_action)

    def test_action(self, action, _):
      self.api.load_and_print_labels()

    def load_labels(self):
        loadedLabels = self.api.load_labels()
        if not loadedLabels:
            pass

        for item in loadedLabels:
            label = Label(item['id'], item['name'], item['type'])
            self.labels.append(label)

            text = Gtk.Label.new(label.name)
            box_row = Gtk.ListBoxRow()
            box_row.set_child(text)
            self.sidebar_list_box.append(box_row)

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
